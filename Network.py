import threading
import queue
import DataLink, PhysicalLayer, MorseCode
import re
from options import *

GLOBAL_IP = DataLink.ID

global2local = {'B':'B', 'A':'A', 'I':'I'}
pattern = "[A-Za-z0-9 ]*"

def receive(q, dlq):
    """Recieves from datalink, reads header sees if it needs to go anywhere else"""
    def extractHeader(m):

        """ m is the message """
        try:
            msgSplit = m.split()

            recip = msgSplit[0]
            src = msgSplit[1]
            messageNum = int(msgSplit[2])
            totalMsgs = int(msgSplit[3])
            msg = ' '.join(msgSplit[4:])

            return (recip, src, messageNum, totalMsgs, msg )
        except IndexError:
            return

    messageQueue = {} #src: list of messages (list has preallocated space)

    while True:
        msgFull = dlq.get()
        msgDict = extractHeader(msgFull)
        #what to do with this message
        if msgDict[recipient] == GLOBAL_IP:
            msgBuilder = messageQueue.get(msgDict[source], [None]*(msgDict[total])) #get an array of empty if there are no prev
            msgBuilder[msgDict[position]-1] = msgDict[message] #put the message in the right place
            messageQueue[msgDict[source]] = msgBuilder # set into the dict
            if msgDict[position] == msgDict[total]:
                #put together the whole message
                q.put({'message' : "".join(messageQueue.get(msgDict[source], [])), 'source':msgDict[source]})
                
        else:
            pass

def send(msgDict):
    """Makes header, sends to datalink to send aling with the local ip and stuff"""
    message = msgDict['message']
    #how to know the morse code length
    splitMessages = []
    currentLen = 0
    currentStr = ''
    #calculating length of message
    for c in message.upper():
        currentStr+=c
        if c == ' ':
            currentLen += DIT_TIME
        else:
            morse = MorseCode.MorseCode[c]
            for d in morse:
                if d=='.':
                    currentLen+=DIT_TIME
                else:
                    currentLen+=3*DIT_TIME
            currentLen+=DIT_TIME
        if currentLen>95:
            splitMessages.append((currentStr,currentLen))
            currentLen = 0
            currentStr = ''
    if currentStr != '':
        splitMessages.append((currentStr,currentLen))

    for i in range(len(splitMessages)):
        messagesLeft = i+1

        msg = splitMessages[i][0]

        packet = "{} {} {} {} {}".format(msgDict["recipient"], GLOBAL_IP, messagesLeft, len(splitMessages), msg)
        
        DataLink.transmit(global2local[msgDict['recipient']], packet)

def applicationishLayerTX():
    """Simulates application layer input"""
    while True:
        recipient = input('ADDRESS OF RECIPIENT: ')
        message = input('MESSAGE TO SEND: ')
        
        if re.match(pattern, message) and re.match(pattern, recipient):
            send({
                'recipient': recipient,  
                'message':message})
        else:
            print('Try Again')

def applicationishLayerRX(q):
    """Simulates application layer input"""
    while True:
        msgDict = q.get()
        print(msgDict['source'])
        print(msgDict['message'])

if __name__ == "__main__":
    #queues to move info
    rxdlq = queue.Queue()
    txdlq = queue.Queue()
    rxq = queue.Queue()
    txq = queue.Queue()
    physicalq = queue.Queue()
    
    #network threads
    rx=threading.Thread(target=receive, name="NETWORKRX",args=(rxq, rxdlq))
    rx.start()

    #app layer threads
    appin = threading.Thread(target=applicationishLayerRX, name="APPIN",args=(rxq,))
    appout = threading.Thread(target=applicationishLayerTX, name="APPOUT")
    appin.start()
    appout.start()

    #data link threads
    rxDatalink=threading.Thread(target=DataLink.readMessage, name="DLRX",args=(physicalq,rxdlq))
    rxDatalink.start()

    #physical layer thread
    r = threading.Thread(target=PhysicalLayer.detect_blinks,name='PLRX',args=(physicalq,))
    r.start()
        
    
    #join threads
    rx.join()
    appin.join()
    appout.join()
    rxDatalink.join()
    r.join()

    print('EXIT')
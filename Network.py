import threading
import queue
import DataLink
from options import *

GLOBAL_IP = DataLink.ID
prot = "B"

global2local = {'B':'B', 'A':'A'}

def receive(q, dlq):
    """Recieves from datalink, reads header sees if it needs to go anywhere else"""
    def extractHeader(m):
        """ m is the message """
        msgSplit = m.split()
        print(msgSplit)

        recip = msgSplit[0]
        src = msgSplit[1]
        messageNum = int(msgSplit[2])
        totalMsgs = int(msgSplit[3])
        msg = ' '.join(msgSplit[4:])

        return {
            'recipient': recip, 
            'source':src, 
            'position':messageNum, 
            'total': totalMsgs,
            'message':message }

    messageQueue = {} #src: list of messages (list has preallocated space)

    while True:
        msgFull = dlq.get()
        msgDict = extractHeader(msgFull)
        #what to do with this message
        if msgDict['recipient'] == GLOBAL_IP:
            msgBuilder = messageQueue.get(msgDict['source'], [None]*(msgDict['total'])) #get an array of empty if there are no prev
            msgBuilder[msgDict['position']-1] = msgDict['message'] #put the message in the right place
            messageQueue[msgDict['source']] = msgBuilder # set into the dict
            if msgDict['position'] == msgDict['total']:
                #put together the whole message
                q.put("".join(messageQueue.get(msgDict['source'], [])))
                
        else:
            pass

def send(q, dlq):
    """Makes header, sends to datalink to send aling with the local ip and stuff"""
    while True:
        msgDict = q.get()
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
            if currentLen>70:
                splitMessages.append((currentStr,currentLen))
                currentLen = 0
                currentStr = ''
        if currentStr != '':
            splitMessages.append((currentStr,currentLen))

        for i in range(len(splitMessages)):
            messagesLeft = i+1

            msg = splitMessages[i][0]

            packet = "{} {} {} {} {}".format(msgDict["recipient"], GLOBAL_IP, messagesLeft, len(splitMessages), msg)
            
            dlq.put({'recip':global2local[msgDict['recipient']],
                'message':packet})

def applicationishLayerTX(q):
    """Simulates application layer input"""
    while True:
        recipient = input('ADDRESS OF RECIPIENT: ')
        message = input('MESSAGE TO SEND: ')
        q.put({
            'recipient': recipient, 
            'protocol':prot, 
            'message':message})

def applicationishLayerRX(q):
    """Simulates application layer input"""
    while True:
        msgDict = q.get()
        print msgDict['source']
        print msgDict['message']

if __name__ == "__main__":
    #queues to move info
    rxdlq = queue.Queue()
    txdlq = queue.Queue()
    rxq = queue.Queue()
    txq = queue.Queue()
    physicalq = queue.Queue()
    
    #network threads
    tx=threading.Thread(target=send,name="NETWORKTX",args=(txq, txdlq))
    tx.start()
    rx=threading.Thread(target=receive, name="NETWORKRX",args=(rxq, rxdlq))
    rx.start()

    #app layer threads
    appin = threading.Thread(target=applicationishLayerRX, name="APPIN",args=(rxq))
    appout = threading.Thread(target=applicationishLayerTX, name="APPOUT",args=(txq))
    appin.start()
    appout.start()

    #data link threads
    txDatalink=threading.Thread(target=transmit,name="TRANSMIT", args=(txdlq,))
    txDatalink.start()
    rxDatalink=threading.Thread(target=readMessage, name="DATALINKRECIEVER",args=(physicalq,rxdlq))
    rxDatalink.start()
    PhysicalLayer.reciever(physicalq)
    
    #join threads
    tx.join()
    rx.join()
    appin.join()
    appout.join()
    txDatalink.join()
    rxDatalink.join()
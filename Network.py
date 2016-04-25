import threading
import queue
import DataLink
from options import *

GLOBAL_IP = DataLink.ID
prot = "B"

global2local = {'B':'B', 'A':'A'}

def recieve(q, dlq):
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
            if msgDict['position'] == msgDict['total']:
                q.put("".join(messageQueue.get(msgDict['source'], []))+msgDict['message'])
            else:
                msgBuilder = messageQueue.get(msgDict['source'], [None]*(msgDict['total']))
                msgBuilder[msgDict['position']-1] = msgDict['message']
                messageQueue[msgDict['source']] = msgBuilder
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
    #2 queues for dicts of {payload, to, from}
    #one for transmitting, one for receiving
    rxq = queue.Queue()
    tx=threading.Thread(target=transmit,name="NETWORKRX",args=(txq,))
    tx.start()
    txq = queue.Queue()
    rx=threading.Thread(target=readMessage, name="NETWORKTX",args=(rxq,))
    rx.start()
    #how to pull from physical layer's strings?
    tx.join()
    rx.join()
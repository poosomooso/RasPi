import threading
import queue
import PhysicalLayer
import MorseCode
import time
from options import *

ID = 'B'

def transmit(recip, message):
        msg = ' '+message

        packet = recip+' '+ID+' '
        
        parity = getHash(packet+msg)
        
        PhysicalLayer.physicalTransmit(packet+parity+msg)
        
        # start = time.time()
        # while True:
        #     try:
        #         ok = parityQ.get_nowait()
        #         if ok['recipient'] == msgDict['recipient'] and ok['source'] == ID:
        #             #recieved ok message
        #             break
        #     except queue.Empty:
        #         pass
            
        #     if time.time() - start >= 30: #waiting for 30 seconds
        #         PhysicalLayer.physicalTransmit(packet+parity+msg)
        #         start = time.time()



def readMessage(q, networkq):
    """ q is the queue to push messages to """
    def extractHeader(m):
        try:
            msgSplit = m.split()
            print(msgSplit)

            recip = msgSplit[0]
            src = msgSplit[1]

            # if len(msgSplit)==2:
            #     return {
            #         'recipient':recip,
            #         'source':src }

            # else:
            parity = msgSplit[2]
            msg = ' '.join(msgSplit[3:])

            return (recip, src, parity, msg )
        except IndexError:
            return None
    messageProgress = {}
    while True:
        dit=q.get()
        dits = ''

        #build dit string
        for d in dit:
            dits+='.' if d == 1 else ' '
        #interpret string
        
        morse_mess = ''
        morse_chars = dits.rstrip('.').lstrip(' ')
        print(morse_chars)
        morse_chars = morse_chars.split(' ')
        for c in morse_chars:
            if c=='':
                morse_mess+=' '
            elif c=='.':
                morse_mess+='.'
            elif c=='...':
                morse_mess+='-'

        message = ''
        d = MorseCode.ReverseCode
        letters = morse_mess.split(' ')
        spaced = False

        for l in range(len(letters)):
            #two spaces in a row is a message space
            if spaced:
                if letters[l]!='':
                    message+=' '
                    spaced=False
            if letters[l]=='' and l+1<len(letters) and letters[l+1]=='':
                spaced = True
            else:
                try:
                    message+=d[letters[l]]
                except KeyError:
                    pass
        print(message)
        print('DL')

        data = extractHeader(message)
        if data == None:
            return
        # if len(data) == 2:
        #     parityQ.put(data)
        else:
            src = data[source]
            if data[recipient] == ID:
                #parityMsg = ' '.join([data['recipient'], src, '', data['message']])
                # if data['parity'] == getHash(parityMsg):
                    # PhysicalLayer.physicalTransmit('{} {}'.format(src, data['recipient']))
                # else:
                #     break;
                networkq.put(data[dlmessage])
            

def getHash(msg):
    s = 0
    for c in msg:
        s += ord(c.upper())
    return chr(65 + s % 26)
    

        



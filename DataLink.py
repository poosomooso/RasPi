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
        
        parity = getHash(message)#getHash(packet+msg)
        
        PhysicalLayer.physicalTransmit(packet+parity+msg)


def readMessage(q, networkq):
    """ q is the queue to push messages to """
    def extractHeader(m):
        try:
            msgSplit = m.split()
            #print(msgSplit)

            recip = msgSplit[0]
            src = msgSplit[1]
            parity = msgSplit[2]
            msg = ' '.join(msgSplit[3:])

            return (recip, src, parity, msg )
        except IndexError:
            return None
    messageProgress = {}
    while True:
        times = q.get()
        dit = times[1]
        ditTimes = times[0]
        dits = ''

        #build dit string
        for d in ditTimes:
            for i in range(round(d/DIT_TIME)):
                dits+='.' if dit == 1 else ' '
            dit ^= 1
        #interpret string
        
        morse_mess = ''
        morse_chars = dits.rstrip('.').lstrip(' ')
        #print(morse_chars)
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

        else:
            src = data[source]
            if data[recipient] == ID:
                if data[parity] != getHash(data[dlmessage]):
                    print('ERROR: DID NOT SEND CORRECTLY')
                else:
                    networkq.put(data[dlmessage])
            

def getHash(msg):
    s = 0
    for c in msg:
        s += ord(c.upper())
    return chr(65 + s % 26)
    

        



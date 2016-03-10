#
## Introducton to Python breadboarding - Receive Blinks
#
from  SetPin import SetPin
import time
import MorseCode
import threading
import queue
from BlinkTX import *

#thread to read in, generates series of dits
#thread to translate
Q = queue.Queue()
def receiveblinks(RXpin,blinks=200,duration=.0909090909/4):
    dits=''
    num_spaces = 0
    for i in range(blinks):
        
        num_high = 0
        for j in range(11):
            if RXpin.read_pin():
                num_high += 1
            time.sleep(duration)
        reading = round(num_high/11.0)
        if reading == 0:
            num_spaces+=1
        else:
            num_spaces=0
        if num_spaces>=15 and not dits.isspace():
        	#end of message
            Q.put(dits)
            dits = ''
        	#send message string to somewhere
        dits+=("." if  reading==1 else " ")
    Q.put('END')
    
def parse_blinks(datalinkq):
    dits=Q.get()
    while dits!='END':
        morse_mess = ''
        morse_chars = dits.split(' ')

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
        datalinkq.put(item=message)
        print(message)
        dits=Q.get()
    print('END MESSAGES')

def physicalTransmit(msg):
    with BlinkTX(15,"GPIO_22",direction="TX") as blink:
        blink.blinkTX(0,1)
        blink(MorseTX(msg.upper()))

def reciever(datalinkq):
    with SetPin(16,"GPIO_23",direction="RX") as RXpin:
        r = threading.Thread(target=receiveblinks,name='RECIEVE',args=(RXpin,))
        p = threading.Thread(target=parse_blinks,name='PARSE',args=(datalinkq,))
        r.start()
        p.start()
        r.join()
        p.join()
        print('EXIT')

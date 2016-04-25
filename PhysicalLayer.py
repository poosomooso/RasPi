#
## Introducton to Python breadboarding - Receive Blinks
#
from  SetPin import SetPin
import time
import MorseCode
import threading
import queue
from BlinkTX import *
from options import *

#thread to read in, generates series of dits
#thread to translate
Q = queue.Queue()
def detect_blinks(RXpin,duration=float(DIT_TIME)/DIT_SAMPLES):
    while True:
        if RXpin.read_pin():
            Q.put('.')
            receive_blinks(RXpin, duration)
        else:
            time.sleep(duration)


def receive_blinks(RXpin,duration=float(DIT_TIME)/DIT_SAMPLES):
    dits=''
    num_dits = 0
    # raw = ''

    while True:
        num_high = 0
        for j in range(DIT_SAMPLES):
            t = time.time()
            if RXpin.read_pin():
                num_high += 1
            #     raw += '.'
            # else:
            #     raw += ' '
            # if j == 0:
            #     t+=while_time
            time.sleep(duration - (time.time() - t))
        # raw += '|\n'
        reading = round(float(num_high)/DIT_SAMPLES)

        if reading == 1:
            num_dits += 1
        else:
            num_dits = 0
        if num_dits >= 8:# and not dits.isspace():
        	#end of message
            # Q.put(dits)
            # dits = ''
            Q.put('END')
        	#send message string to somewhere
            break
        if reading == 1:
            Q.put(".")
        else:
            Q.put(" ")
    # print(raw)
    
def parse_blinks(datalinkq):
    while True:
        dit=Q.get()
        dits = ''

        #build dit string
        while dit!='END':
            dits+=dit
            dit = Q.get()
        #interpret string
        print(dits)
        morse_mess = ''
        morse_chars = dits.rstrip('.').split(' ')

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
        print('END MESSAGE')

def physicalTransmit(msg):
    print(msg)
    with BlinkTX(15,"GPIO_22",direction="TX") as blink:
        blink.blinkTX(0, DIT_TIME)
        blink(MorseTX(msg.upper()))

def reciever(datalinkq):
    with SetPin(16,"GPIO_23",direction="RX") as RXpin:
        r = threading.Thread(target=detect_blinks,name='RECIEVE',args=(RXpin,))
        p = threading.Thread(target=parse_blinks,name='PARSE',args=(datalinkq,))
        r.start()
        p.start()
        r.join()
        p.join()
        print('EXIT')

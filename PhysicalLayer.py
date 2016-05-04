#
## Introducton to Python breadboarding - Receive Blinks
#
from  SetPin import SetPin
import time
import MorseCode
import threading
import queue
import array
from BlinkTX import *
from options import *

#thread to read in, generates series of dits
#thread to translate
def detect_blinks(dlq ,duration=float(DIT_TIME)/DIT_SAMPLES):

    with SetPin(16,"GPIO_23",direction="RX") as RXpin:  
        
        while True:
            arr = array.array('b', [1]*10000)
            if RXpin.read_pin():
                #Q.put('.')
                receive_blinks(RXpin, dlq, arr, duration)
            else:
                time.sleep(duration/2)


def receive_blinks(RXpin, dlq, arr, duration=float(DIT_TIME)/DIT_SAMPLES):
    #timearr = array.array('d', [0]*500)
    num_dits = 0
    index = 0

    while True:
        num_high = 0
        for j in range(DIT_SAMPLES):
            if RXpin.read_pin():
                num_high += 1
            time.sleep(duration)
            #timearr[index] = time.time()

        if num_high > DIT_SAMPLES/2:
            num_dits += 1
        else:
            num_dits = 0
            arr[index]=0
        index +=1
        if num_dits >= 8:# and not dits.isspace():
            #end of message
            #send message string to somewhere
            dlq.put(arr)
            # for i in range(1, len(timearr)):
            #     print(timearr[i]-timearr[i-1])
            break
    

def physicalTransmit(msg):
    with BlinkTX(15,"GPIO_22",direction="TX") as blink:
        clear = False
        while not clear:
            clear = True
            # for i in range(5):
            #     if blink.read_pin():
            #         clear = False
            #     time.sleep(DIT_TIME)
        print(msg)
        blink.blinkTX(0, DIT_TIME)
        blink(MorseTX(msg.upper()))


        
       
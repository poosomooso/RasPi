#
## Introducton to Python breadboarding - Receive Blinks
#
from  SetPin import SetPin
import time
import MorseCode
import threading
import queue
import array
import RPi.GPIO as GPIO
from BlinkTX import *
from options import *

#thread to read in, generates series of dits
#thread to translate
                
def detect_blinks(dlq ,duration=float(DIT_TIME)/DIT_SAMPLES):

    # class Recieve():
    #     def __init__(self):
    #         with SetPin(16,"GPIO_23",direction="RX") as RXpin:  
    #             self.arr = array.array('d')#, [0]*5000)
    #             self.start = time.time()
    #             self.begin = RXpin.read_pin()
    #             #self.index = 0
    #             GPIO.add_event_detect(RXpin.headerpin, GPIO.BOTH, callback=self.callback)
    #             while True:
    #                 pass

    #     def callback(self, channel):
    #         t = time.time()
    #         dt = t-self.start
    #         #self.arr[self.index] = dt
    #         self.arr.append(dt)
    #         self.start = t
    #         #self.index += 1

    #         if not GPIO.input(channel) and dt > DIT_TIME*8:
    #             print((self.arr[1], self.arr[2], self.arr[3]))
    #             # dlq.put((self.arr, self.begin))
    #             # self.arr = array.array('d')#, [0]*5000)
    #             # #self.index = 0
    #             # self.start = time.time()
    #             # self.begin = GPIO.input(channel)
                
    # Recieve()
    with SetPin(16,"GPIO_23",direction="RX") as RXpin:
        arr = array.array('d', [0]*5000)
        while True:
            if RXpin.read_pin():
                #Q.put('.')
                receive_blinks(RXpin, dlq, arr, duration)
                arr = array.array('d', [0]*5000)
            else:
                time.sleep(duration)


def receive_blinks(RXpin, dlq, arr, duration=float(DIT_TIME)/DIT_SAMPLES):
    #timearr = array.array('d', [0]*500)
    num_dits = 0
    index = 0
    start = time.time()
    read = RXpin.read_pin()
    begin = read
    while True:
        if RXpin.read_pin() == read:
            time.sleep(duration)
        else:
            t = time.time()
            read ^= 1
            arr[index] = t-start
            index += 1
            if not RXpin.read_pin() and t-start >= DIT_TIME*7.7:
                #print((arr[1], arr[2], arr[3]))
                dlq.put((arr, begin))
                # self.arr = array.array('d')#, [0]*5000)
                # #self.index = 0
                # self.start = time.time()
                # self.begin = GPIO.input(channel)
                break
            start = t

            #timearr[index] = time.time()

        # if num_high > DIT_SAMPLES/2:
        #     num_dits += 1
        # else:
        #     num_dits = 0
        #     arr[index]=0
        # index +=1
        # if index == len(arr):
        #     break;
        # if num_dits >= 8:# and not dits.isspace():
        #     #end of message
        #     #send message string to somewhere
        #     dlq.put(arr)
        #     # for i in range(1, len(timearr)):
        #     #     print(timearr[i]-timearr[i-1])
        #     break
    

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


        
       
#
## Introducton to Python breadboarding - Send Blinks
#
from SetPin import SetPin
import time                                                                                                                                                                                                                                                                                                                                                                                                                                                  

def sendblinks(TXpin,blinks=30,duration=1):
    for i in range(blinks):
            
        TXpin.turn_high()
        time.sleep(duration)
        TXpin.turn_low()
        time.sleep(duration)      

if __name__ == "__main__":

            
    with SetPin(15,"GPIO_22",direction="TX") as TXpin:
        sendblinks(TXpin)

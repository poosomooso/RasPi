#
# SetPin setup GPIO pin
#
import RPi.GPIO as GPIO
import time

class SetPin:
    def __init__(self,headerpin=16,BCM="GPIO_23",direction="RX"):
        
        if direction not in {"RX","TX"}:
            raise ValueError ("direction must be 'TX' or 'RX', not {}".direction)

        self.direction = direction

        if BOARD2BCM[headerpin] != BCM:
            raise ValueError(
                "Header pin {} does not correspond to BroadCom GPIO {}".format(headerpin, BCM))
       
        self.headerpin = headerpin
        self.BCM = BCM


        GPIO.setmode(GPIO.BOARD)  # use Pi Header numbers to address GPIO pins

        if self.direction == "TX":
            GPIO.setup(self.headerpin,GPIO.OUT)  # allow pin to read 3.3v and 0v levels
            
        else:
            self.direction == "RX"
            GPIO.setup(self.headerpin,GPIO.IN) # allow pin to set 3.3v and 0v levels
        

    def __enter__(self):
        print("Safe GPIO prepared")
        return self
    def __exit__(self,*rabc):
        GPIO.cleanup()
        print("Safe GPIO exit succeeded")
        return not any(rabc)

    def turn_high(self):
        if self.direction == "RX":
            raise PermissionError(
                "Pin {} (BCM {}) not opened for output".format(
                    self.headerpin,self.BCM))
        
        GPIO.output(self.headerpin,GPIO.HIGH)  # set 3.3V level on GPIO output
            
    def turn_low(self):
        if self.direction == "RX":
            raise PermissionError(
                "Pin {} (BCM {}) not opened for output".format(
                    self.headerpin,self.BCM))
        
        GPIO.output(self.headerpin,GPIO.LOW)   # set ground (0) level on GPIO output

    def read_pin(self):
        
        return GPIO.input(self.headerpin)  # read current headerpin voltage


    def __str__(self):
        return """\
Header pin number is {},
Broadcom device is {},
direction is  {}""".format(self.pin,self.BCM,self.in_out)


#
## RPi2 40 Pin Header Map from Header Pin to BroadCom I/O Device
#

BOARD2BCM = {
    1:"3.3V",
    2:"5v",
    3:"Dual Use: if I2C: SDA   if GPIO: GPIO_2",
    4:"5V",
    5:"Dual Use: if I2C: SDL   if GPIO: GPIO_3",
    6:"GND - Ground = 0V",
    7:"GPIO_4",
    8:"Dual Use: if UART: TXD   if GPIO: GPIO_14",
    9:"GND",
    10:"Dual Use: if UART: RXD   if GPIO: GPIO_15",
    11:"GPIO_17",
    12:"Dual Use: if PCM: CLK   if GPIO: GPIO_18",
    13:"GPIO_27",
    14:"GND",
    15:"GPIO_22",
    16:"GPIO_23",
    17:"3.3V",
    18:"GPRIO_24",
    19:"Dual Use: if SPI: MOSI   if GPIO: GPIO_10",
    20:"GND",
    21:"Dual Use: if SPI: MISO   if GPIO: GPIO_9",
    22:"GPIO_25",
    23:"Dual Use: if SPI: SCLK   if GPIO: GPIO_11",
    24:"Dual Use: if SPI: CE0    if GPIO: GPIO_8",
    25:"GND", 
    26:"Dual Use: if SPI: CE1    if GPIO: GPIO_7",
    27:"ID SD",
    28:"ID SC",
    29:"GPIO_5",
    30:"GND",
    31:"GPIO_6",
    32:"GPIO_12",
    33:"GPIO_13",
    34:"GND",
    35:"Dual Use: if PCM: FS    if GPIO: GPIO_19",
    36:"GPIO_16",
    37:"GPIO_26",
    38:"Dual Use: if PCM: DIN   if GPIO: GPIO_20",
    39:"GND",
    40:"Dual Use: if PCM: DOUT  if GPIO: GPIO_21"
    }


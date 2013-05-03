"""
Code to drive custom built UI using humble pi board. The UI currently
consists of a 16x2 LCD along with three buttons and three leds.
"""
import RPi.GPIO as GPIO
import time
import threading

# Using pins as simple GPIO

RED = 12 #(GPIO1)
YELLOW = 13 #(GPIO2)
GREEN = 15 #(GPIO3)
LED = {'red': 12,
       'yellow': 13,
       'green': 15
       }
SWITCH = [23,24,26]
#SWITCH1 = 23 #(SPI1)
#SWITCH2= 24 #(SPI0)
#SWITCH3 = 26 #(SCLK)

RS = 16 #(GPIO4)
E = 18 #(GPIO5)
D4 = 22 #(GPIO6)
D5 = 7 #(GPIO7)
D6 = 19 #(MOSI)
D7 = 21 #(MISO)

# LCD device constants. Change these for different display size.
WIDTH = 20    # Maximum characters per line
CHR = True
CMD = False
LINE = [0x80,0xC0,0x94,0xD4] # LCD RAM addresses
LINES = 4
# Update speed for display polling
DISPLAYSLEEP = 0.2

# Scrolling speed for display
SCROLL = 0.4

# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005

def write_pin(pin,value):
  GPIO.output(pin,value)

def switch(n):
  return GPIO.input(SWITCH[n])

def led(colour, value):
  GPIO.output(LED[colour], value)


def init():
  GPIO.setmode(GPIO.BOARD)       # Use BCM GPIO numbers. Should work across revisions

  for i in range(0,len(SWITCH)):
    GPIO.setup(SWITCH[i], GPIO.IN)  # 

  for k in LED.keys():
    GPIO.setup(LED[k], GPIO.OUT)  # RED

  GPIO.setup(E, GPIO.OUT)  # E
  GPIO.setup(RS, GPIO.OUT) # RS
  GPIO.setup(D4, GPIO.OUT) # DB4
  GPIO.setup(D5, GPIO.OUT) # DB5
  GPIO.setup(D6, GPIO.OUT) # DB6
  GPIO.setup(D7, GPIO.OUT) # DB7

  byte(0x33,CMD)
  byte(0x32,CMD)
  byte(0x28,CMD)
  byte(0x0C,CMD)  
  byte(0x06,CMD)
  byte(0x01,CMD)  

def display(message):
    # Send string to display
    message = message.ljust(WIDTH," ")  
    
    for i in range(WIDTH):
        byte(ord(message[i]),CHR)

def byte(bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = 1 for character
    #        0 for command

    write_pin(RS, mode) # RS
    
    # High bits
    write_pin(D4, False)
    write_pin(D5, False)
    write_pin(D6, False)
    write_pin(D7, False)
    if bits&0x10==0x10:
        write_pin(D4, True)
    if bits&0x20==0x20:
        write_pin(D5, True)
    if bits&0x40==0x40:
        write_pin(D6, True)
    if bits&0x80==0x80:
        write_pin(D7, True)

    # Toggle 'Enable' pin
    time.sleep(E_DELAY)    
    write_pin(E, True)  
    time.sleep(E_PULSE)
    write_pin(E, False)  
    time.sleep(E_DELAY)      

    # Low bits
    write_pin(D4, False)
    write_pin(D5, False)
    write_pin(D6, False)
    write_pin(D7, False)
    if bits&0x01==0x01:
        write_pin(D4, True)
    if bits&0x02==0x02:
        write_pin(D5, True)
    if bits&0x04==0x04:
        write_pin(D6, True)
    if bits&0x08==0x08:
        write_pin(D7, True)

    # Toggle 'Enable' pin
    time.sleep(E_DELAY)    
    write_pin(E, True)  
    time.sleep(E_PULSE)
    write_pin(E, False)  
    time.sleep(E_DELAY)   
  
def line(l, message):
#    print str(l) + ":" + message + "|"
    byte(LINE[l], CMD)
    display(message)

def scroll(l, message):
    message = (' ' * 16) + message
    while len(message) != 0:
        message = message[1:]
        line(l, message)
        time.sleep(SCROLL)

    
def main():
  """
  Test Code
  """
  hdt = HumbleDisplayThread(data)
  hdt.start()
  
  data.setLine(0,"Hello")
  data.setLed('red',False)
  data.setLed('green',False)
  data.setLed('yellow',False)
  while(True):
    if (switch(0)):
      data.setLine(0,"Switch 0 Pressed")
      for i in range(0,3):
        data.setLed('red',True)
        time.sleep(0.2)
        data.setLed('red',False)
        time.sleep(0.2)
    if (switch(1)):
      data.setLine(0,"Switch 1 Pressed")
      for i in range(0,3):
        data.setLed('green',True)
        time.sleep(0.2)
        data.setLed('green',False)
        time.sleep(0.2)
    if (switch(2)):
      data.setLine(0,"Switch 2 Pressed")
      for i in range(0,3):
        data.setLed('yellow', True)
        time.sleep(0.2)
        data.setLed('yellow',False)
        time.sleep(0.2)
    time.sleep(0.1)

class HumbleData():
  def __init__(self):
    self.line = ["","","",""]
    self.scroll = [False,False,False,False]
    self.led = {'red': False,
                'yellow': False,
                'green': False}
  def getLine(self,n):
    return self.line[n]

  def setLine(self,n,content):
    self.line[n] = content

  def getScroll(self,n):
    return self.scroll[n]

  def setScroll(self,n,value):
    self.scroll[n] = value

  def getLed(self,colour):
    return self.led[colour]

  def setLed(self,colour,value):
    self.led[colour] = value

data = HumbleData()

class HumbleDisplayThread(threading.Thread):
  def __init__(self, hd):
    threading.Thread.__init__(self)
    self.data = hd
    self.daemon = True
    self.carryOn = True

  def done(self):
      self.carryOn = False

  def run(self):
    while (self.carryOn):
      time.sleep(DISPLAYSLEEP)
      for i in range(LINES):
        if (self.data.getScroll(i)):
          scroll(i,self.data.getLine(i))
        else:
          line(i,self.data.getLine(i))
      for k in LED.keys():
        led(k,self.data.getLed(k))
      
if __name__ == '__main__':
  init()
  main()

"""
Code to drive custom built UI using humble pi board. The UI currently
consists of a 16x2 LCD along with two I2C connections and an led borg.
"""
import RPi.GPIO as GPIO
import time
import threading
from LedBorg import LedBorg

# Using pins as simple GPIO

RS = 12 #(GPIO4)
E = 16 #(GPIO5)
D4 = 18 #(GPIO6)
D5 = 22 #(GPIO7)
D6 = 24 #(MOSI)
D7 = 26 #(MISO)

# LCD device constants. Change these for different display size.
WIDTH = 20    # Maximum characters per line
CHR = True
CMD = False
LINE = [0x80,0xC0,0x94,0xD4] # LCD RAM addresses
LINES = 4
BIG = False
# Update speed for display polling
DISPLAYSLEEP = 0.2

# Scrolling speed for display
SCROLL = 0.4

# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005
lb = LedBorg()

def big():
  return BIG

def write_pin(pin,value):
  GPIO.output(pin,value)

def led(colour):
  lb.show(colour)

def init():
  GPIO.setwarnings(False) # Turn warnings off

  GPIO.setmode(GPIO.BOARD)       # Use BCM GPIO numbers. Should work across revisions
#  lb = LedBorg()

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
  data.setColour('black')
  while(True):
      data.setLine(0,"Red")
      data.setColour('red')
      time.sleep(1)
      data.setColour('black')
      time.sleep(0.5)
      data.setLine(0,"Green")
      data.setColour('green')
      time.sleep(1)
      data.setColour('black')
      time.sleep(0.5)
      data.setLine(0,"Blue")
      data.setColour('blue')
      time.sleep(1)
      data.setColour('black')
      time.sleep(0.5)

class HumbleData():
  def __init__(self):
    self.line = ["","","",""]
    self.scroll = [False,False,False,False]
    self.colour = 'black'

  def getLine(self,n):
    return self.line[n]

  def setLine(self,n,content):
    self.line[n] = content

  def getScroll(self,n):
    return self.scroll[n]

  def setScroll(self,n,value):
    self.scroll[n] = value

  def getColour(self):
    return self.colour

  def setColour(self,col):
    self.colour = col

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
#        print self.data.getLine(i)
      led(self.data.getColour())
      
if __name__ == '__main__':
  init()
  main()

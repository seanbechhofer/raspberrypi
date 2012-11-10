import RPi.GPIO as GPIO
import time

# BEGIN GPIO stuff
SWITCH1 = 26 #(SPI1)
SWITCH2= 24 #(SPI0)
SWITCH3 = 23 #(SCLK)

RS = 16
E = 18
D4 = 22
D5 = 7
D6 = 19
D7 = 21

# Define some device constants
WIDTH = 16    # Maximum characters per line
CHR = True
CMD = False

LINE1 = 0x80 # LCD RAM address for the 1st line
LINE2 = 0xC0 # LCD RAM address for the 2nd line 

SCROLL = 0.2

# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005

def write_pin(pin,value):
  GPIO.output(pin,value)

def readSwitch(sw):
  return GPIO.input(sw)

def init():
  GPIO.setmode(GPIO.BOARD)       # Use BCM GPIO numbers
  GPIO.setup(SWITCH1, GPIO.IN)  # 
  GPIO.setup(SWITCH2, GPIO.IN)  # 
  GPIO.setup(SWITCH3, GPIO.IN)  # 
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
    byte(l, CMD)
    display(message)

def scroll(l, message):
    message = (' ' * 16) + message
    while len(message) != 0:
        message = message[1:]
        line(l, message)
        time.sleep(SCROLL)

    


def main():
  line(LINE1,"Hello")
  while(True):
    if (readSwitch(SWITCH1)):
      line(LINE1,"1")
    if (readSwitch(SWITCH2)):
      line(LINE1,"2")
    if (readSwitch(SWITCH3)):
      line(LINE1,"3")
    time.sleep(0.1)
      

if __name__ == '__main__':
  init()
  main()

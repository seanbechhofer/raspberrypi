#!/usr/bin/python
#
# The wiring for the LCD is as follows:
#
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V**
# 16: LCD Backlight GND

#import
import piface.pfio as pfio
import time as time
import os

####### BEGIN Piface specific stuff #######

# Define output to LCD mapping. Don't use 1 and 2 as those are the
# relays (noisy)
RS = 3
E  = 4
D4 = 5 
D5 = 6
D6 = 7
D7 = 8

def interface_init():
    os.system("sudo modprobe spi_bcm2708")
    time.sleep(4)
    pfio.init()
    
# This is confusing. Writing a 1 to a pin via PiFace pulls the pin to
# ground, so the LCD sees it as a 0. So setting false actually
# requires us to write a 1 and true a 0
def write_pin(pin, value):
    if value:
        pfio.digital_write(pin, 0)
    else:
        pfio.digital_write(pin, 1)

####### END Piface specific stuff #######

# From here on it should be generic.         

# Define some device constants
WIDTH = 16    # Maximum characters per line
CHR = True
CMD = False

LINE1 = 0x80 # LCD RAM address for the 1st line
LINE2 = 0xC0 # LCD RAM address for the 2nd line 

SCROLL = 0.1

# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005

def init():
    interface_init()
    # Initialise display
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

def line1(message):
    byte(LINE1, CMD)
    display(message)

def line2(message):
    byte(LINE2, CMD)
    display(message)

def scroll(l, message):
    message = (' ' * 16) + message
    while len(message) != 0:
        line(l, message)
        time.sleep(SCROLL)
        message = message[1:]


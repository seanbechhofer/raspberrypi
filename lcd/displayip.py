#!/usr/bin/python
#
# HD44780 LCD Test Script for
# Raspberry Pi
#
# Author : Matt Hawkins
# Site   : http://www.raspberrypi-spy.co.uk
# 
# Date   : 26/07/2012
#

# The wiring for the LCD is as follows:
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
import datetime as datetime
import lcd as lcd
import subprocess

def main():
    # Main program block

    lcd.init()

    # Send some test
    lcd.line1("Raspberry Pi")
    lcd.line2("Model B")

    time.sleep(4) # delay

    # Send some text
    lcd.line1(datetime.datetime.now().strftime('%b %d  %H:%M:%S\n'))
    lcd.line2('%s' % ( getIP() ) )

def getIP():
    p = subprocess.Popen("ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1", shell=True, stdout=subprocess.PIPE)
    output = p.communicate()[0]
    return output[0:-1]
    
if __name__ == '__main__':
  main()

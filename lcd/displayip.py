#!/usr/bin/python
#
# HD44780 LCD driver script. Shows date/time and IP address.

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
    t = datetime.datetime.now().strftime('%b %d  %H:%M:%S')
    ip = '%s' % ( getIP() ) 
    lcd.line(lcd.LINE1,t)
    lcd.line(lcd.LINE2,ip)

    time.sleep(1)

    t = datetime.datetime.now().strftime('%b %d  %H:%M:%S')
    lcd.scroll(lcd.LINE1,t)
    t = datetime.datetime.now().strftime('%b %d  %H:%M:%S')
    lcd.line(lcd.LINE1,t)
    ip = '%s' % ( getIP() ) 
    lcd.scroll(lcd.LINE2,ip)
    ip = '%s' % ( getIP() ) 
    lcd.line(lcd.LINE2,ip)

def getIP():
    p = subprocess.Popen("ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1", shell=True, stdout=subprocess.PIPE)
    output = p.communicate()[0]
    return output[0:-1]
    
if __name__ == '__main__':
  main()

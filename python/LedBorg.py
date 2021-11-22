#!/usr/bin/env python
import time
import sys
import RPi.GPIO as GPIO
#GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# 11, 13, 15
# 17,21/27,22

BCM=False

# Set which GPIO pins the LED outputs are connected to
LED_RED = 11
LED_GREEN = 13
LED_BLUE = 15

if BCM:
    LED_RED = 17
    if GPIO.RPI_REVISION == 1:
        LED_GREEN = 21                      # Rev 1 boards
    else:
        LED_GREEN = 27                      # Rev 2 boards
    LED_BLUE = 22

# Set all of the LED pins as output pins
GPIO.setup(LED_RED, GPIO.OUT)
GPIO.setup(LED_GREEN, GPIO.OUT)
GPIO.setup(LED_BLUE, GPIO.OUT)


class LedBorg:
    
    colours = {"maroon":"100",
               "red":"200",
               "pink":"211",
               "olive":"110",
               "yellow":"220",
               "lightyellow":"221",
               "green":"010",
               "limegreen":"020",
               "lightgreen":"121",
               "teal":"011",
               "cyan":"022",
               "lightcyan":"122",
               "navy":"001",
               "blue":"002",
               "lightblue":"112",
               "purple":"101",
               "magenta":"202",
               "fuchsiapink":"212",
               "black":"000",
               "grey":"111",
               "white":"222",
               "azure":"012",
               "violet":"102",
               "brightpink":"201",
               "chartreuse":"120",
               "guppiegreen":"021",
               "orange":"210"}

    def show(self,name="red"):

        # Determine the pin levels
        red = GPIO.LOW
        green = GPIO.LOW
        blue = GPIO.LOW
        colour = self.colours[name]
        if len(colour) > 0:
            if colour[0] == '1' or colour[0] == '2':
                red = GPIO.HIGH
        if len(colour) > 1:
            if colour[1] == '1' or colour[1] == '2':
                green = GPIO.HIGH
        if len(colour) > 2:
            if colour[2] == '1' or colour[2] == '2':
                blue = GPIO.HIGH
 
        # Apply the pin levels to the correct pins
        GPIO.output(LED_RED, red)
        GPIO.output(LED_GREEN, green)
        GPIO.output(LED_BLUE, blue)

        # """Show the given colour"""
        # # Open the LedBorg driver
        # dev = open('/dev/ledborg', 'w')
        # # Set LedBorg to the new colour
        # dev.write(self.colours[colour])
        # # Close
        # dev.close()                    

if __name__ == "__main__":
    lb = LedBorg()
    while True:
        for colour in lb.colours:
            print colour
            lb.show(colour)
            time.sleep(10)


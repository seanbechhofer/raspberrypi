#!/usr/bin/env python
# coding: Latin-1

# code taken from the cheerlights.com website.

# Load library functions we want
import time
import urllib

# Setup paramters
cheerlightsUrl = "http://api.thingspeak.com/channels/1417/field/1/last.txt"
colourMap = {"red":"200",
             "green":"020",
             "blue":"002",
             "cyan":"022",
             "white":"111",
             "warmwhite":"222",
             "purple":"102",
             "magenta":"202",
             "yellow":"220",
             "orange":"210"}

# Loop indefinitely
while True:
    try:                                                # Attempt the following:
        cheerlights = urllib.urlopen(cheerlightsUrl)        # Open cheerlights file via URL
        colourName = cheerlights.read()                     # Read the last cheerlights colour
        cheerlights.close()                                 # Close cheerlights file
        if colourMap.has_key(colourName):                   # If we recognise this colour name then ...
            ledBorgColour = colourMap[colourName]               # Get the LedBorg colour to use from the name
        else:                                               # Otherwise ...
            print "Unexpected colour '" + colourName + "'"      # Display the name we did not recognise
            ledBorgColour = "000"                               # Use the colour of black / off
        ledBorg = open('/dev/ledborg', 'w')                 # Open the LedBorg driver
        ledBorg.write(ledBorgColour)                        # Set LedBorg to the new colour
        ledBorg.close()                                     # Close the LedBorg driver
    except:                                             # If we have an error
        pass                                                # Ignore it (do nothing)
    finally:                                            # Regardless of errors:
        time.sleep(1)                                       # Wait for 1 second 

#!/usr/bin/env python

# this file is run using this command: "sudo python radio.py"
# python must be installed, and you must call the command while
# you are in the same folder as the file

from time import sleep
import subprocess
import os
import signal
import humble
import subprocess

def showPaused():
    humble.line(humble.LINE1, chr(0xf7) + "Player [" + chr(0xdb) + "]" )

def showPlaying():
    humble.line(humble.LINE1, chr(0xf7) + "Player [>]")
    
os.system("sudo modprobe spi_bcm2708")

humble.init()
showPaused()
stations = [
            ['6 Music','http://www.bbc.co.uk/radio/listen/live/r6_aaclca.pls'],
            ['Radio 2','http://www.bbc.co.uk/radio/listen/live/r2_aaclca.pls'],
            ['Radio 4','http://www.bbc.co.uk/radio/listen/live/r4_aaclca.pls'],
            ['5 Live','http://www.bbc.co.uk/radio/listen/live/r5l_aaclca.pls'],
            ['Radio 4 Extra','http://www.bbc.co.uk/radio/listen/live/r4x_aaclca.pls'],
            ['Planet Rock', 'http://tx.sharp-stream.com/icecast.php?i=planetrock.mp3']
           ]


print "piPlayer"

# make sure the audio card is started, as well as MPD

currentstation = 0
humble.line(humble.LINE2, stations[currentstation][0])

playing = False

# main loop, looking for button presses
# this looks more complicated because the loop will me fast, this way 
# when you press the buttons it only move one station until you release the button
while(True):
    if (humble.readSwitch(humble.SWITCH1)):
        if (not playing):
            print "Now Playing: " + stations[currentstation][0]
            showPlaying()
            humble.line(humble.LINE2, stations[currentstation][0])
            proc = subprocess.Popen("mplayer -quiet " + stations[currentstation][1], 
#                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True,
                                preexec_fn=os.setsid)
            playing = True
            sleep(0.5)
        else:
            showPaused()
            #humble.line(humble.LINE2, "")
            os.killpg(proc.pid, signal.SIGTERM)
            playing = False
            sleep(0.5)
    if (playing and humble.readSwitch(humble.SWITCH2)):
        os.killpg(proc.pid, signal.SIGTERM)
        currentstation = (currentstation + 1) % len(stations) 
        print "Now Playing: " + stations[currentstation][0]
        humble.line(humble.LINE2, stations[currentstation][0])
        proc = subprocess.Popen("mplayer -quiet " + stations[currentstation][1], 
#                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True,
                                preexec_fn=os.setsid)
        sleep(0.5)
    if (humble.readSwitch(humble.SWITCH3)):
        if (playing):
            os.killpg(proc.pid, signal.SIGTERM)
        humble.line(humble.LINE2, "")
        humble.scroll(humble.LINE2, "Shutting Down...")
        humble.line(humble.LINE2, "Shutting Down...")
        humble.line(humble.LINE1, "")
        humble.line(humble.LINE2, "")
        os.system("sudo halt")
# # this is never hit, but should be here to indicate if you plan on leaving the main loop
print "done"


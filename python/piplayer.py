#!/usr/bin/env python
"""
PiPlayer radio. Plays radio streams from a list of stations. 
Run using this command: "sudo python piplayer.py"
Controlled by buttons: 
1: Start/Stop
2: Change Station
3: Shut Down. Shuts down the pi!
"""

from time import sleep
import subprocess
import os
import signal
import humble
import subprocess

def showPaused():
    humble.line(0, chr(0xf7) + "Player [" + chr(0xdb) + "]" )

def showPlaying():
    humble.line(0, chr(0xf7) + "Player [>]")

def main():    
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
    
    currentstation = 0
    humble.line(1, stations[currentstation][0])
    
    playing = False

    # main loop, looking for button presses
    carryOn = True
    while(carryOn):
        if (humble.switch(0)):
            if (not playing):
                print "Now Playing: " + stations[currentstation][0]
                showPlaying()
                humble.line(1, stations[currentstation][0])
                proc = subprocess.Popen("mplayer -quiet " + stations[currentstation][1], 
                                        #                                stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        shell=True,
                                        preexec_fn=os.setsid)
                playing = True
                sleep(0.5)
            else:
                showPaused()
            #humble.line(1, "")
                os.killpg(proc.pid, signal.SIGTERM)
                playing = False
                sleep(0.5)
        if (playing and humble.switch(1)):
            os.killpg(proc.pid, signal.SIGTERM)
            currentstation = (currentstation + 1) % len(stations) 
            print "Now Playing: " + stations[currentstation][0]
            humble.line(1, stations[currentstation][0])
            proc = subprocess.Popen("mplayer -quiet " + stations[currentstation][1], 
                                    #                            stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    shell=True,
                                    preexec_fn=os.setsid)
            sleep(0.5)
        if (humble.switch(2)):
            if (playing):
                os.killpg(proc.pid, signal.SIGTERM)
            humble.line(0, "")
            humble.line(1, "")
            carryOn = False
#               os.system("sudo halt")

if __name__ == '__main__':
  main()

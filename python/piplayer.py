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
import urllib, os
from bs4 import BeautifulSoup

currentstation = 0
stationInfo = True
stations = [
        ['6 Music','http://www.bbc.co.uk/radio/listen/live/r6_aaclca.pls',
         'http://www.bbc.co.uk/radio/player/bbc_6music'],
        ['Radio 2','http://www.bbc.co.uk/radio/listen/live/r2_aaclca.pls'],
        ['Radio 4','http://www.bbc.co.uk/radio/listen/live/r4_aaclca.pls'],
        ['5 Live','http://www.bbc.co.uk/radio/listen/live/r5l_aaclca.pls'],
        ['Radio 4 Extra','http://www.bbc.co.uk/radio/listen/live/r4x_aaclca.pls'],
        ['Planet Rock', 'http://tx.sharp-stream.com/icecast.php?i=planetrock.mp3']
        ]

BIGDISPLAY = True

def showPaused():
    humble.data.setLine(0, chr(0xf7) + "Player [" + chr(0xdb) + "]" )
    humble.data.setLed('green',False)
    humble.data.setLed('red',False)
    humble.data.setLed('yellow',True)

def showPlaying():
    humble.data.setLine(0, chr(0xf7) + "Player [>]")
    humble.data.setLed('green',True)
    humble.data.setLed('red',False)
    humble.data.setLed('yellow',False)

def nowPlaying():
    global currentstation
    global stationInfo
    global stations
    print "NOWPLAYING"

    if currentstation==0:
        f = urllib.urlopen('http://www.bbc.co.uk/radio/player/bbc_6music')
        stuff = f.read()
        soup = BeautifulSoup(stuff)
        for div in soup.find_all('div'):
            if (div.attrs.has_key('id') and ('now-playing' in div['id']) ):
                artist = div.find(id='artists').get_text().lstrip().rstrip()
                track = div.find(id='track').get_text().lstrip().rstrip()
            if (div.attrs.has_key('id') and ('title' in div['id']) ):
                title = div.get_text().lstrip().rstrip()
            if (div.attrs.has_key('id') and ('description' in div['id']) ):
                description = div.get_text().lstrip().rstrip()

        nowplaying = "Now Playing: " + track + " by " + artist

    if BIGDISPLAY:
        humble.data.setLine(1,stations[currentstation][0])
        print "BIG"
        print nowplaying
        humble.data.setLine(2,nowplaying)
        humble.data.setScroll(2,True)
    else:
        print stationInfo
        if stationInfo:
        #humble.data.setLine(1,stations[currentstation])
            humble.data.setLine(1,stations[currentstation][0])
            humble.data.setScroll(1,False)
        else:
            if currentstation==0:
                humble.data.setLine(1, nowplaying)
                humble.data.setScroll(1,True)
        stationInfo = not stationInfo

def main():
    humble.init()
    hdt = humble.HumbleDisplayThread(humble.data)
    hdt.start()
    doStuff()
    hdt.done()

def doStuff():    
    global currentstation
    global stations
#    humble.init()
    showPaused()
    
    print "piPlayer"
    
    currentstation = 0
    humble.data.setLine(1, stations[currentstation][0])
    humble.data.setScroll(1,False)

    playing = False

    # main loop, looking for button presses
    carryOn = True
    loops = 0
    while(carryOn):
        loops = loops + 1
        if loops > 50000:
            if playing:
                nowPlaying()
            loops = 0
        if (humble.switch(0)):
            if (not playing):
                print "Now Playing: " + stations[currentstation][0]
                showPlaying()
                humble.data.setLine(1, stations[currentstation][0])
                humble.data.setScroll(1,False)
                proc = subprocess.Popen("mplayer -quiet " + stations[currentstation][1], 
                                        #                                stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        shell=True,
                                        preexec_fn=os.setsid)
                playing = True
                sleep(0.5)
            else:
                showPaused()
            #humble.data.setLine(1, "")
                os.killpg(proc.pid, signal.SIGTERM)
                playing = False
                sleep(0.5)
        if (playing and humble.switch(1)):
            os.killpg(proc.pid, signal.SIGTERM)
            currentstation = (currentstation + 1) % len(stations) 
            print "Now Playing: " + stations[currentstation][0]
            humble.data.setLine(1, stations[currentstation][0])
            humble.data.setScroll(1,False)
            proc = subprocess.Popen("mplayer -quiet " + stations[currentstation][1], 
                                    #                            stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    shell=True,
                                    preexec_fn=os.setsid)
            sleep(0.5)
        if (humble.switch(2)):
            if (playing):
                os.killpg(proc.pid, signal.SIGTERM)
            humble.data.setLine(0, "")
            humble.data.setLine(1, "")
            humble.data.setScroll(1,False)
            carryOn = False
#               os.system("sudo halt")

if __name__ == '__main__':
  main()

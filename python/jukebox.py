#!/usr/bin/env python
#
import sys, os, random, time, signal
import subprocess
import humble
import threading
from mpd import (MPDClient, CommandError)
from socket import error as SocketError


# MPD Stuff
HOST = 'localhost'
PORT = '6600'
CON_ID = {'host':HOST, 'port':PORT}

PAUSE = 0.2
DISPLAYSLEEP = 5


# Some functions
def mpdConnect(client, con_id):
    """
    Simple wrapper to connect MPD.
    """
    try:
        client.connect(**con_id)
    except SocketError:
        return False
    return True

class DisplayThread(threading.Thread):
  def __init__(self, jb):
    threading.Thread.__init__(self)
    self.jukebox = jb
    self.daemon = True
    self.carryOn = True

  def done(self):
      self.carryOn = False

  def run(self):
    while (self.carryOn):
        time.sleep(DISPLAYSLEEP)
        status = self.jukebox.client.status()
#        print status
        info = self.jukebox.client.currentsong()
        if status['state'] == 'pause' or status['state'] == 'stop':
            humble.data.setLed('red',True)
            humble.data.setLed('yellow',False)
            humble.data.setLed('green',False)
        else:
            humble.data.setLed('red',False)
            humble.data.setLed('yellow',False)
            humble.data.setLed('green',True)
        try:
            artist = info['artist']
        except KeyError:
            artist = ""
        try:
            title = info['title']
        except KeyError:
            title  = ""
        humble.data.setLine(0,artist)
        if (len(title) >= 16):
            humble.data.setScroll(1,True)
            humble.data.setLine(1,title)
        else:
            humble.data.setScroll(1,False)
            humble.data.setLine(1,title)
        
class Jukebox():
  def __init__(self):
    self.dt = DisplayThread(self)
    self.dt.start()

    ## MPD object instance
    self.client = MPDClient()
    if mpdConnect(self.client, CON_ID):
        print 'Got connected!'
    else:
        print 'fail to connect MPD server.'
        sys.exit(1)
    try:
        f = open('/media/usb/playlist.txt','r')
        playlist = f.readline().rstrip()
        print "Loading " + playlist
        self.client.clear()
        self.client.load(playlist)
    except IOError:
        print "Problem reading playlist"
    self.client.stop()
    self.client.play()

    carryOn = True
    while (carryOn):
        if (humble.switch(0)):
            time.sleep(PAUSE)
            self.toggle()
        if (humble.switch(1)):
            time.sleep(PAUSE)
            self.skip()
        if (humble.switch(2)):
            time.sleep(PAUSE)
            self.stop()
            carryOn = False
            time.sleep(PAUSE)
    # Stop the display thread
    self.dt.done()
    

  def skip(self):
      print "Skipping"
      self.client.next()

  def stop(self):
      print "Stopping"
      self.client.stop()
      humble.data.setLine(0,"")
      humble.data.setLine(1,"")
      humble.data.setLed('red', False)
      humble.data.setLed('green', False)
      time.sleep(0.5)

  def toggle(self):
      status = self.client.status()
      if status['state'] == 'pause' or status['state'] == 'stop':
          self.client.play()
      else:
          self.client.pause()

def main():
    humble.init()
    hdt = humble.HumbleDisplayThread(humble.data)
    hdt.start()
    time.sleep(0.5)
    doStuff()
    hdt.done()
    
def doStuff():
    jb = Jukebox()
    
if __name__ == '__main__':
  main()

#!/usr/bin/env python
"""
Code that allows selection of varios functions on boot.
SWITCH1 = Radio
SWITCH2 = Trains
"""

import humble
import piplayer
import trains
import time
import os

def main():
    humble.init()
    humble.line(0,"Select Function")
    humble.line(1,"1:Radio;2:Trains")
    while (True):
        if humble.switch(0):
            time.sleep(0.2)
            piplayer.main()
            humble.line(0,"Select Function")
            humble.line(1,"1:Radio;2:Trains")
            time.sleep(0.2)
        if humble.switch(1):
            time.sleep(0.1)
            trains.main()
            humble.line(0,"Select Function")
            humble.line(1,"1:Radio;2:Trains")
            time.sleep(0.2)
        if humble.switch(2):
            humble.scroll(0, "Shutting Down...")
            humble.line(0, "Shutting Down...")
            humble.line(1, "")
            os.system("sudo halt")

        time.sleep(0.1)
    
if __name__ == '__main__':
  main()

#!/usr/bin/python
import humbleII as humble
import time
from subprocess import *
from time import sleep, strftime
from datetime import datetime
 
time.sleep(5)

humble.init()
 
#cmd = "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"
cmd = "hostname -I"

def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

while True:
    ipaddr = run_cmd(cmd)
    humble.line(0,datetime.now().strftime('%b %d  %H:%M:%S\n'))
    humble.line(1,'%s' % ( ipaddr ) )
    sleep(2)
    

#!/usr/bin/python
import urllib, os
from bs4 import BeautifulSoup
import re
import humbleII as humble
import time
import datetime
import argparse
import json
import unicodedata

# Pattern for ldb information
LDB = 'http://ojp.nationalrail.co.uk/service/ldbboard/dep/{dep}/{arr}/To'

CONFIG={
    'dep': 'MAN',
    'arr': 'HTC',
    'speak': False,
    'led':True,
    'big':False,
    'announcetwo':False
}


st = open("stations.json")
STATIONS = json.load(st)
st.close()

STATUS={
    'goMessage':"",
    'bestTime':""
}

DELAY = 4
CYCLES = 5
#CYCLES = 15
NEXT = 2

FORMAT = '{time:<5} {dest:<3} {estimate:<5}'
BIGFORMATHEADER = '  {dep:<3} to {arr:<3}   {h:<2}:{m:<2}'
BIGFORMAT1 = '{num:<1}){dest}'
BIGFORMAT2 = '         {time:<5} {estimate:<5}'
BIGFORMAT3 = '{num:<1}){dest:<6} {time:<5} {estimate:<5}'

# Configuration for timings.

# How long it takes to walk to station
WALKING = 12
# How long you're prepared to wait
WAITING = 10
# Danger margin
DANGER = 3

def green():
    global goMessage
    humble.data.setColour('green')
    print "Green"
    STATUS['goMessage'] = "You can go now"

def amber():
    global goMessage
    humble.data.setColour('orange')
    print "Amber"
    STATUS['goMessage'] = "You should go now"

def red():
    global goMessage
    humble.data.setColour('red')
    print "Red"
    STATUS['goMessage'] = "You should wait"

def off():
    global goMessage
    humble.data.setColour('black')
    print "Off"
    STATUS.goMesssage = ""

def lights(now, times):
    if CONFIG['led']:
        # status(g,y)
        greenLight = False
        amberLight = False
        # If it's the case that any train yields green, then show green. Same for amber. 
        for i in range (0,len(times)):
            togo = times[i] - now
            
            print str(togo) + " Minutes"
            if (togo) > (WAITING + WALKING):
                pass
            elif (togo) > (DANGER + WALKING):
                greenLight = True
            elif (togo) > WALKING:
                amberLight = True
            else:
                pass

        if (greenLight):
            green()
        elif (amberLight):
            amber()
        else:
            red()

def shorten(station):
    if STATIONS.has_key(station):
        return STATIONS[station]
    else:
        return station[:3]

# Strip out the table of train times. Relies on knowing where the table occurs. 
def getTrains(soup):
    trains = []
    for div in soup.find_all('div'):
        if (div.attrs.has_key('class') and ("tbl-cont" in div['class']) ):
            body = div.table.tbody
            rows = body.find_all('tr')
            for r in range(0,len(rows)):
                row = rows[r]
                cells = row.find_all('td')
                train = {}
                train['time'] = cells[0].contents[0].strip().encode('ascii','replace')
                train['dest'] = cells[1].contents[0].strip().encode('ascii','replace')
                # Collapse all white space
                train['dest'] = re.sub(r"\s+", ' ', train['dest']).encode('ascii','replace')
                train['report'] = cells[2].contents[0].strip().encode('ascii','replace')
                print train['report']
                if re.match('[0-9][0-9]:[0-9][0-9]',train['report']):
                    train['est'] = train['report']
                else:
                    train['est'] = ""
                trains.append(train)
    return trains

def announce(trains):
    if CONFIG['speak']:
        now = datetime.datetime.now()
        nowH = now.strftime('%H')
        nowM = now.strftime('%M')
        timeMessage = 'The time is {h}:{m}'.format(h=nowH,m=nowM)
        print timeMessage
        toSpeak = timeMessage
#        os.system("echo '%s' | festival --tts" % timeMessage)

        if trains[0]['est'] == "":
            message = 'The next train is at %s' % trains[0]['time']
        else:
            message = 'The next train is scheduled at %s, estimated at %s' % (trains[0]['time'],trains[0]['est'])
        print message
        toSpeak = toSpeak + ". " + message
#        os.system("echo '%s' | festival --tts" % message)

        if CONFIG['announcetwo']:
            if trains[1]['est'] == "":
                message = 'The train after is at %s' % trains[1]['time']
            else:
                message = 'The train after is scheduled at %s, estimated at %s' % (trains[1]['time'],trains[1]['est'])
            print message
            toSpeak = toSpeak + ". " + message
#            os.system("echo '%s' | festival --tts" % message)

        print STATUS['goMessage']
        toSpeak = toSpeak + ". " + STATUS['goMessage']
#        os.system("echo '%s' | festival --tts" % STATUS['goMessage'])
        os.system("echo '%s' | festival --tts" % toSpeak)
        

# Pretty print details
def printTrains(trains):
    destLength = 40
    printFormat = ' {time:<6}| {estimate:<6}| {dest:<' + str(destLength) + '}| {report:<20}'
    printFormat = '{time:<5} {dest:<' + str(destLength) + '} {estimate:<5}'
    print printFormat.format(time="Time",
                             dest="To",
                             estimate="Est",
                             report="Report")
    print "======================"
#    print "12345678901234567890"
    for train in trains:
        print printFormat.format(time=train['time'],
                                 dest=train['dest'][:destLength],
                                 estimate=train['est'],
                                 report=train['report'])
    print "======================"

def checkForShutDown():
    if (humble.switch(2)):
        humble.data.setLine(0, "")
        humble.data.setLine(1, "")
        if CONFIG['big']:
            humble.data.setLine(2, "")
            humble.data.setLine(3, "")
        off()
        return True
    return False
#        os.system("sudo halt")

def reportTrains(trains):
    train = trains[0]
    if (CONFIG['big']):
        humble.data.setLine(1,BIGFORMAT1.format(num="1",
                                     time=train['time'],
                                     dest=train['dest'],
                                     estimate=train['est'],
                                     report=train['report']))
        humble.data.setLine(2,BIGFORMAT2.format(num="1",
                                        time=train['time'],
                                        dest=train['dest'],
                                        estimate=train['est'],
                                        report=train['report']))
    else:
        humble.data.setLine(0,FORMAT.format(num="1",
                                    time=train['time'],
                                    dest=shorten(train['dest']),
                                    estimate=train['est'],
                                    report=train['report']))
    times = []
    for i in range(0,NEXT):
        if i < len(trains):
            trainTime = trains[i]['time']
            if (trains[i]['est'] != ""):
                trainTime = trains[i]['est']
            trainH = int(trainTime[0:2])
            trainM = int(trainTime[3:5])
            if (trainH == 0):
                trainH = 24
            trainMinutes = trainH*60 + trainM
            times.append(trainMinutes)

    for i in range(0,CYCLES):
#        announce(trains)
        now = datetime.datetime.now()
        print now
        nowH = int(now.strftime('%H'))
        nowM = int(now.strftime('%M'))
        if (CONFIG['big']):
            humble.data.setLine(0,BIGFORMATHEADER.format(h=now.strftime('%H'),
                                                 m=now.strftime('%M'),
                                                 dep=CONFIG['dep'],
                                                 arr=CONFIG['arr']))
        if (nowH == 0):
            nowH = 24
        nowMinutes = nowH*60 + nowM
        lights(nowMinutes, times)
        for j in range(1,NEXT+1):
            if j < len(trains):
                train = trains[j]
                if (CONFIG['big']):
                    humble.data.setLine(3,BIGFORMAT3.format(num=str(j+1),
                                                    time=train['time'],
                                                    #dest=shorten(train['dest']),
                                                    # This isn't ideal as it depends on the format
                                                    dest=train['dest'][:6],
                                                    estimate=train['est'],
                                                    report=train['report']))
                else:
                    humble.data.setLine(1,FORMAT.format(num=str(j+1),
                                                time=train['time'],
                                                dest=shorten(train['dest']),
                                                estimate=train['est'],
                                                report=train['report']))
                # if checkForShutDown():
                #     return False
                time.sleep(DELAY)
    return True

def main():    
    global CONFIG

    parser = argparse.ArgumentParser(description='Live Train Times')
    parser.add_argument('-s','--speak', action='store_true', default=False,
                        dest='speak',
                        help='Announce times')
    parser.add_argument('-l','--led', action='store_true', default=False,
                        dest='led',
                        help='Coloured Lights')
    parser.add_argument('-d','--dep', help='Departure', default="HTC")
    parser.add_argument('-a','--arr', help='Arrival', default="MAN")
    parser.add_argument('-b','--big', action='store_true', default=False,
                        dest='big',
                        help='Big Display', )
    args = parser.parse_args()

    CONFIG['speak'] = args.speak
    CONFIG['led'] = args.led
    CONFIG['dep'] = args.dep
    CONFIG['arr'] = args.arr
    CONFIG['big']= args.big

    if CONFIG['big']:
        print "Big Display"
    if CONFIG['speak']:
        print "Announcing"
    if CONFIG['led']:
        print "Lights"
    print LDB.format(dep=CONFIG['dep'],arr=CONFIG['arr'])
    humble.init()
    hdt = humble.HumbleDisplayThread(humble.data)
    hdt.start()
    doStuff()
    hdt.done()

def doStuff():
    carryOn = True
    while(carryOn):
        f = urllib.urlopen(LDB.format(dep=CONFIG['dep'],arr=CONFIG['arr']))
        stuff = f.read()
        o = open('tmp.html','w')
        o.write(stuff)
        soup = BeautifulSoup(stuff)
        trains = getTrains(soup)
        printTrains(trains)
        announce(trains)
        carryOn = reportTrains(trains)
    time.sleep(0.5)

if __name__ == '__main__':
  main()

#!/usr/bin/python
from TSL2561 import TSL2561
from BMP085 import BMP085
import thingspeak
import time, datetime
import humbleII as humble
import LedBorg
import argparse
import sqlite3
import mytempodb
import tweety
import whereami

tsl = TSL2561()
bmp = BMP085()
flipflop = True
lastTweet = {
    "temperature": datetime.datetime(2014,1,1,0,0,0),
    "lux": datetime.datetime(2014,1,1,0,0,0)}

#LOCATION = whereami.whereAmI()
LOCATION="Manchester"

# Parameters controlling tweeting behaviour

TWEET={
    "cold":0,
    "hot":35,
    "dark":5,
    "bright":30000,
    "cycle":30,
    "tweet":1200
}

# Cycle period in seconds
WAIT = 5

# Wait time before updating to thingspeak. Tempo-db has no restrictions.
THROTTLE = 60

# Temperatures and colours

COLD = 14
COOL = 16
OK = 22
WARM = 28
HOT = 30
TOASTY = 35

colours = {
    COLD: "blue",
    COOL: "lightblue",
    OK: "yellow",
    WARM: "green",
    HOT: "orange",
    TOASTY: "red"
    }

def hms(datetime):
    '''Format a date'''
    return datetime.strftime('%H:%M:%S')

def publishTempo(data,verbose=False):
    '''Publish to Tempo-DB'''
    timestamp=datetime.datetime.now()
    mytempodb.write("pi.lux",timestamp,data['field1'])
    mytempodb.write("pi.temperature",timestamp,data['field2'])
    mytempodb.write("pi.pressure",timestamp,data['field3'])
    if verbose:
        print "Published to tempo-db", hms(timestamp)

def publishThingSpeak(data,verbose=False):
    '''Publish to Thingspeak'''
    timestamp=datetime.datetime.now()
    thingspeak.log(data,verbose)
    if verbose:
        print "Published to thingspeak", hms(timestamp)

def store(db,lux,temperature,pressure,verbose=False):
    '''store locally'''
    conn = sqlite3.connect(db) # or use :memory: to put it in RAM
    cursor = conn.cursor()
    cursor.execute("INSERT INTO data (lux,temperature,pressure) VALUES ("+str(lux)+","+str(temperature)+","+str(pressure)+")")
    conn.commit()
    if verbose:
        print "Logged to ", db
    
def report(lux,temperature,pressure):
    '''Report information to display'''
    global flipflop
    now=datetime.datetime.now()
    humble.data.setLine(0,('T:{t:>6}'+chr(0xdf)+'C {d:<5}').format(t=temperature,d=now.strftime('%H:%M')))
    if (flipflop):
        humble.data.setLine(1,'P:{t:>6}mb {d:<5}'.format(t=pressure,d=now.strftime('%d/%m')))
    else:
        humble.data.setLine(1,'L:{l:>6}lx {d:<5}'.format(l=lux,d=now.strftime('%d/%m')))
    flipflop = not flipflop

def tweet(lux,temperature):
    '''Tweet if certain conditions are met'''
    message = None
    now=datetime.datetime.now()
    if temperature <= TWEET["cold"]:
        if (now - lastTweet["temperature"]).seconds > TWEET["cycle"]:
            message = ((now.strftime('%H:%M') + " and Freezing! {t:<4}" + u'\u00b0' + "C").format(t=temperature))
            lastTweet["temperature"] = now
    if temperature > TWEET["hot"]:
        if (now - lastTweet["temperature"]).seconds > TWEET["cycle"]:
            message = ((now.strftime('%H:%M') + " and Hot Hot Hot! {t:<4}"+ u'\u00b0' + "C").format(t=temperature))
            lastTweet["temperature"] = now
    if (now - lastTweet["temperature"]).seconds > TWEET["tweet"]:
        if temperature <= TWEET["cold"]:
            message = ((now.strftime('%H:%M') + " and Freezing! {t:<4}" + u'\u00b0' + "C").format(t=temperature))
            lastTweet["temperature"] = now
        elif temperature > TWEET["hot"]:
            message = ((now.strftime('%H:%M') + " and Hot Hot Hot! {t:<4}" + u'\u00b0' + "C").format(t=temperature))
            lastTweet["temperature"] = now
        else:
            message = ((now.strftime('%H:%M') + " and {t:<4}" + u'\u00b0' + "C").format(t=temperature))
            lastTweet["temperature"] = now

    if lux <= TWEET["dark"]:
        if (now - lastTweet["lux"]).seconds > TWEET["cycle"]:
            message = (now.strftime('%H:%M') + " and dark!")
            lastTweet["lux"] = now
    if lux > TWEET["bright"]:
        if (now - lastTweet["lux"]).seconds > TWEET["cycle"]:
            message = (now.strftime('%H:%M') + " Bright Light!")
            lastTweet["lux"] = now
    if (now - lastTweet["lux"]).seconds > TWEET["tweet"]:
        if lux <= TWEET["dark"]:
            message = (now.strftime('%H:%M') + " and dark!")
            lastTweet["lux"] = now
        elif lux > TWEET["bright"]:
            message = (now.strftime('%H:%M') + " Bright Light!")
            lastTweet["lux"] = now
    if message:
        message = "In " + LOCATION['city'] + ", " + LOCATION['country_name'] + " it's " + message
        #print "Tweeting: ", message

        tweety.tweet(message)

def colour(temperature):
    '''Map temperatures to colours'''
    if temperature <= COLD:
        humble.data.setColour(colours[COLD])
    elif temperature <= COOL:
        humble.data.setColour(colours[COOL])          
    elif temperature <= OK:
        humble.data.setColour(colours[OK])          
    elif temperature <= WARM:
        humble.data.setColour(colours[WARM])          
    elif temperature <= HOT:
        humble.data.setColour(colours[HOT])          
    else:
        humble.data.setColour(colours[TOASTY]) 

def main():
    '''Main loop'''
    parser = argparse.ArgumentParser(description='Log and display sensor data')
    parser.add_argument('-d','--lcd', action='store_true', default=False,
                        dest='lcd',
                        help='log to LCD')
    parser.add_argument('-l','--led', action='store_true', default=False,
                        dest='led',
                        help='log to LED')
    parser.add_argument('-t','--tweet', action='store_true', default=False,
                        dest='tweet',
                        help='Tweet')
    parser.add_argument('--thingspeak', action='store_true', default=False,
                        dest='thingspeak',
                        help='publish to thingspeak')
    parser.add_argument('--tempo', action='store_true', default=False,
                        dest='tempo',
                        help='publish to tempo-db')
    parser.add_argument('-v','--verbose', action='store_true', default=False,
                        dest='verbose',
                        help='verbose')
    parser.add_argument('-s','--store', help='log to database')
    args = parser.parse_args()

    print "Data Logger"
    status = "Options:"
    if args.tweet:
        status = status + " tweet"
    if args.lcd:
        status = status + " lcd"
    if args.led:
        status = status + " led"
    if args.tempo:
        status = status + " tempo"
    if args.thingspeak:
        status = status + " thingspeak"
    if args.verbose:
        status = status + " verbose"
    if args.store:
        status = status + " store: " + args.store
    print status
    exit

    if (args.lcd or args.led):
        humble.init()
        hdt = humble.HumbleDisplayThread(humble.data)
        hdt.start()

    count = 0

    

    while True:
        # Read data from sensors. Lux, temp and pressure
        lux = int(tsl.readLux())
        temperature = bmp.readTemperature()
        # Pressure in millibars
        pressure = bmp.readPressure()/100
        if args.lcd:
            report(lux,temperature,pressure)
        if args.led:
            colour(temperature)
        if args.verbose:
            print "LUX: ", lux
            print "TMP: ", temperature
            print "PRS: ", pressure
            print "Last Tweets"
            print "  lux", hms(lastTweet["lux"])
            print " temp", hms(lastTweet["temperature"])
           

        if args.tweet:
            tweet(lux, temperature)

        data = {
            'field1': lux,
            'field2': temperature,
            'field3': pressure
            }
        if (args.tempo):
            publishTempo(data,args.verbose)
#        print count
        if (count > THROTTLE):
            if (args.thingspeak):
                publishThingSpeak(data,args.verbose)
            if (args.store):
                store(args.store,lux,temperature,pressure,args.verbose)
            count = 0
        else:
            count = count + WAIT
            
        time.sleep(WAIT)

if __name__ == '__main__':
  main()

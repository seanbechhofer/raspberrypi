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

tsl = TSL2561()
bmp = BMP085()
flipflop = True
lastTweet = {
    "temperature": datetime.datetime(2013,1,1,0,0,0),
    "lux": datetime.datetime(2013,1,1,0,0,0)
}

TWEET={
    "cold":0,
    "hot":25,
    "dark":0,
    "bright":30000,
    "cycle":60
}

WAIT = 5
THROTTLE = 30
PUBLISH = False
BORG = False
LCD = False


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

def publishTempo(data,verbose=False):
    timestamp=datetime.datetime.now()
    mytempodb.write("pi.lux",timestamp,data['field1'])
    mytempodb.write("pi.temperature",timestamp,data['field2'])
    mytempodb.write("pi.pressure",timestamp,data['field3'])
    if verbose:
        print "Published to tempo-db", timestamp

def publishThingSpeak(data,verbose=False):
    thingspeak.log(data,verbose)

def store(db,lux,temperature,pressure,verbose=False):
    conn = sqlite3.connect(db) # or use :memory: to put it in RAM
    cursor = conn.cursor()
    cursor.execute("INSERT INTO data (lux,temperature,pressure) VALUES ("+str(lux)+","+str(temperature)+","+str(pressure)+")")
    conn.commit()
    if verbose:
        print "Logged to ", db
    
def report(lux,temperature,pressure):
    global flipflop
    humble.data.setLine(0,('Temp: {t:<4}'+chr(0xdf)+'C').format(t=temperature))
    if (flipflop):
        humble.data.setLine(1,'Pres: {t:<4}mb'.format(t=pressure))
    else:
        humble.data.setLine(1,'Lght: {t:<4}lux'.format(t=lux))
    flipflop = not flipflop

def tweet(lux,temperature):
    now=datetime.datetime.now()
    if temperature < TWEET["cold"]:
        if (now - lastTweet["temperature"]).seconds > TWEET["cycle"]:
            tweety.tweet(now.strftime('%H:%M') + " and it's Freezing! " + temperature + " degrees")
            lastTweet["temperature"] = now
    if temperature > TWEET["hot"]:
        if (now - lastTweet["temperature"]).seconds > TWEET["cycle"]:
            tweety.tweet((now.strftime('%H:%M') + " and it's Hot Hot Hot! {t:<4}"+" C").format(t=temperature))
            lastTweet["temperature"] = now
    if lux <= TWEET["dark"]:
        if (now - lastTweet["lux"]).seconds > TWEET["cycle"]:
            tweety.tweet(now.strftime('%H:%M') + " and it's dark!")
            lastTweet["lux"] = now
    if lux > TWEET["bright"]:
        if (now - lastTweet["lux"]).seconds > TWEET["cycle"]:
            tweety.tweet(now.strftime('%H:%M') + " Bright Light!")
            lastTweet["lux"] = now
            

def colour(temperature):
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
    parser.add_argument('-p','--thingspeak', action='store_true', default=False,
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

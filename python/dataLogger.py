from TSL2561 import TSL2561
from BMP085 import BMP085
import thingspeak
import time
import humbleII as humble
import LedBorg
import argparse

tsl = TSL2561()
bmp = BMP085()
flipflop = True
WAIT = 5
THROTTLE = 30
PUBLISH = False
BORG = False
LCD = False


COLD = 14
COOL = 16
OK = 18
WARM = 21
HOT = 24
TOASTY = 25

colours = {
    COLD: "blue",
    COOL: "lightblue",
    OK: "yellow",
    WARM: "green",
    HOT: "pink",
    TOASTY: "red"
    }

def report(lux,temperature,pressure):
    global flipflop
    humble.data.setLine(0,('Temp: {t:<4}'+chr(0xdf)+'C').format(t=temperature))
    if (flipflop):
        humble.data.setLine(1,'Pres: {t:<4}mb'.format(t=pressure))
    else:
        humble.data.setLine(1,'Lght: {t:<4}lux'.format(t=lux))
    flipflop = not flipflop

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
    parser.add_argument('-p','--publish', action='store_true', default=False,
                        dest='publish',
                        help='publish to thingspeak')
    parser.add_argument('-v','--verbose', action='store_true', default=False,
                        dest='verbose',
                        help='verbose')
    args = parser.parse_args()

    print "Data Logger"
    status = "Options:"
    if args.lcd:
        status = status + " lcd"
    if args.led:
        status = status + " led"
    if args.publish:
        status = status + " publish"
    if args.verbose:
        status = status + " verbose"
    print status

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

        data = {
            'field1': lux,
            'field2': temperature,
            'field3': pressure
            }
        if (count > THROTTLE):
            if(args.publish):
                thingspeak.log(data,args.verbose)
            count = 0
        else:
            count = count + WAIT
            
        time.sleep(WAIT)

if __name__ == '__main__':
  main()

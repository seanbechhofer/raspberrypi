from TSL2561 import TSL2561
from BMP085 import BMP085
import thingspeak
import time

tsl = TSL2561()
bmp = BMP085()
WAIT = 30

while True:
    # Read data from sensors. Lux, temp and pressure
    lux = tsl.readLux()
    temperature = bmp.readTemperature()
    # Pressure in millibars
    pressure = bmp.readPressure()/100
    print "LUX: ", lux
    print "TMP: ", temperature
    print "PRS: ", pressure

    data = {
        'field1': lux,
        'field2': temperature,
        'field3': pressure
        }
    thingspeak.log(data)

    time.sleep(WAIT)

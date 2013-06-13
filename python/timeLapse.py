import piface.pfio, time
from datetime import datetime

WAIT = 6
piface.pfio.init()
focus = piface.pfio.LED(0)
shutter = piface.pfio.LED(1)

def photo():
    focus.turn_on()
    time.sleep(1)
    shutter.turn_on()
    time.sleep(1)
    shutter.turn_off()
    focus.turn_off()

if __name__ == "__main__":
    count = 0
    while(True):
        photo()
        count = count+1
        print "Taken:", repr(count).rjust(1), "at", datetime.now().strftime("%H:%M:%S")
        time.sleep(WAIT-2)
        
        

    


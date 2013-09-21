#!/usr/bin/env python
"""
Code that uses external trigger (e.g. PIR) to take photos and 
upload to twitter
"""

import RPi.GPIO as GPIO
import argparse, os
import time, datetime
from twython import Twython, TwythonError
import ConfigParser

CYCLE=2
PIN = 7
WIDTH=1280
HEIGHT=960
GPIO.setwarnings(False) # Turn warnings off

GPIO.setmode(GPIO.BOARD)  
GPIO.setup(PIN, GPIO.IN)  

config = ConfigParser.ConfigParser()
config.read('/home/pi/conf/config.cfg')
APP_KEY = config.get('KEYS','twitter.consumer.key')
APP_SECRET = config.get('KEYS','twitter.consumer.secret')
OAUTH_TOKEN = config.get('KEYS','twitter.access.token')
OAUTH_TOKEN_SECRET = config.get('KEYS','twitter.access.token.secret')
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

def takePhoto():
    """Take a photo with the name based on the timestamp"""
    now=datetime.datetime.now()
    photo_name=now.strftime('%y%m%d-%H%M%S.jpg')
    os.system("raspistill -t 0" + 
              " -w " + str(WIDTH) + 
              " -h " + str(HEIGHT) + 
              " -o " + photo_name )
    return dict(time=now,name=photo_name)

def tweetPhoto(photo_info):
    """Tweet a photo"""
    photo = open(photo_info['name'], 'rb')
    message = 'Photo: ' + photo_info['time'].strftime('%H:%M:%S on %d/%m/%y')
    print message
    twitter.update_status_with_media(status=message,
                                     media=photo)
    # Delete photo_name

def main():
    parser = argparse.ArgumentParser(description='PIR Triggered camera')
    parser.add_argument('-p','--photo', action='store_true', default=False,
                        dest='photo',
                        help='Take Picture')
    parser.add_argument('-t','--tweet', action='store_true', default=False,
                        dest='tweet',
                        help='Tweet Picture')
    parser.add_argument('-c','--cycle', 
                        type=int,
                        default=10,
                        help='Cycle time')
    parser.add_argument('-d', '--delay', 
                        type=int,
                        default=5,
                        help='Delay after triggering')
    args = parser.parse_args()

    while True:
        print GPIO.input(PIN)
        if GPIO.input(PIN):
            if args.photo:
                photo_info = takePhoto()
                print photo_info
                if args.tweet:
                    tweetPhoto(photo_info)
                    print 'Tweeted!'
                time.sleep(args.delay)
        time.sleep(args.cycle)

if __name__ == '__main__':
  main()

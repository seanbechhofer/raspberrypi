#!/usr/bin/python
import humbleII as humble
import time
import urllib
import simplejson
import ConfigParser 
import argparse
from twython import Twython, TwythonError

PAUSE = 20

def showTweet(user, message):
    print user, message
    humble.data.setLine(0, "@"+user)
    humble.data.setScroll(1, True)
    humble.data.setLine(1, message)

def main():
    humble.init()
    hdt = humble.HumbleDisplayThread(humble.data)
    hdt.start()
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-q','--query', help='query')
    args = parser.parse_args()

    config = ConfigParser.ConfigParser()
    config.read('config.cfg')
    CONSUMERKEY = config.get('KEYS','twitter.consumer.key')
    CONSUMERSECRET = config.get('KEYS','twitter.consumer.secret')
    ACCESSTOKEN = config.get('KEYS','twitter.access.token')
    ACCESSTOKENSECRET = config.get('KEYS','twitter.access.token.secret')
    twitter = Twython(CONSUMERKEY, CONSUMERSECRET, 
                      ACCESSTOKEN, ACCESSTOKENSECRET)

    while True:
        try:
            search_results = twitter.search(q=args.query, count=1)
            for tweet in search_results['statuses']:
                showTweet(tweet['user']['screen_name'].encode('utf-8'),
                tweet['text'].encode('utf-8'))
                time.sleep(PAUSE)
        except TwythonError as e:
            print e

if __name__ == '__main__':
    main()

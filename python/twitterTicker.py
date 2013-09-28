#!/usr/bin/python
import humbleII as humble
import time
import urllib
import simplejson
import argparse
from twython import Twython, TwythonError
import keys

PAUSE = 20

def showTweet(user, message, verbose=False):
    if verbose:
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
    parser.add_argument('-v','--verbose', action='store_true', default=False,
                        dest='verbose',
                        help='verbose')
    args = parser.parse_args()

    # config = ConfigParser.ConfigParser()
    # config.read('/home/pi/conf/config.cfg')
    # CONSUMERKEY = config.get('KEYS','twitter.consumer.key')
    # CONSUMERSECRET = config.get('KEYS','twitter.consumer.secret')
    # ACCESSTOKEN = config.get('KEYS','twitter.access.token')
    # ACCESSTOKENSECRET = config.get('KEYS','twitter.access.token.secret')
    CONSUMERKEY = keys.key('twitter.consumer.key')
    CONSUMERSECRET = keys.key('twitter.consumer.secret')
    ACCESSTOKEN = keys.key('twitter.access.token')
    ACCESSTOKENSECRET = keys.key('twitter.access.token.secret')
    print CONSUMERKEY
    twitter = Twython(CONSUMERKEY, CONSUMERSECRET, 
                      ACCESSTOKEN, ACCESSTOKENSECRET)

    while True:
        try:
            search_results = twitter.search(q=args.query, count=3)
            for tweet in search_results['statuses']:
                showTweet(tweet['user']['screen_name'].encode('utf-8'),
                          tweet['text'].encode('utf-8'),
                          args.verbose)
                time.sleep(PAUSE)
        except TwythonError as e:
            print e

if __name__ == '__main__':
    main()

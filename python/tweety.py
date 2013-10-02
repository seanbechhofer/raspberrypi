from twython import Twython, TwythonError
import keys

APP_KEY = keys.key('twitter.consumer.key')
APP_SECRET = keys.key('twitter.consumer.secret')
OAUTH_TOKEN = keys.key('twitter.access.token')
OAUTH_TOKEN_SECRET = keys.key('twitter.access.token.secret')

# Requires Authentication as of Twitter API v1.1
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

def tweet(message):
    try:
        print "Tweeting: ", message
        twitter.update_status(status=message)
    except TwythonError as e:
        print e


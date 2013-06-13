import httplib, urllib, ConfigParser

config = ConfigParser.ConfigParser()
config.read('config.cfg')
KEY = config.get('KEYS','thingspeak')
#print KEY

def log(stuff,verbose=False):
    stuff['key'] = KEY
    if verbose:
        print stuff
    params = urllib.urlencode(stuff)
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    conn.request("POST", "/update", params, headers)
    response = conn.getresponse()
    if verbose:
        print response.status, response.reason
    data = response.read()
    conn.close()

#log('field1',20)

import httplib, urllib, keys

KEY = keys.key('thingspeak')
#print KEY

def log(stuff,verbose=True):
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


if __name__ == "__main__":
    thing_data = {
        'field1': 1000,
        'field2': 20,
        'field3': 999
    }
    log(thing_data,verbose=True)

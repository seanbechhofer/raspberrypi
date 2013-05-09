import httplib, urllib, ConfigParser

config = ConfigParser.ConfigParser()
config.read('config.cfg')
KEY = config.get('KEYS','thingspeak')
print KEY

params = urllib.urlencode({'field1': 98, 'key': KEY})
headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
conn = httplib.HTTPConnection("api.thingspeak.com:80")
conn.request("POST", "/update", params, headers)
response = conn.getresponse()
print response.status, response.reason
data = response.read()
conn.close()

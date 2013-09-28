import datetime,time, ConfigParser
from tempodb import Client, DataPoint

# Modify these with your credentials found at: http://tempo-db.com/manage/

config = ConfigParser.ConfigParser()
config.read('/home/pi/conf/config.cfg')
KEY = config.get('KEYS','tempo.db.key')
SECRET = config.get('KEYS','tempo.db.secret')
client = Client(KEY, SECRET)

def write(series,time,data):
    client.write_key(series,[DataPoint(time,data)])

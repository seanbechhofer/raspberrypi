import datetime,psutil,time,pytz
from tempodb import Client, DataPoint
import keys

# Modify these with your credentials found at: http://tempo-db.com/manage/

KEY = keys.key('tempo.db.key')
SECRET = keys.key('tempo.db.secret')
client = Client(KEY, SECRET)

def write(series,time,data):
    client.write_key(series,[DataPoint(time,data)])

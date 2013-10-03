import ConfigParser 

config = ConfigParser.ConfigParser()
config.read('/home/pi/conf/config.cfg')

def key(key):
    return config.get('KEYS',key)

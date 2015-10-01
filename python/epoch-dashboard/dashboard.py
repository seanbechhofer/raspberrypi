from flask import Flask, Response, json, render_template
import random
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data.json')
def data():
    global whatever, dude, maximum
    timestamp = int(time.time())
    mydata = {
        'timestamp': timestamp,
        'temperature': random.randint(0,100),
        'lux': random.randint(0,20000),
        'pressure': random.randint(950,1050),
        }
    # json.dumps converts the data structure into JSON, but
    # if we just returned that string, the default Content-Type
    # would be 'text/html'. We need to return a Response object
    # setting the right Content-Type for it
    return Response(json.dumps(mydata),  mimetype='application/json')

if __name__ == '__main__':
    app.run()

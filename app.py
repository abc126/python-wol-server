from flask import Flask
from flask import render_template
from flask import request

from component.wol import WakeOnLan

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/wol')
def wol():
    return render_template('wol.html')

@app.route('/api/v1/wol',methods=['POST', 'GET'])
def send_wol():
    mac = request.form['mac-address']
    sender = WakeOnLan()
    sender.send_magic_packet([mac])
    return "OK "+mac


if __name__ == '__main__':
    app.run(host='0.0.0.0')

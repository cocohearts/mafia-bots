from flask import Flask, render_template, request
from flask_socketio import SocketIO

# Make flask quieter
import logging
log = logging.getLogger('socketio')
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# https://stackoverflow.com/questions/29187933/flask-socketio-cors
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect(data):
    print(f"connection:", data, request.sid)

@socketio.on('message')
def handle_message(data):
    print(f"Received: {data}", request.sid)

if __name__ == '__main__':
    socketio.run(app, debug=True)

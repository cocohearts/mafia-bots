from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, send

# Make flask quieter
import logging
log = logging.getLogger('socketio')
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# https://stackoverflow.com/questions/29187933/flask-socketio-cors
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('set_username')
def set_username(data):
    print(f"set username data:", data)
    session['username'] = data

@socketio.on('message')
def handle_message(data):
    print(f"Received: {data}", session['username'])

if __name__ == '__main__':
    socketio.run(app, debug=True)

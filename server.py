# Game logic
from framework import Game

import datetime as dt
from datetime import timezone

# Web stuff
from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, send, emit

# Make flask quieter
import logging
log = logging.getLogger('socketio')
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# https://stackoverflow.com/questions/29187933/flask-socketio-cors
socketio = SocketIO(app, cors_allowed_origins="*")

# Store a dictionary of active games
# key is username, value is game
games = {}

def emit_message(author, content):
    emit('message', {
        'timestamp': dt.datetime.now().timestamp(),
        'author': author,
        'content': content
    })

@socketio.on('connect')
def handle_connect():
    pass

@socketio.on('new_game')
def handle_new_game():
    username = session['username']
    games[username] = Game()

@socketio.on('set_username')
def set_username(data):
    print(f"set username to:", data)
    session['username'] = data

@socketio.on('message')
def handle_message(data):
    # Ping messages back to user
    username = session['username']
    emit_message(username, data)

if __name__ == '__main__':
    socketio.run(app, debug=True)

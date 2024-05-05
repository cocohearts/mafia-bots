# Game logic
from framework import Game
from bot import Bot

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

    def callback(message_type, data):
        """ if message_type == "game_start":
            pass
        elif message_type == "night":
            pass
        elif message_type == "day":
            pass
        elif message_type == "night_turn":
            pass
        elif message_type == "day_turn":
            pass
        elif message_type == "got_killed":
            pass
        elif message_type == "got_attacked_saved":
            pass
        elif message_type == "vote":
            pass
        elif message_type == "game_over":
            pass """

        print(f"[game callback | {message_type}] {str(data)[:50]}")
        emit_message("system", f"[{message_type}] {data}")
        emit(message_type, data)

    prompts = {
        'Doctor': 'Your goal is to uncover and vote to eliminate the Mafia. Use your powers carefully, and do not reveal that you are the Doctor, otherwise you may be targeted by the Mafia.\n',
        'Cop': 'Your goal is to uncover and vote to eliminate the Mafia. Use your powers carefully, and do not reveal that you are the Cop, otherwise you may be targeted by the Mafia.\n',
        'Mafia': 'Your goal is to kill all of the Townspeople without being revealed and voted off.\n',
        'Villager': 'Your goal is to uncover and vote to eliminate the Mafia.\n'
    }
    roles = ['Mafia', 'Cop', 'Doctor', 'Villager', 'Villager', 'Villager']
    names = ['Alice', 'Bob', 'Charlie', "Daniel", "Eve", "Frank"]
    clients = [Bot(prompts) for _ in range(len(names))]

    games[username] = Game(roles=roles, names=names,
                           clients=clients, callback=callback)
    games[username].play()


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

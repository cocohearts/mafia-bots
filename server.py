from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# https://stackoverflow.com/questions/29187933/flask-socketio-cors
socketio = SocketIO(app, cors_allowed_origins="*")

if __name__ == '__main__':
    socketio.run(app)

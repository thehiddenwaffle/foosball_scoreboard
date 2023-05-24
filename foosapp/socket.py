from flask import g
from flask_socketio import SocketIO, emit

from foosapp.db import get_db
from foosapp.db.orm import get_current_game_orm

socketio = SocketIO()

def get_socket():
    if 'socket' not in g:
        g.socket = socketio

    return g.socket


@socketio.on('get lobby')
def handle_my_custom_event(json):
    d = get_db()
    left, right = None, None
    for user in get_current_game_orm().users:
        left, right = (user, right) if user.is_left else (left, user)
    data = {
        'right': {'id': right.nickname} if right else {},
        'left': {'id': left.nickname} if left else {}
    }
    emit('lobby data', data)

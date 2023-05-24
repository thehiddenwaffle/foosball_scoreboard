from typing import Literal, Union

from flask import (
    Blueprint, render_template, request, url_for, redirect, make_response
)
from flask_sqlalchemy import SQLAlchemy

from foosapp.db import get_db, UserGame, User, Game
from .auth import login_required
from ..qr_code import get_qr

bp = Blueprint('lobby', __name__, url_prefix='/lobby')


@bp.route('/', methods=['GET'])
def root_codes():
    # db.session.add()
    hostname = request.environ['REMOTE_ADDR']
    # player1_register_code = hostname + "/associate/left"
    # player2_register_code = hostname + "/associate/right"

    qr = get_qr()

    resp = make_response(render_template(
        'index.html',
        qr_code_p1=qr(hostname + url_for('game.associate', player_side='left')),
        qr_code_p2=qr(hostname + url_for('game.associate', player_side='right'))
    ))
    # resp.set_cookie('userID', user)

    return resp

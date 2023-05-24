from typing import Literal

from flask import (
    Blueprint, render_template, url_for, redirect, g
)

from foosapp.db import get_db, UserGame, get_current_game_orm
from .auth import login_required

bp = Blueprint('game', __name__, url_prefix='/game')


@bp.route('/associate/<string:player_side>', methods=['GET'])
@login_required
def associate(player_side: Literal['left', 'right'], player_obj=None):
    user_to_associate = player_obj or g.user
    if user_to_associate and player_side:
        a = UserGame(is_left=(player_side == 'left'))
        a.user = player_obj or user_to_associate
        g.curr_game.users.append(a)
        get_db().session.commit()
        return render_template('confirmed-game.html')
    else:
        return redirect(url_for("auth.register", player_side=player_side))


@bp.before_app_request
def attach_curr_game():
    curr_game = get_current_game_orm()
    if curr_game is None:
        g.curr_game = None
    else:
        g.curr_game = curr_game

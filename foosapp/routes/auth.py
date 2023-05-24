import functools
from typing import cast, Literal, Optional

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from sqlalchemy.exc import NoResultFound, IntegrityError

from foosapp.db import get_db, get_user, User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register/', defaults={'player_side': ""}, methods=['GET', 'POST'])
@bp.route('/register/redirect-to-side/<string:player_side>')
def register(player_side: Optional[Literal['left', 'right']]):
    if request.method == 'POST':
        error = None
        nickname, pin = (request.form['nickname'], request.form['pin'])

        if not nickname:
            error = 'Username is required.'
        elif not pin:
            error = 'Password is required.'
        elif player_side and player_side not in ['left', 'right']:
            error = 'Invalid side chosen'

        if error is None:
            d = get_db()
            try:
                new_user = User(nickname=request.form['nickname'], pin=request.form['pin'])
                d.session.add(new_user)
                d.session.commit()
            except IntegrityError:
                error = f"Name {nickname} is already registered."
            else:
                session.clear()
                session['user_id'] = new_user.id
                # return redirect(url_for("game.associate") + "/{}".format(player_side))
                return render_template('confirmed-game.html')

        flash(error)

    return render_template(
        'auth/signup.html',
        player_side=player_side
    )


@bp.route('/login/', defaults={'player_side': ""}, methods=['GET', 'POST'])
@bp.route('/login/redirect-to-side/<string:player_side>', methods=['GET', 'POST'])
def login(player_side: Optional[Literal['left', 'right']]):
    if request.method == 'POST':
        nickname, pin = (request.form['nickname'], int(request.form['pin']))
        d = get_db()
        error = None
        user = None
        try:
            user = d.session.execute(d.select(User).where(User.nickname == nickname)).scalar_one()
        except NoResultFound:
            error = 'Incorrect username.'
        else:
            if user.pin != pin or not (4 <= len(str(pin)) <= 6):
                error = 'Incorrect or bad pin.'

        if error is None and user:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('game.associate', player_side=player_side)) if player_side else \
                render_template('auth/account-confirm.html')
        else:
            flash(error)

    return render_template(
        'auth/login.html',
        player_side=player_side
    )


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    d = get_db()
    if user_id is None:
        g.user = None
    else:
        try:
            g.user = get_user(user_id)
        except NoResultFound:
            g.user = None


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user' not in g or g.user is None:
            return redirect(url_for('auth.login', **kwargs))

        return view(**kwargs)

    return wrapped_view

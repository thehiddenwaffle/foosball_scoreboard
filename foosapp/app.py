import os
from typing import Literal

from flask import Flask, redirect, url_for

from .db import db_hook, Game, UserGame, Goal, get_db, create_new_game_orm, get_current_game_orm, User
# from .goal_sensors import bind_on_goal_scored_left, bind_on_goal_scored_right
from .qr_code import qr_code
from .socket import socketio


def score_goal(side: Literal['right', 'left']):
    d = get_db()

    def db_score():
        current_game: Game = get_current_game_orm()
        left_user_game: UserGame = d.session.execute(
            d.select(UserGame).where(
                UserGame.is_left == (side == 'left'),
                UserGame.games_id == current_game.id
            )
        ).scalar_one()
        left_user: User = d.session.execute(
            d.select(User).where(
                User.id == left_user_game.users_id
            )
        ).scalar_one()
        current_game.goals.append(Goal(scored_by=left_user))
        get_db().session.commit()
    return db_score


# right_goal_switch.when_activated = score_goal('right')
# left_goal_switch.when_activated = score_goal('left')


def create_app(test_config=None):
    basedir = os.path.abspath(os.path.dirname(__file__))

    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = 'Yeah this app wasnt that secure to begin with 48296739069'
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI='sqlite:///' + app.root_path + '/db/fb_database.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_TYPE='filesystem'
    )
    # Extensions
    db_hook.init_app(app)
    qr_code.init_app(app)
    socketio.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Blueprints
    from foosapp.routes import lobby_bp
    from foosapp.routes import game_bp
    from foosapp.routes import auth_bp
    app.register_blueprint(lobby_bp)
    app.register_blueprint(game_bp)
    app.register_blueprint(auth_bp)

    app.add_url_rule("/", view_func=lambda: redirect(url_for('lobby.root_codes')))

    with app.app_context():
        db_hook.create_all()
        # Delete any hanging games
        Game.query.filter(Game.ended_at.is_(None)).delete()
        create_new_game_orm()
        db_hook.session.commit()

    # bind_on_goal_scored_left(score_goal('right'))
    # bind_on_goal_scored_right(score_goal('left'))

    return app

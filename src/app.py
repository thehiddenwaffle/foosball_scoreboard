import os
from datetime import datetime

from flask import Flask, render_template, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_qrcode import QRcode
from .db import Goal, Game, User

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'fb_database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
QRcode(app)


@app.route('/', methods=['GET'])
def root_codes():  # put application's code here
    # db.session.add()
    hostname = request.environ['REMOTE_ADDR']
    player1_register_code = hostname + "/associate/player1"
    player2_register_code = hostname + "/associate/player2"

    resp = make_response(render_template(
        'index.html',
        qr_code_p1=player1_register_code,
        qr_code_p2=player2_register_code)
    )
    # resp.set_cookie('userID', user)

    return resp


@app.route('/associate/<string:player>', methods=['POST'])
def associate(string: str):
    user_id: str
    if string == "player1":
        user_id = request.cookies.get('foosball_id')
    elif string == "player2":
        user_id = request.cookies.get('foosball_id')
    if not user_id:
        return

@app.route('/register', methods=['POST'])
def register():
    request.


if __name__ == '__main__':
    app.run()

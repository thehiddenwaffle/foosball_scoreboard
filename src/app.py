import os
from datetime import datetime

from flask import Flask, render_template, request
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
def hello_world():  # put application's code here
    # db.session.add()
    hostname = request.environ['REMOTE_ADDR']
    player1_register_code = hostname + "/register/player1"
    player2_register_code = hostname + "/register/player2"
    return render_template('index.html', qr_code="Do you speak QR?")


@app.route('/register/<string:player>', methods=['POST'])
def register(string: str):
    user_id: str
    if string == "player1":
        user_id = request.cookies.get('foos_id')
    elif string == "player2":
        user_id = request.cookies.get('foos_id')
    if not user_id:
        pass
        # Create the username



if __name__ == '__main__':
    app.run()

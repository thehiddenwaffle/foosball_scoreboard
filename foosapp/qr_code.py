from flask import g
from flask_qrcode import QRcode

qr_code = QRcode()


def get_qr():
    if 'qr_code' not in g:
        g.qr_code = qr_code

    return g.qr_code

import logging
from logging.handlers import RotatingFileHandler
import os

from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/onhwa.log', maxBytes=102400, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.DEBUG)

    app.logger.info('Onhwa Cafe startup')

from app import routes, models # this line is located in the bottom to avoid import loop

'''
logging.basicConfig(level = logging.DEBUG)
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
else:
    file_handler = logging.FileHandler('onhwa.log')
    handler = logging.StreamHandler()
    file_handler.setLevel(logging.DEBUG)
    logging.handler.setLevel(logging.DEBUG)
    logging.file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
     ))
    logging.handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
     ))
    app.logger.addHandler(handler)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.DEBUG)
'''


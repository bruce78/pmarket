# app/__init__.py
from flask_cors import CORS
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
# local import

from instance.config import app_config
import os

# For password hashing
from flask_bcrypt import Bcrypt


def setConfig(config_name):
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # import the authentication blueprint and register it on the app
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)


app = FlaskAPI(__name__, instance_relative_config=True)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_POOL_SIZE'] = 20
app.config['JSON_AS_ASCII'] = False
# initialize db
db = SQLAlchemy(app)
config_name = os.getenv('APP_SETTINGS')
setConfig(config_name)




from app import db
from flask_bcrypt import Bcrypt
from flask import current_app
import jwt
from datetime import datetime, timedelta
from sqlalchemy.ext.declarative import declared_attr


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    createdTime = db.Column(db.DateTime,  default=db.func.current_timestamp())
    modifiedTime = db.Column(db.DateTime,  default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def save(self):
        """Save a Base to the database.
        This includes creating a new user and editing one.
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Deletes a given Base."""
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

class Admin(Base):
    __tablename__ = 'admin'

    userId = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    state = db.Column(db.String(60))

    def __init__(self, userId, email, password):
        """Initialize the user with an email and a password."""
        self.userId = userId
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def passwordIsValid(self, password):
        """
        Checks the password against it's hash to validates the user's password
        """
        return Bcrypt().check_password_hash(self.password, password)


    @staticmethod
    def generateToken(userId):
        """Generates the access token to be used as the Authorization header"""

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': userId
            }
            # create the byte string token using the payload and the SECRET key
            jwtString = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwtString

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decodeToken(token):
        """Decode the access token from the Authorization header."""
        try:
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired token. Please log in to get a new token"
        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login"


class User(Base):
    __tablename__ = 'user'

    userId = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    state = db.Column(db.String(60))

    countryCode = db.Column(db.Integer)
    nationalNumber = db.Column(db.String(20))
    telegramId = db.Column(db.Integer, unique=True)
    telegramUsername = db.Column(db.String(60))
    telegramFirstName = db.Column(db.String(60))
    telegramLastName = db.Column(db.String(60))
    locale = db.Column(db.String(60))
    currency = db.Column(db.String(60))

    def passwordIsValid(self, password):
        """
        Checks the password against it's hash to validates the user's password
        """
        return Bcrypt().check_password_hash(self.password, password)


class HistoryData(Base):
    # import sqlalchemy.dialects.mysql.JSON
    # length = (2 ** 32) - 1
    data = db.Column(db.Text(4294000000))
    coin = db.Column(db.String(120))
    # step secs
    step = db.Column(db.Integer)
    type = db.Column(db.String(120))


class CoinInfo(Base):
    coin = db.Column(db.String(120), unique=True)
    h24 = db.Column(db.String(120))
    l24 = db.Column(db.String(120))
    percentage = db.Column(db.String(120))
    flowRate = db.Column(db.String(120))
    turnoverRate = db.Column(db.String(120))
    info = db.Column(db.Text(4294000000))


class ExchangeInfo(Base):
    code = db.Column(db.String(80), unique=True)
    h24Volume = db.Column(db.String(40))
    marketNum = db.Column(db.String(120))
    country = db.Column(db.String(40))
    icon = db.Column(db.String(200))
    tradeTypes = db.Column(db.String(120))
    name = db.Column(db.String(30))
    homeLink = db.Column(db.String(80))
    description = db.Column(db.Text(4294000000))


db.create_all()


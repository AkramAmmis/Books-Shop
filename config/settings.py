#settings datei
from dotenv import load_dotenv
import os

load_dotenv()

class Config():
    DEBUG =  True
    PORT = os.environ.get('PORT') or 6000
    SERVER_NAME = 'akram.com:5000'
    ENV = os.environ.get('ENV')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    print(MAIL_PASSWORD,MAIL_USERNAME)

    PAYPAL_CLIENT_ID = os.environ.get('PAYPAL_CLIENT_ID')
    PAYPAL_CLIENT_SECRET = os.environ.get('PAYPAL_CLIENT_SECRET')

    FLASK_ADMIN_SWATCH = 'cerulean'

class Development(Config):
    DEBUG = True
    PORT = os.environ.get('PORT') or 9000
    PAYPAL_MODE = 'sandbox'
class Production(Config):
    DEBUG = False
    PORT = os.environ.get('PORT') or 8080
    PAYPAL_MODE = 'live'

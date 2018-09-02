from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_redis import FlaskRedis

api = Api()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
redis_store = FlaskRedis()
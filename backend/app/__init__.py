from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__)

app.config.from_pyfile('./config.py')

db = SQLAlchemy(app)

auth = HTTPTokenAuth(scheme='Token')

# 所有对象要在注册之前初始化，否则找不到该对象
from app.user import user

app.register_blueprint(user, url_prefix="/api")

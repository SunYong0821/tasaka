# coding: utf-8
##用来创建数据库模型
#from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
#app = Flask(__name__)
#app.config.from_pyfile('./config.py')
#db = SQLAlchemy(app)


from app import db, auth
from flask import current_app, jsonify
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

@auth.error_handler
def error_handler():
    return jsonify({'code':401, 'msg':'Unauthorized Access'})

@auth.verify_token
def verify_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        s.loads(token)
    except SignatureExpired:
        return False
    except BadSignature:
        return False
    return True


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    gender = db.Column(db.Integer)
    city = db.Column(db.String(32))
    province = db.Column(db.String(32))
    country = db.Column(db.String(32))
    img = db.Column(db.String(128))
    openid = db.Column(db.String(32))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def to_json(self):
        return {
            'name': self.name,
            'gender': self.gender,
            'city': self.city,
            'province': self.province,
            'country': self.country,
            'img': self.img,
            'openid': self.openid,
        }

    def generate_auth_token(self):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
        return str(s.dumps({'openid': self.openid}), encoding='utf-8')


if __name__ == '__main__':
    db.create_all()

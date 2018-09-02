"""
数据模型
"""

import uuid
from datetime import datetime
from flask import jsonify
from flask_login import UserMixin
from apiserver.extends import db, login_manager
from apiserver.utils import cryptor
from apiserver.utils import get_code
from apiserver.mixins.crud import CRUDMixin

# pylint: disable=all

def make_uuid():
    return uuid.uuid4().hex[:16]


class User(db.Model, UserMixin):
    """ 用户"""

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
    }

    id = db.Column(db.String(16), default=make_uuid, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(50), nullable=False)
    salt = db.Column(db.String(50), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)
    last_login_time = db.Column(db.DateTime, default=datetime.now)
    soft_del = db.Column(db.Boolean, default=False)

    def __init__(self, username, password):
        """ 初始化"""
        self.username = username
        self.password = password

    @classmethod
    def create(cls, username, password):
        """ 创建用户"""
        _user = cls(username, password)
        db.session.add(_user)
        db.session.commit()
        return _user

    @property
    def password(self):
        """ 获取密码hash值"""
        raise AttributeError('Password is not readable.')

    @password.setter
    def password(self, password):
        """ 设置密码"""
        salt = get_code()
        self.salt = salt
        self.password_hash = cryptor.encrypt(password, salt=salt)

    def verify_password(self, password):
        """ 验证密码"""
        return self.password_hash == cryptor.encrypt(password, salt=self.salt)
    
    def __repr__(self):
        return '<User id: {}, username: {}>'.format(self.id, self.username)


class Category(db.Model, CRUDMixin):

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
    }

    id = db.Column(db.String(16), default=make_uuid, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class Article(db.Model, CRUDMixin):

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
    }
    """
    :field status 0: 删除, 1:发布, 2:下线
    """

    id = db.Column(db.String(16), default=make_uuid, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(16), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.Integer, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)


    def to_json(self, has_content=False):
        resp = {
            'id': self.id,
            'title': self.title,
            'status': self.status,
            'category': self.category,
        }
        category = Category.get_first(id=self.category)
        resp['categoryName'] = category.name
        if has_content:
            resp['content'] = self.content

        return resp


def authenticate(username, password):
    """ 验证"""
    user = User.query.filter_by(username=username).first()
    if user and user.verify_password(password):
        return user


def identity(payload):
    """ 获取用户身份"""
    user_id = payload['identity']
    return User.query.filter_by(id=user_id).first()


def auth_response(token, identity):
    """ 认证返回"""
    return jsonify({
        'access_token': token.decode('utf-8'),
        'username': identity.username,
        'role': identity.role.name,
    })


@login_manager.user_loader
def load_user(user_id):
    """ 获取登录用户"""
    user = User.query.filter_by(id=user_id).first()
    return user


# @login_manager.unauthorized_handler
# def unauthenticated():
#     """ 用户未登录"""
#     return jsonify({
#         'code': 0,
#         'msg': '用户没有登录',
#     })
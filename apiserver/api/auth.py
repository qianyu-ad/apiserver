from .base import RestApi, router
from flask import request
from flask_restful import reqparse
from flask_login import login_user, logout_user, login_required
from apiserver.models import authenticate


@router('/api/login')
class LoginApi(RestApi):

    def parse_form(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'username', required=True, help="用户名不能为空", location="json",
        )
        parser.add_argument(
            'password', required=True, help="密码不能为空", location="json",
        )
        return parser.parse_args()

    def post(self):
        form_data = self.parse_form()
        user = authenticate(form_data['username'], form_data['password'])
        if user:
            login_user(user, True)
            return self.ok(msg="成功登录")
        else:
            return self.no(msg="用户名或密码错误")


@router('/api/logout')
class LogoutApi(RestApi):
    """ 登出"""
    decorators = [login_required]

    def get(self):
        logout_user()
        return self.ok(msg="成功退出")
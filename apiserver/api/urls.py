"""
api 路由加载， 需要加载模块到当前文件, 例如:

    from web.api import auth

这样router装饰器才会把路由加载到当前应用
"""
from apiserver.api import auth
from apiserver.api import article


from apiserver.api.base import register_restful_api
__all__ = ['register_restful_api']
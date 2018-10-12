from .base import RestApi, router
from flask import request, jsonify
from flask_restful import reqparse
from flask_login import login_user, logout_user, login_required
from apiserver.models import Article, Category


@router('/api/category')
class CateroyApi(RestApi):

    decorators = [login_required]

    def parse_form(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'id', location="json",
        )
        parser.add_argument(
            'name', location='json', required=True, help="name 不能为空",
        )
        parser.add_argument(
            'code', location='json', required=True, help="code 不能为空",
        )
        parser.add_argument(
            'siteCode',
            location='json',
            required=True,
            help="siteCode 不能为空",
            dest="site_code",
        )
        args = parser.parse_args()
        args = {k: v for k, v in args.items() if v}
        return args

    def get(self):
        categories = Category.query.all()
        return self.ok(data={
            "list": [c.to_json() for c in categories]
        })
    
    def post(self):
        form_data = self.parse_form()
        if 'id' in form_data:
            category = Category.get_first(id=form_data.pop('id'))
            if category:
                category.update(**form_data)
                return self.ok(msg="更新成功")
            else:
                return self.no(msg="没有找到该分类")
        else:
            category = Category.create(**form_data)
            if category:
                return self.ok(msg="创建成功")
            else:
                return self.no(msg="创建失败")
    
    def delete(self):
        data = request.get_json() or {}
        _id = data.get('id')
        if not _id:
            return self.no(msg="id 不能为空")
        
        category = Category.get_first(id=_id)
        if category:
            articles = Article.get(category=category.id).count()
            if articles > 0:
                return self.no(msg="该分类下存在文章，不能删除")
            else:
                category.delete(True)
                return self.ok(msg="删除成功")
        else:
            return self.no(msg="没有找到该分类") 


@router('/api/articles')
class ArticleListApi(RestApi):

    def parse_form(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'title', required=True, help="标题不能为空", location="json",
        )
        parser.add_argument(
            'content', required=True, help="内容不能为空", location="json",
        )
        parser.add_argument(
            'categoryId', required=True,
            help="分类不能为空", location="json",
            dest="category_id"
        )
        parser.add_argument(
            'keywords', location='json',
        )
        parser.add_argument(
            'description', location='json',
        )
        parser.add_argument(
            'id', location="json",
        )
        args = parser.parse_args()
        args = {k: v for k, v in args.items() if v}
        return args
    
    def query_form(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', default=1, type=int)
        parser.add_argument('size', default=10, type=int)
        parser.add_argument('categoryId', dest='category_id')
        parser.add_argument('status')
        parser.add_argument('id')
        args = parser.parse_args()
        args = {k: v for k, v in args.items() if v}
        return args

    def get(self):
        querys = self.query_form()
        if 'id' in querys:
            article = Article.get_first(id=querys['id'])
            if article:
                return self.ok(data=article.to_json(True))
            else:
                return self.no(msg="没有找到该文章")
        else:
            page = querys.pop('page')
            size = querys.pop('size')
            articles = Article.get(**querys)
            total = articles.count()
            articles = articles.order_by(
                Article.create_time.desc()
            ).offset((page-1) * size).limit(size).all()
            return self.ok(data={
                "total": total,
                "list": [article.to_json() for article in articles]
            })
    
    @login_required
    def post(self):
        form_data = self.parse_form()
        if 'id' in form_data:
            article = Article.get_first(id=form_data.pop('id'))
            if article:
                article.update(**form_data)
                return self.ok(msg="更新成功")
            else:
                return self.no(msg="没有找到该文章")
        else:
            article = Article.create(**form_data)
            if article:
                return self.ok(msg="创建成功")
            else:
                return self.no(msg="创建失败")
    
    @login_required
    def delete(self):
        data = request.get_json() or {}
        _id = data.get('id')
        if not _id:
            return self.no(msg="id 不能为空")

        article = Article.get_first(id=_id)
        if article:
            article.delete(True)
            return self.ok(msg="删除成功")
        else:
            return self.no(msg="没有找到该文章") 


@router('/api/articles/update/status')
class ArticleStatusApi(RestApi):

    decorators = [login_required]

    def parse_form(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'id', location="json", required=True, help="id 不能为空",
        )
        parser.add_argument(
            'status', location='json', required=True, help="status 不能为空", type=int
        )
        args = parser.parse_args()
        return args

    def post(self):
        form_data = self.parse_form()
        article = Article.get_first(id=form_data['id'])
        article.update(status=form_data['status'])
        return self.ok(msg="更新成功")

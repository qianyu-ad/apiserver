from .base import RestApi, router
from flask_restful import reqparse
from flask import request, jsonify
from flask_login import login_required
from apiserver.models import Site, Seo


@router('/api/site')
class SiteListApi(RestApi):

    decorators = [login_required]

    def parse_form(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'name', required=True, help="名称不能为空", location="json",
        )
        parser.add_argument(
            'code', required=True, help="子域名不能为空", location="json",
        )
        parser.add_argument(
            'id', location="json",
        )
        parser.add_argument(
            'desc', location="json",
        )
        args = parser.parse_args()
        args = {k: v for k, v in args.items() if v}
        return args
    
    def get(self):
        sites = Site.query.all()
        return self.ok(data={
            "list": [site.to_json() for site in sites]
        })
    
    def post(self):
        form_data = self.parse_form()
        if 'id' in form_data:
            site = Site.get_first(id=form_data.pop('id'))
            if site:
                site.update(**form_data)
                return self.ok(msg="更新成功")
            else:
                return self.no(msg="没有找到该网站")
        else:
            site = Site.create(**form_data)
            if site:
                return self.ok(msg="创建成功")
            else:
                return self.no(msg="创建失败")
    
    def delete(self):
        data = request.get_json() or {}
        _id = data.get('id')
        if not _id:
            return self.no(msg="id 不能为空")
        
        site = Site.get_first(id=_id)
        if site:
            site.delete(True)
            return self.ok(msg="删除成功")
        else:
            return self.no(msg="没有找到该分类") 


@router('/api/seo')
class SeoApi(RestApi):

    decorators = [login_required]

    def parse_form(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'name', required=True, help="名称不能为空", location="json",
        )
        parser.add_argument(
            'keywords', location="json",
        )
        parser.add_argument(
            'description', location="json",
        )
        parser.add_argument(
            'id', location="json",
        )
        parser.add_argument(
            'desc', location="json",
        )
        args = parser.parse_args()
        args = {k: v for k, v in args.items() if v}
        return args

    def get(self):
        data = request.get_json() or {}
        _id = data.get('id')
        if _id:
            seo = Seo.get_first(id=_id)
            if seo:
                return self.ok(data=seo.to_json())
            else:
                return self.no(msg="没有找到该seo")
        else:
            seo_list = Seo.query.all()
            return self.ok(data={
                'list': [s.to_json() for s in seo_list]
            })

    def post(self):
        form_data = self.parse_form()
        if 'id' in form_data:
            seo = Seo.get_first(id=form_data.pop('id'))
            if seo:
                seo.update(**form_data)
                return self.ok(msg="更新成功")
            else:
                return self.no(msg="没有找到该seo")
        else:
            seo = Seo.create(**form_data)
            if seo:
                return self.ok(msg="创建成功")
            else:
                return self.no(msg="创建失败")
    
    def delete(self):
        data = request.get_json() or {}
        _id = data.get('id')
        if not _id:
            return self.no(msg="id 不能为空")
        
        seo = Seo.get_first(id=_id)
        if seo:
            seo.delete(True)
            return self.ok(msg="删除成功")
        else:
            return self.no(msg="没有找到该seo") 
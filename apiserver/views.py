from flask import Blueprint, abort, render_template, current_app, request
from apiserver.models import Article

bp = Blueprint('home', __name__)

@bp.route('/')
def index():
    _id = request.args.get('id')
    article = Article.get_first(id=_id)
    return render_template('article.html', article=article)


@bp.route('/articles/<id>')
def render_conetnt(id):
    article = Article.get_first(id=id)
    if article:
        return article.content
    else:
        abort(404)
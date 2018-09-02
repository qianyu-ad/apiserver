from flask import Blueprint, abort, render_template, current_app
from apiserver.models import Article

bp = Blueprint('home', __name__)

@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/articles/<id>')
def render_conetnt(id):
    article = Article.get_first(id=id)
    if article:
        return article.content
    else:
        abort(404)
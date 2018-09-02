from flask import Blueprint, abort
from apiserver.models import Article

bp = Blueprint('home', __name__)


@bp.route('/articles/<id>')
def render_html(id):
    article = Article.get_first(id=id)
    if article:
        return article.content
    else:
        abort(404)
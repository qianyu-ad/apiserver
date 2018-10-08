from flask import Blueprint, abort, render_template, current_app, request
from apiserver.models import Article, Category

bp = Blueprint('home', __name__)


def get_top15_articles(category_id=None):
    """ 获取15个浏览量最高的文章"""
    if category_id is not None:
        articles = Article.query.filter_by(
            category_id=category_id
        )
    else:
        articles = Article.query
    
    articles = articles.order_by(
        Article.count.desc(),
        Article.create_time.desc()
    ).limit(15)
    return articles


def get_site_categories():
    """ 获取网站分类"""
    site_code = request.host.split('.')[0]
    categories = Category.query.filter_by(site_code=site_code)
    return categories


@bp.route('/')
@bp.route('/category/<category_code>')
def index(category_code=None):
    page = request.args.get('page', 1, type=int)
    categories = get_site_categories()
    if category_code:
        category = Category.get_first(code=category_code)
        if category:
            articles = Article.query.filter_by(
                category_id=category.id
            ).order_by(
                Article.create_time.desc()
            )
            pagination = articles.paginate(page, per_page=10, error_out=False)
            top_articles = get_top15_articles(category.id)
            return render_template(
                'index.html',
                articles=articles,
                pagination=pagination,
                top_articles=top_articles,
                categories=categories,
            )

    category_ids = [c.id for c in categories]    
    articles = Article.query.filter(
        Article.category_id.in_(category_ids)
    ).order_by(
        Article.create_time.desc()
    )
    pagination = articles.paginate(page, per_page=10, error_out=False)
    top_articles = get_top15_articles()

    return render_template(
        'index.html',
        articles=articles,
        pagination=pagination,
        top_articles=top_articles,
        categories=categories,
    )


@bp.route('/article/<id>')
def detail(id):
    article = Article.get_first(id=id)
    if article:
        count = article.count or 0
        article.update(count=count + 1)
        top_articles = get_top15_articles(article.category_id)
    else:
        top_articles = get_top15_articles()
    
    categories = get_site_categories()
    return render_template(
        'article.html',
        article=article,
        top_articles=top_articles,
        categories=categories,
    )
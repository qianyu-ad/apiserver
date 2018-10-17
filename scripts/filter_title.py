import os
import sys
import json
sys.path.append(os.getcwd())
from apiserver.models import db, Article
from manage import app


def main():
    with app.app_context():
        articles = Article.query.all()
        for article in articles:
            title = article.title.split('</h1>')[0]
            if article.title != title:
                article.title = title
        
        db.session.commit()

if __name__ == '__main__':
    main()
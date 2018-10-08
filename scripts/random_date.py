import os
import sys
sys.path.join(os.path.dirname(os.getcwd()))
from apiserver.utils import random_date
from apiserver.models import db, Article
from manage import app


def main():
    with app.app_context():
        articles = Article.query.all()
        for article in articles:
            article.display_time = random_date()
        
        db.session.commit()

if __name__ == '__main__':
    main()
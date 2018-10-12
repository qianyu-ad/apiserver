import os
import sys
import json
sys.path.append(os.getcwd())
from apiserver.models import db, Article
from manage import app

path = '/data/work/jsonfile'


def main():
    with app.app_context():
        for filename in os.listdir(path):
            filepath = os.path.join(path, filename)
            with open(filepath) as fd:
                result = json.loads(fd.read())
                article = Article(
                    category_id=result['categoryId'],
                    title=result['title'],
                    content=result['content'],
                    keywords=result['keywords'],
                    description=result['seoDescription'],
                )
                db.session.add(article)
            os.remove(filepath)
        db.session.commit()

if __name__ == '__main__':
    main()
"""
管理
"""
import os
from flask_script import Server, Manager
from apiserver.app import create_app
from apiserver.models import db, User, Article, Category, Site, Seo
from apiserver.utils import random_date
from flask_migrate import Migrate, MigrateCommand

# pylint: disable=all

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.command
def init_admin():
    # 初始化角色
    user = User.create('admin', 'admin123')
    db.session.add(user)
    db.session.commit()


@manager.command
def drop():
    db.drop_all()


@manager.command
def runserver():
    os.system('gunicorn -c unicorn.py manage:app')


@manager.command
def random_date():
    articles = Article.query.all()
    for article in articles:
        article.display_time = random_date()
    
    db.session.commit()

manager.add_command('run', Server(
    host='0.0.0.0',
    port=5000,
    use_reloader=True,
    use_debugger=True
))


def main():
    manager.run()

if __name__ == '__main__':
    main()
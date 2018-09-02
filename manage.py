"""
管理
"""
from flask_script import Server, Manager
from apiserver.app import create_app
from apiserver.models import db, User, Article, Category

# pylint: disable=all

app = create_app()
manager = Manager(app)


@manager.command
def init():
    drop()
    db.create_all()
    # 初始化角色
    user = User.create('admin', 'admin123')
    cate = Category.create(name="通用")
    article = Article.create(title='你好', content="好好吃啊", category=cate.id)
    db.session.add(user)
    db.session.add(article)
    db.session.add(cate)
    db.session.commit()


@manager.command
def drop():
    db.drop_all()


@manager.command
def runserver():
    os.system('gunicorn -c unicorn.py manage:app')

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
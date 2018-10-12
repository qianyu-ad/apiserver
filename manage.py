"""
管理
"""
import os
from flask_script import Server, Manager
from apiserver.app import create_app
from apiserver.models import db, User, Article, Category, Site
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
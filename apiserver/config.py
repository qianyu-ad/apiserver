"""
项目配置文件
"""
import os
import logging

ROOT_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
DOWN_DIR = os.path.join(
    ROOT_DIR,
    'downloads',
)

DEBUG = False
SECRET_KEY = b'flask_cap make a project'
REDIS_URL = "redis://localhost:6379/0"
DB_CONFIG = dict(
    host='127.0.0.1',
    db='apiserver',
    username='root',
    password='123456',
)


try:
    from local_settings import LOCAL_DB_CONFIG, LOCAL_DEBUG_CONFIG
    DB_CONFIG.update(LOCAL_DB_CONFIG)
    DEBUG = LOCAL_DEBUG_CONFIG
    print('db config: ', DB_CONFIG)
except ImportError:
    pass

if not DEBUG:
    # 日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%Y%m%d %H:%M:%S',
        filename='apiserver.log',
        filemode='a'
    )

# 数据库连接
DB_URI = "mysql+pymysql://{}:{}@{}/{}?charset=utf8".format(
    DB_CONFIG['username'], DB_CONFIG['password'],
    DB_CONFIG['host'], DB_CONFIG['db'],
)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_restful import Api
#数据库兼容
import pymysql
pymysql.install_as_MySQLdb()
#实例化插件
csrf = CSRFProtect()
models = SQLAlchemy()
api = Api()

def create():
    """
    生成app配置
    :return:
    """
    app = Flask(__name__)#创建APP
    app.config.from_object("settings.Config")#加载配置
    models.init_app(app)# models = SQLAlchemy(app) 加载数据库
    #csrf.init_app(app) #加载csrf插件
    api.init_app(app)
    #导入蓝图
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
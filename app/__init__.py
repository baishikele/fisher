from flask import Flask
from app.models.base import db
from flask_login import LoginManager
from flask_mail import Mail

login_manager = LoginManager()
mail = Mail()

def create_app():
    # app = Flask(__name__, static_folder='xx/xx') # 可以更改默认静态文件路径和访问url，原理也是用装饰器注册视图函数
    app = Flask(__name__) # 插线排
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')

    # 蓝图
    register_blueprint(app)

    # loginmanager，管理用户cookie
    login_manager.init_app(app)
    # 告诉flask哪个视图函数是登录
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或注册'

    # 数据库
    db.init_app(app)
    db.create_all(app=app)# RuntimeError: No application found!!!!，可通过查看源码，有几种方式解决，with语句自己把上下文加入栈中/

    # 注册mail
    mail.init_app(app)

    return app

def register_blueprint(app):
    # 必须在视图控制器加入装饰器以后，在把蓝图注册到app，注意注册顺序！！！！
    from app.web import web
    app.register_blueprint(web)
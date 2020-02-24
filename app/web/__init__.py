# 蓝图分文件用
from flask import Blueprint, render_template

# 蓝图 blueprint，用来图来注册路由，再把蓝图注册到flask app对象中
web = Blueprint('web', __name__) # 模块名称__name__
print('初始化的web蓝图'+str(id(web)))

# 统一处理404页面。aop思想，不要把一样的代码散落在各个地方
@web.app_errorhandler(404)
def not_found(e):
    # 此处可以处理复杂逻辑：比如 记录日志等
    return render_template('404.html'), 404

# 注册book模块
from app.web import book
# import app.web.book 这种方式也可以
from app.web import auth
from app.web import drift
from app.web import errors
from app.web import gift
from app.web import main
from app.web import passenger
from app.web import wish

# 注册user模块
from app.web import user
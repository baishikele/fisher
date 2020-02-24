# secure配置文件存储内容：1，包含机密文件密码等   2，生产环境和开发环境不同配置

# config文件变量都大写
DEBUG = False
# SQLALCHEMY_DATABASE_URI这个要原方不动的写对，cymysql是数据库驱动
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:123456@localhost:3306/fisher'
SECRET_KEY = 'ththththth'



# Email 配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = '38020858@qq.com'
MAIL_PASSWORD = 'angnkewaczmscbbh'
#   cpicxyukelgdbiej
MAIL_SUBJECT_PREFIX = '[鱼书]'
MAIL_SENDER = '鱼书 <hello@yushu.im>'

from .base import Base, db
from sqlalchemy import Column, Integer, String, Float, Boolean
# 加密用
from werkzeug.security import generate_password_hash, check_password_hash
# cookie
from flask_login import UserMixin

from app import login_manager

from app.libs.helper import isbn_or_key
from app.spider.yushu_book import YuShuBook
from app.models.gift import Gift
from app.models.wish import Wish
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

# User类继承自 UserMixin，所以不需要自己再实现 哪个字段写入cookie了
class User(UserMixin, Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0) # 鱼豆：上传一本书获得0.5个鱼豆；成功送出1个鱼豆；获得一本书减少1个鱼豆
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    # password进行另外的操作，所以用了setter和getter方法，hasattr方法password返回的是true
    _password = Column('password', String(128), nullable=False)

    # getter
    @property
    def password(self):
        return self._password

    # setter
    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    # 检查密码是否相同
    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    # User类继承自 UserMixin，所以不需要自己再实现 哪个字段写入cookie了
    # def get_id(self):
    #     return self.id

    # 书是否可以添加到赠送清单里
    def can_save_to_list(self, isbn):
        if isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first: # 如果这本书不在鱼书api后台里
            return False
        # 如果这本书已经在赠送中（没有赠送完成）
        gift = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        # 如果这本书已经被这个用户添加到心愿单里
        wish = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        if gift or wish:
            return  False
        else:
            return True

    # 生成带id的token
    def generate_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    # 根据token取出id重置密码
    @classmethod
    def reset_password(cls, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get(uid)
            user.password = new_password
        return True

@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
from .base import Base, db
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, func
from sqlalchemy.orm import relationship
from .book import Book
from flask import current_app
from flask_login import current_user
from app.spider.yushu_book import YuShuBook

class Gift(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    # 因为本项目没有本地存储book数据，所以用isbn
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))
    # 赠送流程是否完成
    launched = Column(Boolean, default=False)

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book

    # 首页用的数据
    @classmethod
    def recent(cls):
        gifts = Gift.query.filter_by(launched=False).limit(
            current_app.config['RECENT_BOOK_PER_PAGE']).all()
        return [Book.book(gift.isbn) for gift in gifts]


    # 获取某个用户正在送出的礼物
    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query.filter_by(launched=False, uid=uid).all()
        return gifts

    # sql!!!!!根据isbn列表去wish表查询，分组查数量
    @classmethod
    def get_wish_count(cls, isbn_list):
        result_puple = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched==False,Wish.status==1,Wish.isbn.in_(isbn_list)).\
            group_by(Wish.isbn).all()
        # puple转dict
        result_dict = [{'count': w[0], 'isbn': w[1]} for w in result_puple]
        return result_dict


from app.models.wish import Wish

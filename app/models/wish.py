from .base import Base, db
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, func
from sqlalchemy.orm import relationship
from app.spider.yushu_book import YuShuBook

class Wish(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    # 因为本项目没有本地存储book数据，所以用isbn
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))
    launched = Column(Boolean, default=False)

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book

    @classmethod
    def get_wishes_by(cls, uid):
       return Wish.query.filter_by(uid=uid, launched=False).all()

    # gift表查分组统计
    @classmethod
    def get_gifts_count(cls, isbn_list):
        result_puple = db.session.query(func.count(Gift.id), Gift.isbn).filter(
                          Gift.launched==False, Gift.status==1,
                          Gift.isbn.in_(isbn_list)).group_by(Gift.isbn).all()
        result_dict = [{'count': w[0], 'count': w[1]} for w in result_puple]
        return result_dict

from app.models.gift import Gift

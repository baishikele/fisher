from sqlalchemy import Column, Integer, String #基础包

from app.models.base import Base
from app.spider.yushu_book import YuShuBook

# mvc中的m层。有种思路：先不考虑数据库设计，先考虑业务，由业务驱动生成数据库
# code first 和orm区别：code first只注重生成表， orm概念更广泛，增删改查
class Book(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column('author', String(30), default='未名')
    binding = Column(String(20))
    publisher = Column(String(50))
    price = Column(String(20))
    pages = Column(Integer)
    pubdate = Column(String(20))
    isbn = Column(String(15), nullable=False, unique=True)
    summary = Column(String(1000))
    image = Column(String(50))

    @classmethod
    def book(cls, isbn):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        return yushu_book.first
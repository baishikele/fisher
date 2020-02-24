
from app.libs.httper import HTTP
from flask import current_app #类似于 request，代理模式实现

# 面向对象：在这里整理了数据结构，因为isbn和keyword查询出来的结构是不一样的
# 这里并没有把dict转为对象，这是viewmodel的工作，这里只是把结构统一
class YuShuBook():
    # 变量字符串可以包含变量，用{}
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        self.keyword = ''
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        result = HTTP.get(url)
        self.keyword = isbn
        self.total = 1
        self.books.append(result)

    def search_by_keyword(self, keyword, page):
        url = self.keyword_url.format(keyword, current_app.config['PER_PAGE'], self.__caculate_start(page))
        retult = HTTP.get(url)
        self.keyword = keyword
        self.total = retult['total']
        self.books = retult['books']

    @property
    def first(self):
        return self.books[0] if self.total>=1 else None

    def __caculate_start(self, page):
        return current_app.config['PER_PAGE'] * (page-1)
# “面向过程”
class _YuShuBook(object):
    # 变量字符串可以包含变量，用{}
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    @classmethod
    def search_by_isbn(cls, isbn):
        url = cls.isbn_url.format(isbn)
        result = HTTP.get(url) # json string
        return result

    @classmethod
    def search_by_keyword(cls, keyword, page):
        url = cls.keyword_url.format(keyword, current_app.config['PER_PAGE'], cls.caculate_start(page))
        result = HTTP.get(url, False)
        return result

    @staticmethod
    def caculate_start(page):
        return current_app.config['PER_PAGE'] * (page-1)
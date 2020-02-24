# from fisher__deprecated import app
from app.libs.helper import isbn_or_key
from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookCollection, BookViewModel
from . import web # 引入__init__下的web对象
from flask import request
from app.forms.book import SearchForm #校验url参数
from flask import jsonify, flash, render_template
from flask_login import current_user
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.trade import TradeInfo

import json
print('注册的web蓝图'+str(id(web)))

# 这种方式不优雅
# @web.route('/book/search/<q>/<page>')

@web.route('/book/search')
def search():
    # request是flask提供的对象，使用request需要注意是否在视图函数的上下文中触发的
    form = SearchForm(request.args)
    books = BookCollection()
    if form.validate():
        q = form.q.data.strip() # 这里通过form获取q，而不通过request.args['q']获取，是因为验证层可能会有默认值
        page = form.page.data
        yushu_book = YuShuBook() # dict结构
        if isbn_or_key(q) == 'key':
            # result = YuShuBook.search_by_keyword(q, page)
            yushu_book.search_by_keyword(q, page)
        else:
            # result = YuShuBook.search_by_isbn(q)
            yushu_book.search_by_isbn(q)
        books.fill(yushu_book, q) # viewmodel
        # return books, 200, {'content-type': 'application/json'}

    else:
        # 检验不通过的error这里是在form对象里，另外一般库是放在异常里抛出来的
        # return jsonify(form.errors)
        #
        flash('没有找到搜索内容')
    # 对象序列化成字典，递归，对于对象里属性又是对象，用lambda表达式进行转换
    # return json.dumps(books, default=lambda o: o.__dict__)
    return render_template('search_result.html', books=books)

@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    # 1，详情书籍信息
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book_view_model = BookViewModel(yushu_book.first)

    # 2，这本书是否在我的gift中
    has_in_gift = False
    has_in_wish = False
    if current_user.is_authenticated:
        gifts = Gift.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).all()
        if gifts:
            has_in_gift=True

        wishes = Wish.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).all()
        if wishes:
            has_in_wish=True

    trade_gifts = Gift.query.filter_by(launched=False, isbn=isbn).all()
    trade_gifts_model = TradeInfo(trade_gifts)
    trade_wishes = Wish.query.filter_by(launched=False, isbn=isbn).all()
    trade_wishes_model = TradeInfo(trade_wishes)
    return render_template('book_detail.html', book=book_view_model, has_in_gifts=has_in_gift,
                           has_in_wishes=has_in_wish,
                           wishes=trade_wishes_model,
                           gifts=trade_gifts_model)
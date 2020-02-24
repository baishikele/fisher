from . import web
from app.models.gift import Gift
from app.view_models.book import BookViewModel
from flask import render_template

@web.route('/')
def index():
    books = Gift.recent()
    recent = [BookViewModel(book) for book in books]
    return render_template('index.html', recent=recent)
# 1，最近30条
# 2，倒序
# 3，去重
# 4，礼物表，book表
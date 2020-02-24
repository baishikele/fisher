from . import web
from flask_login import login_required, current_user
from app.models.gift import Gift
from app.models.base import db
from flask import current_app, redirect, url_for, flash, render_template
from app.models.user import User
from app.view_models.book import BookViewModel
from app.view_models.gift import MyGifts

@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gift(isbn):
    if current_user.can_save_to_list(isbn):
        '''
        # 事务
        try:
            gift = Gift()
            gift.isbn = isbn
            # User模型里实现的方法
            gift.uid = current_user.id
            # 加鱼豆
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)
            # 上面操作了两张表，SQLAlchemy天然支持事务
            db.session.commit()
        except Exception as e: # 如果不回滚，那么这次和后续的插入都会失败
            db.session.rollback()
            raise e
        '''
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            # User模型里实现的方法
            gift.uid = current_user.id
            # 加鱼豆
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)
    else:
        flash('你当前有赠送这本书或你心愿清单里有这本书')

    return redirect(url_for('web.book_detail', isbn=isbn))

@web.route('/my/gifts')
@login_required
def my_gifts():
    gifts_of_mine = Gift.get_user_gifts(current_user.id) # gift model
    isbn_list = [gift.isbn for gift in gifts_of_mine] # [str]
    wish_count_list = Gift.get_wish_count(isbn_list) # [dict]
    my_gifts_view_model = MyGifts(gifts_of_mine, wish_count_list)
    return render_template('my_gifts.html', gifts=my_gifts_view_model.gifts)

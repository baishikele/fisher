from . import web
from flask_login import current_user, login_required
from flask import redirect, flash, url_for, render_template
from app.models.wish import Wish
from app.models.base import db
from app.view_models.wish import MyWishes
@web.route('/my/wish')
@login_required
def my_wish():
    # 1,wish表查wishes
    # 2.isbn_list
    # 3，gift表查x人要送
    wishes = Wish.get_wishes_by(current_user.id)
    isbn_list = [wish.isbn for wish in wishes]
    gifts_count = Wish.get_gifts_count(isbn_list)
    my_wishes = MyWishes(wishes, gifts_count)
    return render_template('my_wish.html', wishes=my_wishes.wishes)

@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        wish = Wish()
        wish.isbn = isbn
        wish.uid = current_user.id
        with db.auto_commit():
            db.session.add(wish)
    else:
        flash('你当前有赠送这本书或你心愿清单里有这本书')
    return redirect(url_for('web.book_detail', isbn=isbn))

from . import web
from flask_login import login_required
@web.route('/pending')
def pending():
    pass


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    return '123'
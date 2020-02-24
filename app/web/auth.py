from app.libs.email import send_email
from . import web
from flask import render_template, request, redirect, url_for, flash
from app.forms.auth import RegisterForms, LoginForms, EmailForms, PasswordField
from app.models.user import User
from app.models.base import db
from flask_login import login_user, logout_user

@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))

# 通过get展示模板，post提交数据
@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForms(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
        user.set_attrs(form.data)# 动态赋值
        '''
        # 存入数据库
        db.session.add(user)
        db.session.commit()
        '''
        with db.auto_commit():
            db.session.add(user)
            
        return redirect(url_for('web.login'))
    return render_template('auth/register.html', form=form)

@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForms(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            # 用flask插件管理cookie，主要是写入id。具体见user模型继承的父类
            # 默认关闭浏览器就删除cookie
            login_user(user, remember=True)
            # 取url的next值进行重定向到用户本来想去的地址
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('账号或者密码不对')
    return render_template('auth/login.html', form={'data':{}})

@web.route('/forget_password_request', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForms(request.form)
    if request.method == 'POST':
        if form.validate():
            # first_or_404 自动抛出异常，不用手动raise exception，可用try定制自己的404页面
            # try:
                user = User.query.filter_by(email=form.email.data).first_or_404()
            # except Exception as e:
            #     return render_template('404.html')
                if user:
                    send_email(to=form.email.data, subject='重置你的密码', template='email/reset_password.html',
                               user=user, token=user.generate_token())
    return render_template('auth/forget_password_request.html', form=form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = PasswordField(request.form)
    if request.method == 'POST' and form.validate():
        success = User.reset_password(token, form.password1.data)
        if success:
            flash('密码已更新，请重新登录')
            redirect(url_for('web.login'))
        else:
            flash('密码重置失败')
    return render_template('auth/forget_password.html')
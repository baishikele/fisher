from flask_mail import Message
from app import mail
from flask import current_app, render_template

def send_email(to, subject, template, **kwargs):
    # msg = Message('测试邮件', sender='38020858@qq.com', body='test body',
    #               recipients=['38020858@qq.com'])
    msg = Message('[鱼书]' + ' ' + subject, sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template(template, **kwargs)
    mail.send(msg)
from wtforms import Form, StringField, IntegerField, PasswordField
from wtforms.validators import Length, NumberRange, DataRequired, Email, ValidationError, EqualTo
from app.models.user import User
from app.models.base import db

class RegisterForms(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64),
                                    Email(message='电子邮箱不符合规范')])
    password = PasswordField(validators=[DataRequired(message='密码不可以为空，请输入您的密码'),
                                         Length(6, 32)])
    nickname = StringField(validators=[DataRequired(),
                                       Length(2,10, message='昵称至少需要两个字符，最多10个字符')])

    # 业务方面的校验
    def validate_email(self, field):
        # db.session
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮件已被注册')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已经存在')


class LoginForms(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64),
                                    Email(message='电子邮箱不符合规范')])
    password = PasswordField(validators=[DataRequired(message='密码不可以为空，请输入您的密码'),
                                         Length(6, 32)])

class EmailForms(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64),
                                    Email(message='电子邮箱不符合规范')])

class ResetPasswordForm(Form):
    password1 = PasswordField(validators=[DataRequired(),
                                          Length(6, 32, message='密码长度至少需要3到32个字符之间'),
                                          EqualTo('password2', message='两次输入的密码不相同')])
    password2 = PasswordField(validators=[DataRequired(), Length(6, 32)])
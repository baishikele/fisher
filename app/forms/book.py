from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, data_required


class SearchForm(Form):
    # 一个方法里使用多个验证器
    q = StringField(validators=[data_required(), Length(min=1, max=30, message='查询条件不合法')])
    page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)
    '''
    {
        "page": [
            "Number must be between 1 and 99."
        ],
        "q": [
            "查询条件不合法"
        ]
    }
    '''
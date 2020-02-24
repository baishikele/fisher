from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery  # flask包里
from sqlalchemy import Column, SmallInteger, Integer
from contextlib import contextmanager
from datetime import datetime

class SQLAlchemy(_SQLAlchemy):

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

# 重写父类的query方法，加入自己想要的查询条件
class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    # 这个属性是让sqlalchemy知道不要创建base表
    __abstract__ = True
    # 软删除
    status = Column(SmallInteger, default=1)
    # 数据库新增字段怎么办？？》
    create_time_ = Column(Integer)
    def __init__(self):
        self.create_time_ = int(datetime.now().timestamp())

    @property
    def create_time(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time_)
        else:
            return None

    # 动态赋值：把字段转成对象属性（key值和属性名称相同）
    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)



# !!!!!!注意base模块和book等业务模块引入顺序，这个bug卡了半天
# from app.models import book
# from app.models import user
# from app.models import gift

# python编写代码circular import问题
# https://blog.csdn.net/weixin_40107510/article/details/90320939
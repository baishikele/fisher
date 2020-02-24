from flask import Flask, current_app


app = Flask(__name__)

context = app.app_context()
context.push()
current_app.config['DEBUG']
context.pop()

# 上面更优雅的写法用with语句
with app.app_context():
    current_app.config['DEBUG']

# 一个请求过来，会生成包含Request对象的上下文对象request_context，request_context
# 进栈之前会检查app_context_stack里是否有app_context上下文对象，如果没有系统会添加一个


# flask有两个栈，app_context_stack和request_context_stack，里面都是对应的上下文对象，上下文对象包含app和request
# 为什么栈内不直接加入app对象和request对象？因为上下文中还有其他属性

# 离线应用和单元测试可能会自己手动往app栈内添加上下文，如果从浏览器和postman请求就不需要



# flask上下文和with语句

class MyResource:
    def __enter__(self):
        print('连接资源')
        return self

    # exit函数需要后面的几个参数，否则无法进入这个函数
    def __exit__(self, exc_type, exc_val, exc_tb):
        print('关闭资源')
        if exc_tb:
            print('exit有异常')
        else:
            print('exit没有异常')
        return True #return true 表示异常在exit里处理完了，不需要外面再次处理,如果什么都不返回，那么就是return none
try:
    with MyResource() as obj_a: # as 后面的对象不是管理器的实例对象，而是__enter__ return的对象
        # 1/0 #模拟异常
        print(obj_a)
except Exception as exp:
    print('外面处理异常')


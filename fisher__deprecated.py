# 在setting里设置虚拟环境的默认解释器
from flask import Flask, make_response

app = Flask(__name__)
# flask自己有一个变量可以读取配置，参数传配置的路径，key值必须都大写
app.config.from_object('config')
print(id(app))

#imprt后面接的是 模块, (1,book模块需要app对象，2，fisher主文件需要执行book代码)
# 会产生循环引用！！！！！！通过蓝图解决
# from app.web import book

# 下面的视图函数分流到app web book模块里去了

# 路由装饰器底层也是调用add_url_rule函数
@app.route('/hello')
def hello(): #这就是视图函数，mvc里的controller
    headers = {
        # 'content-type': 'application/json'
        'content-type': 'text/plain',
        'location': 'www.baidu.com'
    }
    response = make_response('<html></html>', 200)
    response.headers = headers
    return response
    # return '<html></html>', 200, headers

'''

# 下面的是弃用的，重构前的代码
@app.route('/book_/search/<q>/<page>')
def search_change(q: str, page: str):
    # 关键字搜索和bn搜索，bn搜索：1，13位0-9的数字组成 2，10位0-9的数字，包括 - 组成
    isbn_or_key = 'key'
    if len(q) == 13 and q.isdigit():
        isbn_or_key = 'isbn'
    short_q = q.replace('-', '')
    if '-' in q and len(q) == 10 and short_q.isdigit():
        isbn_or_key = 'isbn'
    return '123'

# 重构上面的函数
@app.route('/book/search/<q>/<page>')
def search(q: str, page='1'):
    result = ''
    if isbn_or_key(q) == 'key':
        result = YuShuBook.search_by_keyword(q, page)
    else:
        result = YuShuBook.search_by_isbn(q)
    return result, 200, {'content-type': 'application/json'}
    # {"books": [{"author": ["\u8463\u4f1f\u660e"], "binding": "\u5e73\u88c5", "category": "\u7f16\u7a0b", "id": 261,
    #             "image": "https://img1.doubanio.com/lpic/s28994368.jpg",
    #             "images": {"large": "https://img1.doubanio.com/lpic/s28994368.jpg"}, "isbn": "9787121297335",
    #             "pages": "504", "price": "105", "pubdate": "2016-9-15",
    #             "publisher": "\u7535\u5b50\u5de5\u4e1a\u51fa\u7248\u793e", "subtitle": "", "summary":
    # return result

    # flask自带的json序列化函数，效果和下面自己封装成元组的形式一样，甚至更丰富一些
    # "{\n \"books\": [\n {\n \"author\": [\n \"\\u8463\\u4f1f\\u660e\"\n ], \n \"binding\": \"\\u5e73\\u88c5\", \n \"category\": \"\\u7f16\\u7a0b\", \n \"id\": 261, \n \"image\": \"https://img1.doubanio.com/lpic/s28994368.jpg\", \n \"images\": {\n \"large\": \"https://img1.doubanio.com/lpic/s28994368.jpg\"\n },
    # return jsonify(result)

    # return json.dumps(result), 200, {'content-type': 'application/json'}


# 注意修改url路由后，要清理浏览器缓存
@app.route('/say/')
def say():
    return 'say hello, 大叔!'


def hi():
    return 'hi,大叔'


app.add_url_rule('/hi', view_func=hi)
'''
# 为什么加这个判断?加了这个判断只有在这个文件作为项目入口的时候才开启服务，如果是被导入那么不进入判断
# 生产环境的时候是nginx+uwsgi，uwsgi本身就是一个服务，如果再开启一个flask服务就不可以了
if __name__ == '__main__':
    # debug：debug模式优点：1，可以实时监听文件改动，不用反复重启服务2，又友好的调试log
    # host：如果不传host那么局域网都不能访问这台机器开启的服务
    # config是从flask里面读取的
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=81)

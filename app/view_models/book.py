

# 把dict转为对象返回给调用者（视图函数）
class BookViewModel:

    def __init__(self, data):
        self.title = data['title']
        self.author = ','.join(data['author'])
        self.binding = data['binding']
        self.publisher = data['publisher']
        self.image = data['images']['large']
        self.price = data['price']
        self.isbn = data['isbn']
        self.pubdate = data['pubdate']
        self.summary = data['summary']
        self.pages = data['pages']

    # 属性拼接，在模板里比较麻烦，所以在viewmodel里拼接完，模板直接用
    # func转属性
    @property
    def intro(self):
        intros = filter(lambda x: True if x else False,
                        [self.author, self.publisher, self.price])
        return '/'.join(intros)


class BookCollection:

    def __init__(self):
        self.total = 0
        self.keyword = ''
        self.books = []

    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.keyword = yushu_book.keyword
        self.books = [BookViewModel(book) for book in yushu_book.books]

# viewmodel层，把原始数据加工一下再返回客户端
class _BookViewModel:

    @classmethod
    def package_single(cls, data, keyword):
        # 先定义数据结构
        returned = {
            'books' : [],
            'total' : 0,
            'keyword' : keyword
        }
        if data:
            returned['books'] = [cls.__cut_book_data(data)]
            returned['total'] = 1
        return returned

    @classmethod
    def package_collection(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            # for book in data['books']:
            #     new_book = cls.__cut_book_data(book)
            #     returned['books'].append(new_book)
            # 替代上面的for循环，更优雅，列表推导式
            returned['books'] = [cls.__cut_book_data(book) for book in data['books']]
            returned['total'] = len(data['books'])
        return returned

    @classmethod
    def __cut_book_data(cls, data):
        book = {
                'title': data['title'],
                'author': '、'.join(data['author']),
                'binding': data['binding'],
                'publisher': data['publisher'],
                'image': data['images']['large'],
                'price': data['price'],
                'isbn': data['isbn'],
                'pubdate': data['pubdate'],
                'summary': data['summary'],
                'pages': data['pages']
        }
        return book
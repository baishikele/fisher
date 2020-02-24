from app.view_models.book import BookViewModel


class MyWish:
    def __init__(self, book, wishes_count):
        self.wishes_count = wishes_count
        self.book = book

class MyWishes:

    # [model]  [dict]
    def __init__(self, wishes, wishes_count):
        self.__wishes = wishes
        self.__wishes_count = wishes_count
        self.wishes = wishes
        self.wishes=self.__parse()

    def __parse(self):
        temp_list = []
        for wish in self.__wishes:
            temp_list.append(self.__get_single(wish))
        return temp_list

    def __get_single(self, wish):
        count = 0
        for wish_count in self.__wishes_count:
            if wish_count['isbn'] == wish.isbn:
                count = wish_count['count']
        return MyWish(BookViewModel(wish.book.first), count)



from app.view_models.book import BookViewModel

class MyGift:
    def __init__(self, book, wishes_count):
        self.book = book
        self.wishes_count = wishes_count


class MyGifts:
    # [model], [str]
    def __init__(self, gifts_of_mine, wishes_count_list):
        self.gifts = []

        self.__gifts_of_mine = gifts_of_mine
        self.__wishes_count_list = wishes_count_list
        self.gifts = self.__parse()

    def __parse(self):
        tempList = []
        for gift in self.__gifts_of_mine:
            tempList.append(self.__matching(gift))
        return tempList

    # gift:model
    def __matching(self, gift):
        count = 0
        for wish in self.__wishes_count_list:
            if wish['isbn'] == gift.isbn:
                count = wish['count']
        my_gift = MyGift(book=BookViewModel(gift.book.first), wishes_count=count)
        return my_gift
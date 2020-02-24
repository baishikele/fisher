
def isbn_or_key(word: str):
    isbn_or_key = 'key'
    if len(word) == 13 and word.isdigit():
        isbn_or_key = 'isbn'
    short_q = word.replace('-', '')
    if '-' in word and len(word) == 10 and short_q.isdigit():
        isbn_or_key = 'isbn'
    return isbn_or_key
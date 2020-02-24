

from contextlib import contextmanager

@contextmanager
def auto_commit():
    print('aaaa')
    yield 'cccc'
    print('bbbb')

with auto_commit() as r:
    print(r)
    print('3333')
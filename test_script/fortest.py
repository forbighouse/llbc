class Block(object):

    def __init__(self, header, transactions=None):
        print('this is ')
        self._header = header
        self.transactions = transactions or []

    def a1(self):
        print(self._header)

    def b1(self):
        print(self.transactions)


if __name__ == '__main__':
    a = ['1', '2', '3']
    b = 'test header'
    c = Block(b, a)
    c.a1()

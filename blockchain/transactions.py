

class Transaction(object):

    def __init__(self, to, value, data, sig):
        self.to = to
        self.value = value
        self.data = data
        self.sig = sig

    def hash(self):
        # rlp
        # Todo
        return [self.to,
                self.value,
                self.sig,
                self.data]


class TransactionOffset(object):
    def __init__(self, vin, offset):
        self._vin = vin
        self._offset = offset
        try:
            self.data()
        finally:
            print("rating translate %s" % self._vin)

    def data(self):
        return [
            self._vin,
            self._offset
        ]
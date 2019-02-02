

class BlockHeader(object):

    # ('prevhash', hash32),
    # ('coinbase', address),
    # ('difficulty', big_endian_int),
    # ('timestamp', big_endian_int),

    def __init__(self, block_id, pre_hash, coin_base, difficulty, timestamp):
        self._pre_hash = pre_hash
        self._coin_base = coin_base
        self._difficult = difficulty
        self._timestamp = timestamp

    def hash(self):
        return


class Block(object):

    def __init__(self, header, transactions=None):
        self._header = header
        self.transactions = transactions or []

    @property
    def tansaction_count(self):
        return len(self.transactions)


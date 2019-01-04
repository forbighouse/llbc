

class Observation(object):

    fields = [
        ('prevhash', hash32),
        ('uncles_hash', hash32),
        ('coinbase', address),
        ('state_root', trie_root),
        ('tx_list_root', trie_root),
        ('receipts_root', trie_root),
        ('bloom', int256),
        ('difficulty', big_endian_int),
        ('number', big_endian_int),
        ('gas_limit', big_endian_int),
        ('gas_used', big_endian_int),
        ('timestamp', big_endian_int),
        ('extra_data', binary),
        ('mixhash', binary),
        ('nonce', binary)
    ]

    def __init__(self):
        self.observe_time = 0
        self.observe_event = 0
        self.observe_zone = 0
        self.node_list = []

    def get_time(self):
        return self.observe_time

    def get_zone(self):
        return self.observe_zone
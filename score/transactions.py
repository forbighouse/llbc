

class Transaction(object):

    def __init__(self, observations):
        self.to = 0x0
        self.data = self.serialize(observations)

    def parse(self):
        # rlp
        # Todo
        return

    def serialize(self, observations):
        return observations.get_time()


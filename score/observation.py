

class Observation():

    def __init__(self):
        self.observe_time = 0
        self.observe_event = 0
        self.observe_zone = 0
        self.node_list = []

    def get_time(self):
        return self.observe_time

    def get_zone(self):
        return self.observe_zone
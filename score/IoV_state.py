# import numpy as np
from score.nodemanager import ServiceNode

IOV_STATE_DEFAULTS = {
    "vehicles": []
}


class DistanceManger(object):
    _could_linked_set = dict()
    def __init__(self,):
        self.veh_id = 0
        self.veh_graph = dict()
        self.veh_sets = {'A': 1}

    def _create_distance_adjacency_matrix(self):
        self.veh_graph.update({'A': ['B', 'C'],
                               'B': ['A', 'D'],
                               'C': ['A', 'E'],
                               'D': ['B', 'D'],
                               'E': ['C']})

    def distance_valiate(self, x):
        print(x.veh_id)

    def could_linked_set(self):
        return self._could_linked_set


import numpy as np
from score.nodemanager import ServiceNode



IOV_STATE_DEFAULTS = {
    "vehicles": []
}

IOV_LISTENING_MESSAGE = {
    "time": 0,
    "veh_id": '01',
    "location": [1, 1]
}

IOV_LOCAL_MESSAGE = {
    "time": 0,
    "veh_id": '02',
    "location": [0, 1]
}



def distenance_calculate(locC, locR):
    return np.linalg.norm(np.array(locC) - np.array(locR))


class DistanceManger(object):

    def __init__(self, remote_veh_id, remote_location, remote_time):
        self.veh_id = IOV_LOCAL_MESSAGE["veh_id"]
        self.remote_veh_id = remote_veh_id
        self.remote_location = remote_location
        self.remote_time = remote_time
        self.veh_graph = dict()
        self.veh_sets = {'A': 1}

    def _create_distance_adjacency_matrix(self):
        self.veh_graph.update({'A': ['B', 'C'],
                               'B': ['A', 'D'],
                               'C': ['A', 'E'],
                               'D': ['B', 'D'],
                               'E': ['C']})

    def _a(self):
        wait_update = {self.veh_id: }

    def distance_valiate(self, x):
        print(x.veh_id)

    def could_linked_set(self):
        return self._could_linked_set


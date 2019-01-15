import numpy as np
from score.nodemanager import ServiceNode

STATE_DEFAULTS = {
    "time": 0,
    "ADJ_NODE_MATRIX":{},
    "ADJ_DIS_MATRIX": {}
}


class Message(object):
    pass


class IoVMessage(Message):

    def __init__(self, time, veh_id, location):
        self._time = time
        self._veh_id = veh_id
        self._location = location

    @property
    def time(self):
        return self._time

    @property
    def veh_id(self):
        return self._veh_id

    @property
    def location(self):
        return self._location


IOV_STATE_DEFAULTS = {
    "vehicles": []
}


def distance_cal(loc1, loc2):
    return np.linalg.norm(np.array(loc1) - np.array(loc2))


def adjacency_item(msg1, msg_set):
    assert isinstance(msg1, IoVMessage)
    return {msg1.veh_id: dis_list(msg1, msg_set)}


def dis_list(msg1, msg_set):
    dis_set = []
    node_set = []
    if msg_set:
        for i in msg_set:
            dis_set.append(distance_cal(msg1.location, i.location))
            node_set.append(i.veh_id)
        return {msg1.veh_id: node_set}, {msg1.veh_id: dis_set}
    else:
        return


def c(msg_dict, msg_set):
    msg_dict.update(msg_set)


class DistanceManger(object):

    def __init__(self, remote_veh_id, remote_location, remote_time):
        self.veh_id = IOV_LOCAL_MESSAGE["veh_id"]
        self.remote_veh_id = remote_veh_id
        self.remote_location = remote_location
        self.remote_time = remote_time
        self.veh_graph = dict()
        self.veh_sets = {'A': 1}

    def _create_distance_adjacency_matrix(self):
        self.veh_graph.update({'A': [{'B': 1}, {'C': 2}],
                               'B': ['A', 'D'],
                               'C': ['A', 'E'],
                               'D': ['B', 'D'],
                               'E': ['C']})


    def distance_valiate(self, x):
        print(x.veh_id)


    def could_linked_set(self):
        return self._could_linked_set


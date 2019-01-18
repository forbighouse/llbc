import numpy as np
import time

STATE_DEFAULTS = {
    "time": 0,
    "ADJ_NODE_MATRIX": {},
    "ADJ_DIS_MATRIX": {}
}


class Message:
    _fields = []

    def __init__(self, *args):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        for name, value in zip(self._fields, args):
            setattr(self, name, value)


# 车辆发出的消息格式
class IoVSendMessage(Message):
    _fields = ['send_time', 'veh_id', 'location']

    def send(self):
        return self.send_time, self.veh_id, self.location


class IoVRecvMessage(Message):
    _fields = ['current_time', 'send_time', 'veh_id', 'location']

    def recv(self):
        return self.current_time, self.send_time, self.veh_id, self.location


def revc_message(message):
    s = time.time(), message[0], message[1], message[2]
    return s


IOV_STATE_DEFAULTS = {
    "vehicles": []
}


# 计算一个节点与它的地理位置接近的其他节点的邻接表
# ///////////////////////////////////////////////////
def adjacency_item(msg1, msg_set):
    assert isinstance(msg1, Message)
    return {msg1.veh_id: dis_list(msg1, msg_set)}


def distance_cal(loc1, loc2):
    return np.linalg.norm(np.array(loc1) - np.array(loc2))


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
# ////////////////////////////////////////////////


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


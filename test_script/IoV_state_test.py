from score.IoV_state import *
from score.nodemanager import ServiceNode
import random

IOV_LISTENING_MESSAGE1 = IoVMessage(time=0, veh_id='01', location=[1, 0])
IOV_LISTENING_MESSAGE2 = IoVMessage(time=1, veh_id='02', location=[2, 2])
IOV_LOCAL_MESSAGE = IoVMessage(time=0, veh_id='02', location=[0, 1])

msg_set = []
msg_set.append(IOV_LISTENING_MESSAGE1)
msg_set.append(IOV_LISTENING_MESSAGE2)

def iov_state_test():
    node1 = ServiceNode(node_type=1,
                        veh_id='001',
                        longitude=123,
                        latitude=321,
                        observe_vehs=[],
                        current_time=12)

    d, e = dis_list(IOV_LOCAL_MESSAGE, msg_set)
    print(d)
    print(e)

    # veh_id = 'A'
    # node1 = DistanceManger(veh_id) # 需要获取可link的节点集合
    # could_link_with_set = node1.distance_valiate()
    # res_tag = servicenode.communicate(could_link_with_set)
    # for k in res_tag:
    #     if k.tag == True:
    #         return


def iov_test():
    x = list()
    num = range(4, 23)
    for i in range(1, 100, 5):
        x.append([random.choice(num), i])
    return x


if __name__ == "__main__":
    # iov_state_test()

    with open("location_test.txt", "w") as w:
        for i in iov_test():
            w.writelines(str(i) + '\n')

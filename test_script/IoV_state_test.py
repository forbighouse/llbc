from score.IoV_state import *
from score.nodemanager import ServiceNode


def iov_state_test():
    node1 = ServiceNode(node_type=1,
                        veh_id='001',
                        longitude=123,
                        latitude=321,
                        observe_vehs=[],
                        current_time=12)
    b = DistanceManger()
    b.distance_valiate(node1)
    # veh_id = 'A'
    # node1 = DistanceManger(veh_id) # 需要获取可link的节点集合
    # could_link_with_set = node1.distance_valiate()
    # res_tag = servicenode.communicate(could_link_with_set)
    # for k in res_tag:
    #     if k.tag == True:
    #         return

if __name__ == "__main__":
    iov_state_test()

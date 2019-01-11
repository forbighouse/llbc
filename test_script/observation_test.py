from score.observation import Observation
from score.nodemanager import ServiceNode

def test_ob():
    # exam_obs = [
    #     {'zone': 0, ' section': 'a', 'event': 'accident', 'time': 1},
    #     {'zone': 2, ' section': 'b', 'event': 'light', 'time': 2},
    #     {'zone': 2, ' section': 'd', 'event': 'accident', 'time': 1},
    #     {'zone': 1, ' section': 'a', 'event': 'light', 'time': 2},
    #     {'zone': 4, ' section': 'c', 'event': 'accident', 'time': 2},
    #     {'zone': 7, ' section': 'd', 'event': 'accident', 'time': 3},
    # ]
    # 位置txt
    # 10分钟
    ServiceNode(node_type=1, veh_id='001', longitude=123, latitude=321, observe_vehs=[], current_time=12)
    # veh_traj = [
    #     {'veh_id': 0, 'longitude': 0, 'latitude': 0, 'observe_vehs': 'accident', 'current_time': 1},
    #     {'zone': 2, ' section': 'b', 'event': 'light', 'time': 2},
    #     {'zone': 2, ' section': 'd', 'event': 'accident', 'time': 1},
    #     {'zone': 1, ' section': 'a', 'event': 'light', 'time': 2},
    #     {'zone': 4, ' section': 'c', 'event': 'accident', 'time': 2},
    #     {'zone': 7, ' section': 'd', 'event': 'accident', 'time': 3},
    # ]
    ServiceNode.showfield()

    #
    # a = Observation()
    # b = Observation(000, '000', '111', 'light')
    # print()


if __name__ == '__main__':
    test_ob()

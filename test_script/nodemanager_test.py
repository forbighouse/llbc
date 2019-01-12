from score.nodemanager import ServiceNode


def test_nm():
    node1 = ServiceNode(node_type=1,
                        veh_id='001',
                        longitude=123,
                        latitude=321,
                        observe_vehs=[],
                        current_time=12)
    node1.observe_vehicle = '123'


if __name__ == '__main__':
    test_nm()

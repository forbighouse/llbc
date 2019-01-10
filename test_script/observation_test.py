from score.observation import Observation


def test_ob():


    exam_obs = [
        {'zone': 0, ' section': 'a', 'event': 'accident', 'time': 1},
        {'zone': 2, ' section': 'b', 'event': 'light', 'time': 2},
        {'zone': 2, ' section': 'd', 'event': 'accident', 'time': 1},
        {'zone': 1, ' section': 'a', 'event': 'light', 'time': 2},
        {'zone': 4, ' section': 'c', 'event': 'accident', 'time': 2},
        {'zone': 7, ' section': 'd', 'event': 'accident', 'time': 3},
    ]
    # 位置txt
    # 10分钟


    a = Observation()
    b = Observation(000, '000', '111', 'light')
    print()


if __name__ == '__main__':
    test_ob()

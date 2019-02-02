from score.IoV_state import IoVSendMessage
import random
import uuid


# 读取位置信息，生成广播消息
def file_location(files):
    gen = []
    with open(files, 'r') as f:
        locations = f.readlines()
    for i in range(0, len(locations)):
        locations[i] = locations[i].rstrip('\n')
        a = locations[i].split(',')
        # gen.append((a[0][1:], a[1][:-2]))
        gen.append((a[0][1:], a[1][:-1]))
    return gen


# 随机产生若干个accident，每一个可以保持一段时间
def accident_factory():
    """
    :return:  set=([id, timer])
    """
    ACCIDENT_NUM = 10
    accident_set = set()
    for i in range(ACCIDENT_NUM):
        accident_set.add((i, random.randint(1, 100)))
    return accident_set


# 随机产生一条轨迹，轨迹必须是单调的，可以递增也可以递减
def trajectory():
    veh_num = 50
    # rsu_num = 20
    # road_len = 2000
    time_len = 200000
    start_point = random.sample(range(time_len), 50)
    veh_trajectory = []
    for i in range(veh_num):
        veh_id = uuid.uuid3(uuid.NAMESPACE_DNS, str(i))
        # xy = range(road_len)
        veh_trajectory.append({start_point[i]: veh_id})
    return veh_trajectory




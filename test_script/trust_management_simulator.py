import uuid
import random
from score.IoV_state import distance_cal_x


ACCIDENT_NUM = 5
RSU_NUM = 20
THRESHOLD_COMMUNICATION = 300
RSU_DISTANCE = 250
veh_num = 50
# rsu_num = 20
road_len = 5000
time_len = 200000


class UploadMessage(object):
    def __init__(self, rec_veh_id, send_veh_id, m1, rating):
        self._rec_veh_id = rec_veh_id
        self._send_veh_id = send_veh_id
        self._m1 = m1
        self._rating = rating

    def pack(self):
        return [
            self._rec_veh_id,
            self._send_veh_id,
            self._m1,
            self._rating
        ]


def rsu_location():
    rsu_id_list = [uuid.uuid3(uuid.NAMESPACE_DNS, str(i)) for i in range(RSU_NUM)]
    rsu_list = [i for i in range(250, 5000, 250)]
    return dict(zip(rsu_id_list, rsu_list))


def accident_factory():
    accident_id = []
    accident_location = []
    for i in range(ACCIDENT_NUM):
        accident_id.append(str(i))
        accident_location.append((random.randint(0, road_len), 0))
    return dict(zip(accident_id, accident_location))


def veh_trajectory():
    distance_veh = random.sample(range(5, 100), 50)
    start_point = random.sample(range(5, 100), 1)
    veh_locations = []
    d = 0
    for i in distance_veh:
        d += start_point[0] + i
        veh_locations.append(d)
    veh_id_list = [uuid.uuid3(uuid.NAMESPACE_DNS, str(i)) for i in range(veh_num)]
    return dict(zip(veh_id_list, veh_locations))


def rsu_search(veh_location_s, rsu_list):
    belong_rsu_optional = []
    for rsu_id, rsu_locations in rsu_list.items():
        if abs(rsu_locations - veh_location_s) < RSU_DISTANCE:
            belong_rsu_optional.append((rsu_id, rsu_locations, abs(rsu_locations - veh_location_s)))

    def distance(elem):
        return elem[1]

    if len(belong_rsu_optional) == 2:
        belong_rsu_optional.sort(key=distance)

    return belong_rsu_optional[0]


if __name__ == '__main__':

    # 随机产生的事件的位置 dict, location
    accident_list = accident_factory()
    # accident_list = random.randint(0, road_len)

    # 随机产生的车辆位置 dict, (veh_id: location
    veh_location = veh_trajectory()

    # 每一辆车与事件的距离, list, (veh_id, distance)
    distance_list = []
    # 位置距离小于THRESHOLD_COMMUNICATION的具体距离，list, (veh_id, distance)
    vail_veh = []

    for k1, v1 in accident_list.items():
        d = []
        for k2, v2 in veh_location.items():
            d.append((k2, int(distance_cal_x(v1[0], v2))))
        distance_list.append(d)
    adjacency_list = dict(zip(list(accident_list.keys()), distance_list))

    for k, v in adjacency_list.items():
        d = []
        for v1 in v:
            if v1[1] < THRESHOLD_COMMUNICATION:
                d.append(v1)
        vail_veh.append(d)

    # 每一个rsu的位置，dict, (id, location)
    rsu_location_list = rsu_location()

    for i in vail_veh:
        for j in i:
            veh_id_single = j[0]
            veh_location_single = veh_location[veh_id_single]
            # rsu_id_single, ((rsu_id, location), distance between rsu and veh
            rsu_id_single = rsu_search(veh_location_single, rsu_location_list)




    for i in vail_veh:
        print(i)
    print('yhr')
import uuid
import random
import time
import math
from score.IoV_state import distance_cal_x


ACCIDENT_NUM = 5
RSU_NUM = 20
THRESHOLD_COMMUNICATION = 300
RSU_DISTANCE = 250
veh_num = 50
# rsu_num = 20
road_len = 5000
time_len = 200000
VEHICLE_PERCEPTION_DISTANCE = 150
ACCIDENT_TYPE = 0


#
def rate(veh_id, vec_locations, message_list, veh_location):
    """
    :param veh_id: 发出此rate的veh的id
    :param vec_locations: 发出此rate的veh的位置
    :param message_list: 收到的所有message的列表
    :return: 当前veh给所有message的评价
    """
    rating_list = []
    for veh_id, veh_locations in veh_location.items():
        veh_recv_msg = []
        for msg in message_list:
            for veh_msg_index in range(len(msg[1])):
                if veh_id != msg[1][veh_msg_index][0]:
                    msg_list = rate_collet_msg(veh_locations,
                                               veh_location[msg[1][veh_msg_index][0]], #

                                               )
                else:
                    msg_list = []
                    veh_recv_msg.append(msg_list)


        # for vehs in range(len(msg[1])):
        #     rating_list.append([veh_id, msg[1][vehs][0][0], msg[0][1], rate_rating(msg[1][vehs][0][1])])
    return rating_list

def rate_collet_msg(veh_locations, veh_send_location,):
    msg_list = []
    if abs(veh_locations - veh_send_location) < THRESHOLD_COMMUNICATION:
        msg_list.append(rate_rating(msg[1][veh_msg_index][1]))
    else:
        msg_list.append(0)


# 评分c = b + e(-γd)
def rate_rating(distance, b=0, gamma=1):
    return b + pow(math.e, ((-gamma)*distance))


def rate_condition_report(location1, location2):
    """
    :param location1: 发出此rate的veh的位置
    :param location2: accident的位置
    :return:
    """
    return abs(location1 - location2) < VEHICLE_PERCEPTION_DISTANCE


def message(vaild_veh_list, accidents, report_cycle):
    """
    :param vaild_veh_list:
    :param accidents:
    :param report_cycle: time.clock()
    :return:返回当前网络内的所有message的列表
    """
    if not len(vaild_veh_list):
        print("vaild_veh_list empty")

    message_list = []
    for index, accident_veh in enumerate(vaild_veh_list):
        accident_location = accidents[index][1][0]
        accident_type = accidents[index][2]

        if len(accident_veh):
            # 随机找1到3辆车message同一个accident
            veh_report = random.sample(accident_veh, random.randint(1, 3))
            # 给每一次message添加汇报时间
            veh_report_final = []
            for veh in range(len(veh_report)):
                # 给report_cycle添加或减少一个时间差量
                report_time = random.uniform(-1, 1)
                # 打包并重新构造添加了时间的车辆列表
                veh_report_final.append([veh_report[veh], report_cycle+report_time])
            message_list.append([[accident_location, accident_type], veh_report_final])
        else:
            veh_report = []
            message_list.append([[accident_location, accident_type], veh_report])

    return message_list


# 生成rsu的位置
def rsu_location():
    rsu_id_list = [uuid.uuid3(uuid.NAMESPACE_DNS, str(i)) for i in range(RSU_NUM)]
    rsu_list = [location for location in range(250, 5000, 250)]
    return dict(zip(rsu_id_list, rsu_list))


# 生成accident
def accident_factory():
    accident_type = ACCIDENT_TYPE
    accidents = []
    for i in range(ACCIDENT_NUM):
        accidents.append([str(i), (random.randint(0, road_len), 0), accident_type])
    return accidents


# 生成veh的位置
def veh_trajectory():
    distance_veh = random.sample(range(5, 100), 50)
    start_point = random.sample(range(5, 100), 1)
    veh_locations = []
    d_location = 0
    for i in distance_veh:
        d_location += start_point[0] + i
        veh_locations.append(d_location)
    veh_id_list = [uuid.uuid3(uuid.NAMESPACE_DNS, str(i)) for i in range(veh_num)]
    return dict(zip(veh_id_list, veh_locations))


# 返回离veh最近的rsu
def rsu_search(veh_location_s, rsu_list):
    """
    :param veh_location_s: 单一的一辆veh
    :param rsu_list: 所有的rsu的地址列表
    :return: 离veh_location_s最近的一个rsu
    """

    if not veh_location_s:
        print("No vehcile closed to accident")
        return

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

    accident_id_list = [m for m in range(ACCIDENT_NUM)]
    for v1 in accident_list:
        d = []
        for k2, v2 in veh_location.items():
            d.append((k2, int(distance_cal_x(int(v1[1][0]), v2))))
        distance_list.append(d)
    adjacency_list = dict(zip(accident_id_list, distance_list))

    for k, v in adjacency_list.items():
        d = []
        for v1 in v:
            if v1[1] < THRESHOLD_COMMUNICATION:
                d.append(v1)
        vail_veh.append(d)

    # 每一个rsu的位置，dict, (id, location)
    rsu_location_list = rsu_location()

    report_cycle = time.clock()
    #

    messages = message(vail_veh, accident_list, report_cycle)

    rating_list = []
    for veh, locations in veh_location.items():
        rating_list.append(rate(veh, locations, messages))


    for index_accident, veh_list in enumerate(vail_veh):
        message_veh = random.sample(veh_list, 1)
        for j in veh_list:
            veh_id_single = j[0]
            veh_location_single = veh_location[veh_id_single]
            # rsu_id_single, ((rsu_id, location), distance between rsu and veh
            rsu_id_single = rsu_search(veh_location_single, rsu_location_list)




    for i in vail_veh:
        print(i)
    print('yhr')
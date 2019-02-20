import uuid
import random
import time
import math
from score.IoV_state import distance_cal_x

# 仿真的事件数量
ACCIDENT_NUM = 5
# RSU的设定数量
RSU_NUM = 20
# 通信距离设定
THRESHOLD_COMMUNICATION = 300
# RSU的间距
RSU_DISTANCE = 250
# 仿真车辆的数量
VEH_NUM = 50
# 道路长度，目前只有一条直路
road_len = 5000
# 仿真时间
time_len = 200000
# 车辆感知范围，设定车辆在多近的距离才可以汇报事件
VEHICLE_PERCEPTION_DISTANCE = 150
# 事件的类型，例如车祸、红绿灯、限行、拥堵等
ACCIDENT_TYPE = 0
# 一个消息的时效性
TIME_TOLERANCE = 1
# 测试模式
DEBUG = 1
# 更新所有的txt文件
UPDATE_TXT = 0


#
def rate(message_list, veh_location):
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
            msg_list = []
            for veh_msg_index in range(len(msg[1])):
                if veh_id != msg[1][veh_msg_index][0][0]:  # 他自己也报
                    veh_for_one_msg = rate_collect_msg(veh_locations,
                                                       veh_location[msg[1][veh_msg_index][0][0]],
                                                       msg[0],
                                                       msg[1][veh_msg_index])
                    if veh_for_one_msg:
                        msg_list.append(veh_for_one_msg)
                    else:
                        continue

            # veh_recv_msg.append(veh_for_one_msg)
            if len(msg_list):
                veh_recv_msg.append(msg_list)
            else:
                veh_recv_msg.append(0)

        rating_list.append(veh_recv_msg)

        # for vehs in range(len(msg[1])):
        #     rating_list.append([veh_id, msg[1][vehs][0][0], msg[0][1], rate_rating(msg[1][vehs][0][1])])
    return rating_list


def rate_collect_msg(veh_locations, veh_send_location, msg0, msg1):
    """
    :param veh_locations: 任意一辆车的位置，其实是接收message的veh
    :param veh_send_location: 发送message的车辆的位置
    :param
    :return:
    """
    # 还应该判断消息的时效性，应该在哪判断？
    if abs(veh_locations - veh_send_location) < THRESHOLD_COMMUNICATION:
        # [汇报message的id, ,accident的位置， accident的类型，评分]
        return [msg1[0][0], msg0[0], msg0[1], rate_rating(msg1[0][1])]
    else:
        # 如果小于通信距离，当前车辆无法接收到message，所以msg_list在该车辆位置置0
        return 0


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
    rsu_id_list = [str(uuid.uuid3(uuid.NAMESPACE_DNS, str(i))) for i in range(RSU_NUM)]
    rsu_list = [location for location in range(250, 5000, 250)]
    return dict(zip(rsu_id_list, rsu_list))


# RSU收集评分
def rsu_rating_collection(send_id, recv_msg, rsu_location_list, veh_location):
    rsu_for_send = rsu_search(veh_location[send_id], rsu_location_list)
    tag_for_no_msg = 0
    upload_msg = []
    for accident in recv_msg:
        if accident[0] == 0 or accident[0] == -1:
            tag_for_no_msg += 1
        else:
            assert type(accident) is list
            for msg in accident:
                upload_msg.append([rsu_for_send[0],  # 接收的transaction的RSU
                                   send_id,  # 发送这个transaction的veh
                                   msg[0],   # 报告message的veh
                                   msg[2],   # 报告的事件类型
                                   msg[3]])  # 该message的评分 Todo
    if tag_for_no_msg == 5:
        return
    else:
        return upload_msg





# 生成accident
def accident_factory():
    accident_type = ACCIDENT_TYPE
    accidents = []
    write_to_file = []
    for i in range(ACCIDENT_NUM):
        accidents.append([str(i), (random.randint(0, road_len), 0), accident_type])
        write_to_file.append('{};{};{}'.format(str(i), str((random.randint(0, road_len), 0)), str(accident_type)))
    # ==============================================
    if UPDATE_TXT:
        with open('accident_list.txt', 'w') as w:
            for strs in write_to_file:
                w.write(strs)
                w.write('\n')
    # ==============================================
    if not DEBUG:
        return accidents
    else:
        accidentss = []
        with open('accident_list.txt', 'r') as handler:
            for x in handler:
                x = x.strip('\n').split(';')
                y = x[1].split(',')
                int1 = int(y[0][1:])
                int2 = int(y[1][1:-1])
                accidentss.append([x[0], (int1, int2), int(x[2])])
        return accidentss


# 生成veh的位置
def veh_trajectory():
    distance_veh = random.sample(range(5, 100), 50)
    start_point = random.sample(range(5, 100), 1)
    veh_locations = []
    d_location = 0
    for i in distance_veh:
        d_location += start_point[0] + i
        veh_locations.append(d_location)
    veh_id_list = [str(uuid.uuid3(uuid.NAMESPACE_DNS, str(i))) for i in range(VEH_NUM)]
    if UPDATE_TXT:
        with open('veh_list.txt', 'w')as w:
            for id_index in range(VEH_NUM):
                strw = '{};{}'.format(str(veh_id_list[id_index]), veh_locations[id_index])
                w.write(strw)
                w.write('\n')
    if not DEBUG:
        return dict(zip(veh_id_list, veh_locations))
    else:
        ids = []
        locationss = []
        with open('veh_list.txt', 'r') as handler:
            for x in handler:
                x = x.strip('\n').split(';')
                ids.append(x[0])
                locationss.append(int(x[1]))
        return dict(zip(ids, locationss))



# 返回离veh最近的rsu
def rsu_search(veh_location_s, rsu_list):
    """
    :param veh_location_s: 需要找到附近RSU的veh地址
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
    # [rsu的id, rsu的位置, rsu和veh的距离
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

    # 得到评分列表
    report_cycle = time.clock()
    messages = message(vail_veh, accident_list, report_cycle)

    rating_list = rate(messages, veh_location)

    # 评分发送给RSU
    veh_id_list = []
    for key,values in veh_location.items():
        veh_id_list.append(key)

    for veh_index in range(len(rating_list)):
        rsu_rating_list = rsu_rating_collection(veh_id_list[veh_index],
                                                rating_list[veh_index],
                                                rsu_location_list,
                                                veh_location)


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
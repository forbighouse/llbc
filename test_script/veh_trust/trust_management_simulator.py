# -*- coding: UTF-8 -*-
import random
import time
import math
import copy
import numpy as np
import json
from collections import defaultdict
from score.IoV_state import distance_cal_x
from test_script.veh_trust.base_veh_location import ACCIDENT_TYPE, ACCIDENT_NUM, ROAD_LEN

# 仿真轮数
SIMULATION_ROUND = 50
# RSU的设定数量
RSU_NUM = 35
# 通信距离设定
THRESHOLD_COMMUNICATION = 300
# RSU的间距
RSU_DISTANCE = 250
# 仿真车辆的数量
VEH_NUM = 50
# 仿真时间
time_len = 200000
# 车辆感知范围，设定车辆在多近的距离才可以汇报事件
VEHICLE_PERCEPTION_DISTANCE = 150
# 一个消息的时效性
TIME_TOLERANCE = 1
# 事件发生的阈值
THRESHOLD = 0.5
# 事件发生的概率
PE = 0.5  # 应该用动态的每个事件用一个，这里先用相同的测试
# 测试模式
DEBUG = 0
# 更新所有的txt文件
UPDATE_TXT = 0
# veh和accident的距离值修正，根据accident的可能性判定公式，太近了超出1
RATE_CORRECT = 50


# 生成rsu的位置
def rsu_location():
    # rsu也用UUID的话，后续跟veh的名字很容易混
    # rsu_id_list = [str(uuid.uuid3(uuid.NAMESPACE_DNS, str(i))) for i in range(RSU_NUM)]
    rsu_id_list = [str(i) for i in range(RSU_NUM)]
    rsu_list = [location for location in range(250, (RSU_DISTANCE*RSU_NUM), RSU_DISTANCE)]
    rsu_dict = dict(zip(rsu_id_list, rsu_list))
    # p1 = {key: value for key, value in rsu_dict.items() if value > 300}
    return rsu_id_list, rsu_dict


# RSU收集评分
def rsu_rating_collection(send_id, recv_msg, rsu_location_list, veh_location):
    rsu_for_send = rsu_search(veh_location[send_id], rsu_location_list)
    tag_for_no_msg = 0
    upload_msg = []
    for accident in recv_msg:
        if accident == 0 or accident == -1:
            tag_for_no_msg += 1
        else:
            assert type(accident) is list
            for msg in accident:
                upload_msg.append([rsu_for_send[0],  # 接收的transaction的RSU
                                   send_id,  # 发送这个transaction的veh
                                   msg[0],   # 报告message的veh
                                   msg[1],   # 报告的事件类型
                                   msg[3],  # 该message的评分
                                   msg[4]])
    if tag_for_no_msg == 5:
        pass
    else:
        return upload_msg


# 生成accident
def accident_factory(accident_fast_mode=0):
    accident_type = ACCIDENT_TYPE
    accidents = []
    ids = []
    contents = []
    for i in range(ACCIDENT_NUM):
        x = random.randint(0, ROAD_LEN)
        accidents.append([str(i), (x, 0), accident_type])
        ids.append(str(i))
        contents.append([(x, 0), accident_type])

    if accident_fast_mode:
        accident_dict = dict(zip(ids, contents))
        return accidents, accident_dict
    else:
        accidents2 = []
        ids_2 = []
        contents_2 = []
        with open('accident_list.txt', 'r') as handler:
            for x in handler:
                x = x.strip('\n').split(';')
                y = x[1].split(',')
                int1 = int(y[0][1:])
                int2 = int(y[1][1:-1])
                accidents2.append([x[0], (int1, int2), int(x[2])])
                ids_2.append(x[0])
                contents_2.append([(int1, int2), int(x[2])])
        accident_dict_2 = dict(zip(ids_2, contents_2))
        return accidents2, accident_dict_2


# 生成veh的位置
def veh_trajectory():
    veh_id_list = []
    locationss = []
    with open('veh_list.txt', 'r') as handler:
        for x in handler:
            x = x.strip('\n').split(';')
            veh_id_list.append(x[0])
            locationss.append(int(x[1]))
    # 每一次都更新位置
    if not DEBUG:
        # 随机veh之间的距离和随机第一辆veh的起始位置
        distance_veh = random.sample(range(5, 100), len(veh_id_list))
        start_point = random.sample(range(5, 100), 1)
        veh_locations = []
        d_location = 0
        for i in distance_veh:
            d_location += i + start_point[0]
            veh_locations.append(d_location)
        random.shuffle(veh_locations)
        random.shuffle(veh_id_list)
        return veh_id_list, dict(zip(veh_id_list, veh_locations))
    # 测试模式：每次都从txt文件中读取位置
    else:
        return veh_id_list, dict(zip(veh_id_list, locationss))


def veh_id_fun():
    veh_id_list = []
    with open('veh_list.txt', 'r') as handler:
        for x in handler:
            x = x.strip('\n').split(';')
            veh_id_list.append(x[0])
    return veh_id_list


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
    # print(belong_rsu_optional)
    return belong_rsu_optional[0]


# 生成产生message的veh列表
# 一辆veh可能发出多个msg，所以所谓的虚假消息应该与对应数量的车有关，但是仿真很难控制，
# 所以此处假定msg假不假与车无关，只与msg有关
def merge_veh(vail_veh, false_ratio):
    """
    :param vail_veh:
    :param false_ratio:
    :return:
    """
    if false_ratio == 0:
        return vail_veh, []
    else:
        len_vail_veh_num = 0
        for veh_num in vail_veh:
            len_vail_veh_num += len(veh_num)
        false_veh_num = round(len_vail_veh_num * false_ratio)

        # 从vail_veh中找出与false_veh_num对应数量的车作为fake_msg的发送者
        pos_veh_list, neg_veh_list = merge_veh_delicate(int(false_veh_num), vail_veh)
        return pos_veh_list, neg_veh_list


def merge_veh_delicate(false_veh_num, vail_veh):
    all_veh = []
    accident_num_list = []
    accident_list_list = []
    for i in range(len(vail_veh)):
        accident_num_list.append(i)
        accident_list_list.append([])
        for j in vail_veh[i]:
            all_veh.append([i, j])

    veil_veh_dict = dict(zip(accident_num_list, accident_list_list))
    random.shuffle(all_veh)

    if false_veh_num:
        pos_veh_each_list = all_veh[false_veh_num:]
        neg_veh_each_list = all_veh[:false_veh_num]

        for line in pos_veh_each_list:
            veil_veh_dict[line[0]].append(line[1])

        veil_veh_list = list(veil_veh_dict.values())

        neg_veh_list = []
        for neg_line in neg_veh_each_list:
            neg_veh_list.append([neg_line[1]])

        return veil_veh_list, neg_veh_list

    else:
        pos_veh_each_list = all_veh

        for line in pos_veh_each_list:
            veil_veh_dict[line[0]].append(line[1])

        veil_veh_list = list(veil_veh_dict.values())

        return veil_veh_list, []


def merge_veh_delicate_v2(false_veh_num, vail_veh):
    if false_veh_num:
        pos_veh_each_list = vail_veh[false_veh_num:]
        neg_veh_each_list = vail_veh[:false_veh_num]
        for line in neg_veh_each_list:
            line[3] = 1
            line[5] = 1
        return pos_veh_each_list, neg_veh_each_list

    else:
        return vail_veh, []


def message(vaild_veh_list, accidents, veh_location_dict, report_cycle):
    """
    :param vaild_veh_list:
    :param accidents:
    :param veh_location_dict:
    :param report_cycle: time.clock()
    :return:返回当前网络内的所有message的列表
    """
    if not len(vaild_veh_list):
        print("vaild_veh_list empty")

    vail_accident_num = len(accidents)

    message_list = []
    for index, accident_veh in enumerate(vaild_veh_list):
        if index < vail_accident_num:
            accident_location = accidents[index][1][0]
            accident_type = accidents[index][2]
            if len(accident_veh):
                # 随机找1到3辆车message同一个accident
                # veh_report = random.sample(accident_veh, random.randint(1, 3))
                # if DEBUG:
                #     veh_report = []
                #     veh_report.append(accident_veh[0])

                # 全部车辆上报
                veh_report = accident_veh

                # 给每一次message添加汇报时间
                veh_report_final = []

                for veh in range(len(veh_report)):
                    # 给report_cycle添加或减少一个时间差量
                    report_time = random.uniform(-1, 1)
                    # 打包并重新构造添加了时间的车辆列表
                    fake_tag = 0
                    veh_report_final.append([veh_report[veh], fake_tag, report_cycle + report_time])
                message_list.append([[accident_location, accident_type], veh_report_final])
            else:
                veh_report = []
                message_list.append([[accident_location, accident_type], veh_report])
        else:
            # 给每一次message添加汇报时间
            veh_report_final = []
            for veh in range(len(accident_veh)):
                fake_tag = 1
                veh_report_final.append([accident_veh[veh], fake_tag, report_cycle])
                vec_id = accident_veh[veh][0]
                accident_location = veh_location_dict[vec_id] + accident_veh[veh][1] + random.choice([250, 270, 290])
                accident_type = random.choice([2, 0, 1])
                message_list.append([[accident_location, accident_type], veh_report_final])

    return message_list


def message_merge(messages, veh_location):
    message_list = []
    for veh_id, veh_locations in veh_location.items():
        veh_recv_msg = []
        for msg in messages:
            msg_list = []
            for veh_msg_index in range(len(msg[1])):
                if veh_id != msg[1][veh_msg_index][0][0]:  # 他自己也报
                    veh_for_one_msg = message_collect(veh_id,
                                                      veh_locations,
                                                      veh_location[msg[1][veh_msg_index][0][0]],
                                                      msg[0],
                                                      msg[1][veh_msg_index],
                                                      msg[1][veh_msg_index][1])
                    if veh_for_one_msg:
                        msg_list.append(veh_for_one_msg)
                    else:
                        continue

            # veh_recv_msg.append(veh_for_one_msg)
            if len(msg_list):
                veh_recv_msg.append(msg_list)
            else:
                veh_recv_msg.append(0)
        message_list.append(veh_recv_msg)
    return message_list


def message_collect(veh_id, veh_locations, veh_send_location, msg0, msg1, fake_tag):
    """
    :param veh_locations: 任意一辆车的位置，其实是接收message的veh
    :param veh_send_location: 发送message的车辆的位置
    :param
    :return:
    """
    # 还应该判断消息的时效性，应该在哪判断？
    if abs(veh_locations - veh_send_location) < THRESHOLD_COMMUNICATION:
        # [收到message的id, 汇报message的id, accident的位置， accident的类型, accident的距离, 是否为假消息]
        return [veh_id, msg1[0][0], msg0[0], msg0[1], msg1[0][1], fake_tag]
    else:
        # 如果小于通信距离，当前车辆无法接收到message，所以msg_list在该车辆位置置0
        return 0


# 应该在这里添加false消息的控制
def accident_probability(veh_dict, veh_ids, false_ratio):
    accidents_list = []
    for vehs, msgs in veh_dict.items():
        accident_case_list = []
        for msg in msgs:
            accident_case_list.append(msg[2])
        accident_case_list = list(set(accident_case_list))
        acciden_empty_list = [[] for i in range(len(accident_case_list))]
        accident_dict = dict(zip(accident_case_list, acciden_empty_list))
        accidents_list.append(accident_dict)
    veh_accident_dict = dict(zip(veh_ids, accidents_list))

    for vehs_v2, msgs_v2 in veh_dict.items():
        for msg_v2 in msgs_v2:
            accident_num = msg_v2[2]
            veh_accident_dict[vehs_v2][accident_num].append(msg_v2)

    accident_veh_list = []
    rating_veh_dict = defaultdict(list)
    for vehs_v3, msg_v3 in veh_accident_dict.items():
        veh_ids_v1 = []
        veh_accident_list = []
        for accident_index, accident_msg in msg_v3.items():
            acci_prob = accident_pro(accident_msg, false_ratio)
            veh_ids_v1.append(accident_index)
            veh_accident_list.append(acci_prob)
        veh_accident_dict_pro = dict(zip(veh_ids_v1, veh_accident_list))
        accident_veh_list.append(veh_accident_dict_pro)

        for msg_one in veh_dict[vehs_v3]:
            if msg_one[3] == 0 and veh_accident_dict_pro[msg_one[2]][0] > THRESHOLD:
                one_copy = copy.deepcopy(msg_one)
                one_copy.append(1)
                rating_veh_dict[vehs_v3].append(one_copy)
            elif msg_one[3] == 0 and veh_accident_dict_pro[msg_one[2]][0] < THRESHOLD:
                one_copy = copy.deepcopy(msg_one)
                one_copy.append(-1)
                rating_veh_dict[vehs_v3].append(one_copy)
            elif msg_one[3] == 1 and veh_accident_dict_pro[msg_one[2]][1] > THRESHOLD:
                one_copy = copy.deepcopy(msg_one)
                one_copy.append(1)  # 评分在最后，
                rating_veh_dict[vehs_v3].append(one_copy)
            elif msg_one[3] == 1 and veh_accident_dict_pro[msg_one[2]][1] < THRESHOLD:
                one_copy = copy.deepcopy(msg_one)
                one_copy.append(-1)  # 评分在最后，
                rating_veh_dict[vehs_v3].append(one_copy)

    veh_accident_pro_dict = dict(zip(veh_ids, accident_veh_list))
    return veh_accident_pro_dict, rating_veh_dict


def accident_pro(accident_msg, false_ratio):
    # accident_type_dict = defaultdict(list)
    # for i in accident_msg:
    #     rate_for_acci_type = rate_rating(i[4])
    #     accident_type_dict[i[3]].append(rate_for_acci_type)

    false_veh_num = round(len(accident_msg) * false_ratio)
    pos_veh_list, neg_veh_list = merge_veh_delicate_v2(int(false_veh_num), accident_msg)

    pos_pro = occur_probability(PE, pos_veh_list, neg_veh_list)
    neg_pro = 1 - pos_pro
    return [pos_pro, neg_pro]


def rsu_statistic(rsu_meet_num):
    sorted_res = sorted(rsu_meet_num.items(), key=lambda item: item[1])

    if sorted_res[-1][1] == sorted_res[-2][1] and  sorted_res[-1][0] == '0':
        return sorted_res[-2][0]
    else:
        return sorted_res[-1][0]


def rate(message_list, veh_location):
    """
    :param veh_location: 发出此rate的veh的位置
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
                                                       msg[1][veh_msg_index],
                                                       msg[1][veh_msg_index][1])
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
    return rating_list


def rate_collect_msg(veh_locations, veh_send_location, msg0, msg1, fake_tag):
    """
    :param veh_locations: 任意一辆车的位置，其实是接收message的veh
    :param veh_send_location: 发送message的车辆的位置
    :param
    :return:
    """
    # 还应该判断消息的时效性，应该在哪判断？
    if abs(veh_locations - veh_send_location) < THRESHOLD_COMMUNICATION:
        # [汇报message的id, ,accident的位置， accident的类型，评分, 是否为假消息]
        return [msg1[0][0], msg0[0], msg0[1], rate_rating(msg1[0][1]), fake_tag]
    else:
        # 如果小于通信距离，当前车辆无法接收到message，所以msg_list在该车辆位置置0
        return 0


# 评分c = b + e(-γd)
# RATE_CORRECT制定为50
def rate_rating(distance, rate_correct=RATE_CORRECT, b=0.5, gamma=0.014):
    if distance < rate_correct:
        distance = rate_correct
    ck = b + pow(math.e, ((-gamma)*distance))
    assert ck < 1
    return ck


# 每一辆车给出得到的message的评分
def veh_rate(msg_list):
    accident_probiblity = []
    for accident in msg_list:
        rates = []
        if accident != 0:
            for msgs in accident:
                rates.append(msgs[3])
                # 发出message的veh_id
            accident_probiblity.append(occur_probability(PE, rates))
        else:
            accident_probiblity.append(0)
    # 给出最后的对每一个message的评分
    return rate_get(msg_list, accident_probiblity)


# event的概率
def occur_probability(pe, pos_veh_list, neg_veh_list):
    pos_list = []
    _pos_list = []
    for x in pos_veh_list:
        pos_list.append(rate_rating(x[4]))
        _pos_list.append(1-rate_rating(x[4]))
    neg_list = []
    _neg_list = []
    for y in neg_veh_list:
        neg_list.append(rate_rating(y[4]))
        _neg_list.append(1-rate_rating(y[4]))

    def multi_plicator(num_list):
        result = 1
        for num in num_list:
            result = result * num
        assert 0 < result < 1
        return result

    part1 = pe * multi_plicator((pos_list+_neg_list))
    part2 = (1-pe) * multi_plicator((neg_list+_pos_list))
    return part1 / (part1 + part2)


def rate_count(rating_each_list):
    """
    :param rating_each_list:
    :return: 正面rating的数量，负面rating的数量
    """
    positive_num = 0
    negative_num = 0
    fake_msg_num = 0
    for num in rating_each_list:
        if num == 1:
            positive_num += 1
        elif num == -1:
            negative_num += 1
        elif num == -2:
            fake_msg_num += 1

    return positive_num, negative_num, fake_msg_num


# 每一辆车计算message的评分
def rate_get(msg_list, accident_probability):
    assert type(msg_list) is list
    accident_act = []
    for y in accident_probability:
        if y > THRESHOLD:
            accident_act.append(1)
        else:
            accident_act.append(0)

    rate_result_for_one_veh = []
    for msg_index in range(len(msg_list)):
        if msg_list[msg_index] != 0:
            d = []
            for msgs in msg_list[msg_index]:
                if accident_act[msg_index] == 1:  rates_for = 1
                else:  rates_for = -1
                d.append([msgs[0],  # 报告message的veh
                          msgs[1],  # 报告accident的位置
                          msgs[2],  # 报告accident的类型
                          rates_for,  # 该message的评分
                          msgs[4]])  # 该message的真伪
            rate_result_for_one_veh.append(d)
        else:
            rate_result_for_one_veh.append(0)
    return rate_result_for_one_veh


# 一个基站开始计算offset
def offset(rsu_ratings_list):
    veh_count_dict = defaultdict(list)
    false_offset_tag = 0
    for rate_line in rsu_ratings_list:
        append_list = rate_line[2:]
        if rate_line[3] == 0 and rate_line[5] == 0:
            false_offset_tag = 1
        elif rate_line[3] == 0 and rate_line[5] == 1:
            false_offset_tag = -1
        elif rate_line[3] == 0 and rate_line[5] == -1:
            false_offset_tag = -1
        elif rate_line[3] == 1 and rate_line[5] == 1:
            false_offset_tag = 1
        append_list.append(false_offset_tag)
        veh_count_dict[rate_line[1]].append(append_list)

    # rating_count = []
    # for veh_id, rating in veh_count_dict.items():
    #     p_num, n_num, fake_num = rate_count(rating)
    #     rating_count.append([veh_id, p_num, n_num, fake_num])
    #
    # offset_result = []
    # for each_count in rating_count:
    #     offset_result.append([each_count[0], offset_count(each_count), each_count[3]])
    #
    # return offset_result, veh_count_dict
    return veh_count_dict


# 计算正负rating的数量
def offset_rate_count(rating_each_list):
    """
    :param rating_each_list:
    :return: 正面rating的数量，负面rating的数量
    """
    positive_num = 0
    negative_num = 0
    for num in rating_each_list:
        if num == 1:
            positive_num += 1
        elif num == -1:
            negative_num += 1

    return [positive_num, negative_num]


# offset的统计计算
def offset_count(rating_count):
    m = rating_count[1]  # 正
    n = rating_count[2]  # 负

    # def sensitivity_fun(xx): return xx*xx
    # def sensitivity_fun(xx): return xx
    # def sensitivity_fun(xx): return xx*xx*xx
    def sensitivity_fun(xx): return pow(math.e, xx)

    sita1 = sensitivity_fun(m) / (sensitivity_fun(m) + sensitivity_fun(n))
    sita2 = sensitivity_fun(n) / (sensitivity_fun(m) + sensitivity_fun(n))

    return (sita1*m - sita2*n) / (m + n)


def simulator_count(offset_list):
    pos_num = 0
    neg_num = 0
    fake_num = 0
    for num in offset_list:
        if num[0] > 0:
            pos_num += 1
        elif num[0] < 0:
            neg_num += 1
        fake_num += num[1]
    return [pos_num, neg_num, fake_num]


def traditional_version(round_num, false_ratio):
    # rsu的位置列表，dict, (id, location)
    rsu_ids, rsu_location_list = rsu_location()
    # 随机产生的事件的位置 dict, location
    accident_list, accident_dict = accident_factory()

    rsu_transaction_list = [[] for ids in range(len(rsu_ids))]
    rsu_transaction = dict(zip(rsu_ids, rsu_transaction_list))
    # 记录每一个rsu获得的评分情况，与rsu_transaction区别开
    rsu_rating_for_count = copy.deepcopy(rsu_transaction)
    rsu_max_id_list = []
    veh_ids = []
    neg_veh_all_list = []
    # 所有轮产生的所有的message
    messages_list = []

    # message_dict收集所有轮积攒下的msg
    accident_dict_key = [k for k in accident_dict.keys()]
    accident_dict_empty = [[] for j in range(len(accident_dict))]
    message_dict = dict(zip(accident_dict_key, accident_dict_empty))

    # 反转accident，索引其地址，返回其序号
    accident_dict_reverse = {v[0][0]: [k, v[1]] for k, v in accident_dict.items()}
    veh_empty_ids = veh_id_fun()
    veh_empty_list = [[] for u in range(len(veh_empty_ids))]
    veh_dict = dict(zip(veh_empty_ids, veh_empty_list))

    # 记录每一辆veh在一轮里面见到的rsu的数量
    rsu_epoch_dict = defaultdict(dict)
    veh_rsu_all_dict = defaultdict(dict)
    for veh_ in veh_empty_ids:
        veh_rsu_all_dict[veh_] = copy.deepcopy(rsu_epoch_dict)

    for epoch in range(round_num):
        # 随机产生的车辆位置 dict, (veh_id: location
        veh_ids, veh_location = veh_trajectory()

        # 每一辆车与事件的距离, list, (veh_id, distance)
        distance_list = []

        # 位置距离小于THRESHOLD_COMMUNICATION的具体距离，list, (veh_id, distance)
        vail_veh = []
        false_veh = []

        # 求得vail_veh
        accident_id_list = [m for m in range(ACCIDENT_NUM)]
        for v1 in accident_list:
            d = []
            for k2, v2 in veh_location.items():
                d.append((k2, int(distance_cal_x(int(v1[1][0]), v2))))
            distance_list.append(d)
        adjacency_list = dict(zip(accident_id_list, distance_list))

        # 控制msg的真假数量
        for k, v in adjacency_list.items():
            true_msg_veh = []
            false_msg_veh = []
            for v1 in v:
                if v1[1] < THRESHOLD_COMMUNICATION:
                    true_msg_veh.append(v1)
                else:
                    false_msg_veh.append(v1)
            vail_veh.append(true_msg_veh)  # accident周围的车辆
            false_veh.append(false_msg_veh)  # 远离accideng的车辆

        # 得到评分列表
        report_cycle = time.clock()
        messages = message(vail_veh,
                           accident_list,
                           veh_location,
                           report_cycle)

        for one_epoch in messages:
            for veh_id, veh_locations in veh_location.items():
                for msg in one_epoch[1]:
                    if veh_id != msg[0][0]:  # 他自己也报
                        veh_for_one_msg = message_collect(veh_id,
                                                          veh_locations,
                                                          veh_location[msg[0][0]],
                                                          one_epoch[0],
                                                          msg,
                                                          msg[1])
                        if veh_for_one_msg:
                            veh_dict[veh_id].append(veh_for_one_msg)

        # 找veh对应的rsu

        for veh_id_key, veh_loc_value in veh_location.items():
            rsu_assemble_list = rsu_search(veh_loc_value, rsu_location_list)
            _x = veh_rsu_all_dict[veh_id_key]
            _x[rsu_assemble_list[0]] = _x.get(rsu_assemble_list[0], 0) + 1

    _, veh_rating_dict = accident_probability(veh_dict, copy.deepcopy(veh_empty_ids), false_ratio)

    veh_meet_rsu = defaultdict(int)
    for veh_s, rsu_meet_num in veh_rsu_all_dict.items():
        veh_meet_rsu[veh_s] = rsu_statistic(rsu_meet_num)

    # rating_list = rate(messages_list[1], veh_location)

    # 每辆车统计评分
    # len_accident = len(merge_veh_list)  # 算上假的msg总共有多少种
    # msg_rate_list = []
    # for msg_index in range(len(rating_list)):
    #     if len(rating_list[msg_index]) == len_accident:
    #         msg_rate_list.append(veh_rate(rating_list[msg_index]))

    # 评分发送给RSU
    # RSUs得到的所有评分
    rsu_rating_dic = defaultdict(list)
    for veh_index, msg_list in veh_rating_dict.items():
        for msgs in msg_list:
            rsu_id = veh_meet_rsu[veh_index]
            rsu_rating_dic[rsu_id].append(msgs)


    # todo
    # 每一个RSU用收到的rate计算对应车辆的offset，使用区块链的来竞争记账权
    rsu_offset_dict = defaultdict(list)
    rsu_pre_offset_dict = defaultdict(list)
    for rsu_offset_id, rsu_ratings in rsu_rating_dic.items():
        pre_offset = offset(rsu_ratings)
        rsu_pre_offset_dict[rsu_offset_id] = pre_offset
        # rsu_offset_dict[rsu_offset_id].append()

    # npd: not update
    # npd_transaction_by_rsu_list = []
    # rsu_id_list_v2 = []
    # rsu_transaction_len = 0
    # rsu_transaction_max_id = 0
    # for key, value in rsu_id_dict.items():
    #     rsu_transaction[key].append(offset(value))
    #     rsu_rating_for_count[key].append(value)
    #
    #     if len(offset(value)) > rsu_transaction_len:
    #         rsu_transaction_len = len(offset(value))
    #         rsu_transaction_max_id = key
    # rsu_max_id_list.append(rsu_transaction_max_id)
    #     # rsu_id_list_v2.append(key)
    #     # npd_transaction_by_rsu_list.append(offset(value))
    # pass
    #     # npd_transaction_by_rsu_dict = dict(zip(rsu_id_list_v2, npd_transaction_by_rsu_list))
    # # --------------------------------------------------------------------------------------
    # rsu_active_list = []
    # trans = []
    # for key, rsus in rsu_transaction.items():
    #     if len(rsus) > 0:
    #         rsu_active_list.append(key)
    #         trans.append(rsus)
    #
    # count = [None, 0]
    # for i in range(len(trans)):
    #     count_veh_trans = 0
    #     for j in trans[i]:
    #         count_veh_trans += len(j)
    #     if count_veh_trans > count[1]:
    #         count[1] = count_veh_trans
    #         count[0] = rsu_active_list[i]
    #
    # consensus_node = count[0]
    #
    # veh_offset_list = [[] for i in range(len(veh_ids))]
    # veh_offset_dict = dict(zip(veh_ids, veh_offset_list))
    # veh_offset_result_dict = veh_offset_dict
    # for ep in rsu_transaction[consensus_node]:
    #     for eps in ep:
    #         veh_offset_dict[eps[0]].append([eps[1], eps[2]])
    #
    # for key, value in veh_offset_dict.items():
    #     veh_offset_result_dict[key] = simulator_count(value)

    # return veh_offset_result_dict, rsu_rating_for_count[consensus_node], veh_ids, accident_dict，rsu_rating_dic
    return rsu_rating_dic, rsu_pre_offset_dict


def statistic_msg(rsu_rating_dic):
    key_tag  = 0
    num_tag = 0
    for rsu_id, rsu_msg in rsu_rating_dic.items():
        if len(rsu_msg) > num_tag:
            key_tag = rsu_id
            num_tag = len(rsu_msg)
    return statistic_msg_count(rsu_rating_dic[key_tag])


def statistic_offset(pre_offset_dict):
    veh_offset_dict = defaultdict(dict)
    for rsu, msgs in pre_offset_dict.items():
        veh_offset_sub_dict = defaultdict(dict)
        for veh, ms in msgs.items():
            acci_dict = defaultdict(list)
            # 如果这是一个false的message，那么这不应该作为+1算在是trust的offset计算里
            for xi in ms:
                if xi[3] == 1:
                    acci_dict[xi[0]].append(-1)
                else:
                    acci_dict[xi[0]].append(xi[4])
            veh_offset_sub_dict[veh] = acci_dict
        veh_offset_dict[rsu] = veh_offset_sub_dict

    veh_offset_all_list = []
    pos_num_all_veh = 0
    neg_num_all_veh = 0
    for vehs, offset in veh_offset_dict['0'].items():
        # 一辆车的所有评分
        pos_num_one_veh, neg_num_one_veh = statistic_offset_count(offset)
        veh_offset_all_list.append(offset_count([None, pos_num_one_veh, neg_num_one_veh]))
        pos_num_all_veh += pos_num_one_veh
        neg_num_all_veh += neg_num_one_veh
    trust_num = 0
    for i in veh_offset_all_list:
        trust_num += i

    # 应该只是给出最后的一个trust offset
    trust_offset_num = round((trust_num/len(veh_offset_all_list)), 2)
    unfair_offset_ratio_res = round(neg_num_all_veh/(pos_num_all_veh+neg_num_all_veh), 2)
    return trust_offset_num, unfair_offset_ratio_res


# 统计一辆车的不同的accident下的所有评分
def statistic_offset_count(accident_rating_dict):
    pos_num_all = 0
    neg_num_all = 0
    for accident, rating_list in accident_rating_dict.items():
        p_num, n_num = offset_rate_count(rating_list)
        pos_num_all += p_num
        neg_num_all += n_num
    return pos_num_all, neg_num_all


def statistic_msg_count(msg_list):
    pos_num1 = 0
    neg_num1 = 0
    for msg in msg_list:
        if msg[3] == 0 and msg[5] == 0 and msg[6] == 1:
            pos_num1 += 1
        elif msg[3] == 1 and msg[5] == 1 and msg[6] == -1:
            pos_num1 += 1
        elif msg[3] == 0 and msg[5] == 0 and msg[6] == -1:
            neg_num1 += 1
        elif msg[3] == 1 and msg[5] == 1 and msg[6] == 1:
            neg_num1 += 1
    return pos_num1, neg_num1


def statistic_fun(rsu_rating_res, ids, accident_dict):
    accident_dict_key = [k for k in accident_dict.keys()]
    accident_dict_empty = [[] for j in range(len(accident_dict))]
    accident_iter = dict(zip(accident_dict_key, accident_dict_empty))
    veh_list = [copy.deepcopy(accident_iter) for i in range(len(ids))]
    veh_dict = dict(zip(ids, veh_list))

    # 反转accident，索引其地址，返回其序号
    accident_dict = {v[0][0]: [k, v[1]] for k, v in accident_dict.items()}

    #  --------------------------------------------------------
    # | 接收msg的车号 | accident序号1 | ...... | accident序号n |
    #  --------------------------------------------------------
    for rsu_rating in rsu_rating_res:
        for msg in rsu_rating:
            # msg[2]发出msg的车号，msg[4]该msg的rating(可能作废)， msg[5]fake标记
            receiver_msg = msg[1]
            accident_tag = accident_dict[msg[3]][0]
            veh_dict[receiver_msg][accident_tag].append([msg[2], msg[4], msg[5]])

    pass


if __name__ == '__main__':

    unfair_msg_ratio_list = []
    unfair_offset_ratio_list = []
    trust_offset_list = []
    rounds = np.arange(0, 1, 0.05)
    for x in rounds:
        # res, rsu_rating_res, veh_ids, accident_list = traditional_version(SIMULATION_ROUND, 0.6)
        rsu_rating_dic, pre_offset_dict = traditional_version(SIMULATION_ROUND, x)

        rating_num = 0
        false_msg_num = 0

        # 第一张图，求假消息与评分的关系
        pos_num, neg_num = statistic_msg(rsu_rating_dic)
        false_ratio = neg_num / (neg_num + pos_num)
        unfair_msg_ratio_list.append(false_ratio)

        #  第二张图，求不公平的评分与真实值得图
        trust_offset_res, unfair_offset_ratio = statistic_offset(pre_offset_dict)
        trust_offset_list.append(trust_offset_res)
        unfair_offset_ratio_list.append(unfair_offset_ratio)



    unfair_msg_ratio_dict = dict(zip(rounds, unfair_msg_ratio_list))
    unfair_msg_ratio_json = json.dumps(unfair_msg_ratio_dict)
    a = open(r"unfair_msg2.txt", "w", encoding='UTF-8')
    a.write(unfair_msg_ratio_json)
    a.close()

    # trust_offset_dict = dict(zip(unfair_offset_ratio_list, trust_offset_list))
    # trust_offset_json = json.dumps(trust_offset_dict)
    # b = open(r"trust_offset3.txt", "+w", encoding='UTF-8')
    # b.write(trust_offset_json)
    # b.close()






import random
import time
import math
import copy
import numpy as np
import json
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
    return rsu_id_list, dict(zip(rsu_id_list, rsu_list))


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
    print()
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
            d_location += start_point[0] + i
            veh_locations.append(d_location)
        random.shuffle(veh_locations)
        return veh_id_list, dict(zip(veh_id_list, veh_locations))
    # 测试模式：每次都从txt文件中读取位置
    else:
        return veh_id_list, dict(zip(veh_id_list, locationss))


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


def message_fake_tag(veh_id, _neg_veh_list):
    if len(_neg_veh_list):
        for i in _neg_veh_list:
            if i[0] == veh_id:
                return 1
            else:
                return 0
    else:
        return 0


# 一个基站开始计算offset
def offset(value_list):
    veh_count = [veh[2] for veh in value_list]
    veh_rate_count = [[] for count in range(len(value_list))]
    veh_count_dict = dict(zip(veh_count, veh_rate_count))
    for rate_line in value_list:
        veh_count_dict[rate_line[2]].append(rate_line[-2])
        if rate_line[5] == 1:
            veh_count_dict[rate_line[2]].append(-2)

    rating_count = []
    for veh_id, rating in veh_count_dict.items():
        p_num, n_num, fake_num = rate_count(rating)
        rating_count.append([veh_id, p_num, n_num, fake_num])

    offset_result = []
    for each_count in rating_count:
        offset_result.append([each_count[0], offset_count(each_count), each_count[3]])

    return offset_result


# 计算正负rating的数量
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


def rate_condition_report(location1, location2):
    """
    :param location1: 发出此rate的veh的位置
    :param location2: accident的位置
    :return:
    """
    return abs(location1 - location2) < VEHICLE_PERCEPTION_DISTANCE


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
def occur_probability(pe, peck):
    peck_ = []
    for x in peck:
        peck_.append(1-x)

    def multi_plicator(num_list):
        result = 1
        for num in num_list:
            result = result * num
        assert 0 < result < 1
        return result
    part1 = pe * multi_plicator(peck)
    part2 = (1-pe) * multi_plicator(peck_)
    return part1 / (part1 + part2)


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


# offset的统计计算
def offset_count(rating_count):
    m = rating_count[1]  # 正
    n = rating_count[2]  # 负

    def sensitivity_fun(xx): return xx*xx

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

        # 拆分veh,返回的是拼接好的
        pos_veh_list, neg_veh_list = merge_veh(vail_veh, false_ratio)
        merge_veh_list = pos_veh_list + neg_veh_list
        neg_veh_all_list.append(neg_veh_list)

        # 得到评分列表
        report_cycle = time.clock()
        messages = message(merge_veh_list,
                           accident_list,
                           veh_location,
                           report_cycle)
        rating_list = rate(messages, veh_location)

        # veh的id列表
        # veh_id_list = []
        # for key, values in veh_location.items():
        #     veh_id_list.append(key)

        # 每辆车统计评分
        len_accident = len(merge_veh_list)  # 算上假的msg总共有多少种
        msg_rate_list = []
        for msg_index in range(len(rating_list)):
            if len(rating_list[msg_index]) == len_accident:
                msg_rate_list.append(veh_rate(rating_list[msg_index]))

        # 评分发送给RSU
        # 一轮下来RSUs得到的所有评分
        rsu_rating_list = []
        for veh_index in range(len(msg_rate_list)):
            rsu_rating = rsu_rating_collection(veh_ids[veh_index],
                                               msg_rate_list[veh_index],
                                               rsu_location_list,
                                               veh_location)
            if rsu_rating:
                if len(rsu_rating) > 1:
                    for i in rsu_rating:
                        rsu_rating_list.append(i)
                else:
                    rsu_rating_list.append(rsu_rating[0])

        # 每一个RSU用收到的rate计算对应车辆的offset，使用区块链的来竞争记账权
        rsu_id_list = [rsu_rating[0] for rsu_rating in rsu_rating_list]
        rsu_id_num_list = [[] for i in range(len(rsu_id_list))]
        rsu_id_dict = dict(zip(rsu_id_list, rsu_id_num_list))
        for rsu_rating in rsu_rating_list:
            rsu_id_dict[rsu_rating[0]].append(rsu_rating)

        # npd: not update
        npd_transaction_by_rsu_list = []
        rsu_id_list_v2 = []
        rsu_transaction_len = 0
        rsu_transaction_max_id = 0
        for key, value in rsu_id_dict.items():
            rsu_transaction[key].append(offset(value))
            rsu_rating_for_count[key].append(value)

            if len(offset(value)) > rsu_transaction_len:
                rsu_transaction_len = len(offset(value))
                rsu_transaction_max_id = key
        rsu_max_id_list.append(rsu_transaction_max_id)
            # rsu_id_list_v2.append(key)
            # npd_transaction_by_rsu_list.append(offset(value))
        pass
        # npd_transaction_by_rsu_dict = dict(zip(rsu_id_list_v2, npd_transaction_by_rsu_list))
    # --------------------------------------------------------------------------------------
    rsu_active_list = []
    trans = []
    for key, rsus in rsu_transaction.items():
        if len(rsus) > 0:
            rsu_active_list.append(key)
            trans.append(rsus)

    count = [None, 0]
    for i in range(len(trans)):
        count_veh_trans = 0
        for j in trans[i]:
            count_veh_trans += len(j)
        if count_veh_trans > count[1]:
            count[1] = count_veh_trans
            count[0] = rsu_active_list[i]

    consensus_node = count[0]

    veh_offset_list = [[] for i in range(len(veh_ids))]
    veh_offset_dict = dict(zip(veh_ids, veh_offset_list))
    veh_offset_result_dict = veh_offset_dict
    for ep in rsu_transaction[consensus_node]:
        for eps in ep:
            veh_offset_dict[eps[0]].append([eps[1], eps[2]])

    for key, value in veh_offset_dict.items():
        veh_offset_result_dict[key] = simulator_count(value)

    return veh_offset_result_dict, rsu_rating_for_count[consensus_node], veh_ids, accident_dict


def statistic_fun(rsu_rating_res, ids, accident_dict):
    accident_dict_key = [k for k in accident_dict.keys()]
    accident_dict_empty = [[] for j in range(len(accident_dict))]
    accident_iter = dict(zip(accident_dict_key, accident_dict_empty))
    veh_list = [accident_iter for i in range(len(ids))]
    veh_dict = dict(zip(ids, veh_list))

    # 反转accident，索引其地址，返回其序号
    accident_dict = {v[0][0]: [k, v[1]] for k, v in accident_dict.items()}

    # ------------------------------------------------------------
    # | 接收msg的车号 | accident序号1 | ...... | accident序号n |
    #
    # ------------------------------------------------------------
    for rsu_rating in rsu_rating_res:
        for msg in rsu_rating:
            # msg[2]发出msg的车号，msg[4]该msg的rating(可能作废)， msg[5]fake标记
            receiver_msg = msg[1]
            accident_tag = accident_dict[msg[3]][0]
            veh_dict[receiver_msg][accident_tag].append([msg[2], msg[4], msg[5]])

    pass


if __name__ == '__main__':

    unfair_offset_ratio = []
    rounds = np.arange(0, 1, 0.05)
    for x in rounds:
        print(x)
        res, rsu_rating_res, veh_ids, accident_list = traditional_version(SIMULATION_ROUND, x)

        # trust_offset_sum = 0  # 共有多少个评分
        # false_offset_sum = 0
        # false_msg_sum = 0
        # for i in res.values():
        #     trust_offset_sum += i[0]
        #     false_offset_sum += i[1]
        #     false_msg_sum += i[2]
        #
        # false_ratio = false_msg_sum / (trust_offset_sum + false_offset_sum)
        # unfair_offset_ratio.append(false_ratio)

        rating_num = 0
        false_msg_num = 0

        res_list = statistic_fun(rsu_rating_res, veh_ids, accident_list)

        for rsuss in rsu_rating_res:
            for i in rsuss:
                rating_num += i[4]
                false_msg_num += i[5]
        false_ratio = false_msg_num / rating_num
        unfair_offset_ratio.append(false_ratio)
        c_dict = dict(zip(rounds, unfair_offset_ratio))

        c_list = json.dumps(c_dict)
        a = open(r"data_source_list.txt", "w", encoding='UTF-8')
        a.write(c_list)
        a.close()








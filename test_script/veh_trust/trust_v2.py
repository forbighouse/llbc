from test_script.veh_trust.trust_management_simulator import *
from test_script.veh_trust.base_veh_location import *

NUM_REQUEST_VEH = 5
# 车辆请求的内容
REQ_DATA_CONTENT = 0
# 车辆请求的距离要求
REQ_DISTENCE_REQ = 0
# 车辆请求的时间要求
REQ_TIME_REQ = 0


def veh_trajectory_v2():
    veh_id_list = []
    with open('veh_list.txt', 'r') as handler:
        for x in handler:
            x = x.strip('\n').split(';')
            veh_id_list.append(x[0])

    # 随机车辆之间的距离和随机第一辆车的起始位置
    distance_veh_start = random.sample(range(5, 100), len(veh_id_list))
    start_point = random.sample(range(5, 20), 1)
    veh_locations_start = []
    veh_locations_end = []
    d_location_start = 0
    d_location_end = 0
    for i in distance_veh_start:
        d_location_start += i + start_point[0]
        veh_locations_start.append(d_location_start)

    distance_veh_end = random.sample(range(5, 100), len(veh_id_list))
    for j in distance_veh_end:
        d_location_end += j + start_point[0]
        veh_locations_end.append(d_location_end)

    random.shuffle(veh_locations_start)
    random.shuffle(veh_locations_end)
    random.shuffle(veh_id_list)
    return veh_id_list, dict(zip(veh_id_list, veh_locations_start)), dict(zip(veh_id_list, veh_locations_end))


def bl_address_read(file_address=BLOCKCHAIN_ADDRESS_FILE):
    bl_address_id_list = []
    with open(file_address, 'r') as handler:
        for line in handler:
            line = line.strip('\n').split(';')
            bl_address_id_list.append(line[0])
    return bl_address_id_list


def veh_address_allocation(veh_init_ids, bl_address_ids):
    address_veh_dict = defaultdict(str)
    for veh_id, address_ids in zip(veh_init_ids, bl_address_ids):
        for address_id in address_ids:
            address_veh_dict[address_id] = veh_id
    bl_address_ids_list = [bl_address_ids[i:i + 3] for i in range(0, len(bl_address_ids), 3)]
    veh_address_dict = dict(zip(veh_init_ids, bl_address_ids_list))
    return veh_address_dict, address_veh_dict


def count_valid_for_req(temp_list, veh_location):
    re_valid_veh_dict = defaultdict(list)
    for msg in temp_list:
        re_valid_veh_dict[msg[1]] = count_valid_part_fun(msg, veh_location)
    return re_valid_veh_dict


def count_valid_part_fun(one_msg, veh_location):
    tmp_valid_veh = []
    for tmp_veh_id, tmp_veh_location in veh_location.items():
        if tmp_veh_id != one_msg[1]:
            if int(distance_cal_x(one_msg[2], tmp_veh_location)) <= THRESHOLD_COMMUNICATION:
                tmp_valid_veh.append(tmp_veh_id)
    return tmp_valid_veh


def event_owned(tmp_veh_id, vail_veh):
    event_owned_list = []
    for tmp_vehs in vail_veh:
        if tmp_veh_id in tmp_vehs:
            event_owned_list.append(vail_veh.index(tmp_vehs))
    return event_owned_list


def traditional_v2(round_num, false_ratio):
    # # //rsu的位置列表，dict, (id, location)
    # rsu_ids, rsu_location_list = rsu_location()
    # //随机产生的事件的位置 dict, location
    event_list, accident_dict = accident_factory()
    #
    # rsu_transaction_list = [[] for ids in range(len(rsu_ids))]
    # rsu_transaction = dict(zip(rsu_ids, rsu_transaction_list))
    # # //记录每一个rsu获得的评分情况，与rsu_transaction区别开
    # rsu_rating_for_count = copy.deepcopy(rsu_transaction)
    # rsu_max_id_list = []
    # veh_ids = []
    # neg_veh_all_list = []
    # # //所有轮产生的所有的message
    # messages_list = []
    #
    # # //message_dict收集所有轮积攒下的msg
    # accident_dict_key = [k for k in accident_dict.keys()]
    # accident_dict_empty = [[] for j in range(len(accident_dict))]
    # message_dict = dict(zip(accident_dict_key, accident_dict_empty))
    #
    # # //反转accident，索引其地址，返回其序号
    # accident_dict_reverse = {v[0][0]: [k, v[1]] for k, v in accident_dict.items()}
    # //现在有了这么多车了，下一步是往外发消息
    veh_init_ids = veh_id_fun()
    bl_address_ids = bl_address_read()
    veh_address_dict, address_veh_dict = veh_address_allocation(veh_init_ids,bl_address_ids)

    # //记录每一辆veh在一轮里面见到的rsu的数量
    veh_seq_for_epoch_dict = defaultdict(list)
    veh_req_for_epoch_dict = defaultdict(list)
    # rsu_epoch_dict = defaultdict(dict)
    # veh_rsu_all_dict = defaultdict(dict)
    # for veh_ in veh_init_ids:
    #     veh_rsu_all_dict[veh_] = copy.deepcopy(rsu_epoch_dict)

    for epoch in range(round_num):
        # //随机产生的车辆位置 dict, (veh_id: location)
        veh_ids, veh_location = veh_trajectory()
        # //每一辆车与事件的距离, list, (veh_id, distance)
        distance_list = []
        # //位置距离小于THRESHOLD_COMMUNICATION的具体距离，list, (veh_id, distance)
        vail_veh = []
        false_veh = []

        # 求得vail_veh
        accident_id_list = [m for m in range(ACCIDENT_NUM)]
        for v1 in event_list:
            d = []
            for k2, v2 in veh_location.items():
                d.append((k2, int(distance_cal_x(int(v1[1][0]), v2))))
            distance_list.append(d)
        adjacency_list = dict(zip(accident_id_list, distance_list))

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

        send_request_veh_id_list = random.sample(veh_ids, NUM_REQUEST_VEH)
        veh_req_for_epoch_dict[epoch].append(send_request_veh_id_list)
        veh_seq_for_epoch_dict[epoch].append(vail_veh)

        temp_list = []
        for veh_sending_req in send_request_veh_id_list:
            event_ready_for_veh = random.choice(event_list)
            activate_address = random.choice(veh_address_dict[veh_sending_req])
            temp_list.append([activate_address,
                              veh_sending_req,
                              veh_location[veh_sending_req],
                              random.randint(0, 100),  # 消息时间或者是这则消息的排序
                              [event_ready_for_veh[0], REQ_DISTENCE_REQ, REQ_TIME_REQ]])
        veh_valid_for_all_msg_dict = count_valid_for_req(temp_list, veh_location)

        sorted_temp_list = sorted(temp_list, key=lambda x:x[3])
        for req_msg in sorted_temp_list:
            veh_valid_for_one_msg_list = count_valid_part_fun(req_msg, veh_location)
            for tmp_veh in veh_valid_for_one_msg_list:
                event_for_relay_list = event_owned(tmp_veh, vail_veh)
                if not len(event_for_relay_list):


        # 得到评分列表
        report_cycle = time.clock()
        messages = message(vail_veh,
                           event_list,
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

    _, veh_rating_dict = accident_probability(veh_dict, copy.deepcopy(veh_init_ids), false_ratio)

    veh_meet_rsu = defaultdict(int)
    for veh_s, rsu_meet_num in veh_rsu_all_dict.items():
        veh_meet_rsu[veh_s] = rsu_statistic(rsu_meet_num)

    # 评分发送给RSU
    # RSUs得到的所有评分
    rsu_rating_dic = defaultdict(list)
    for veh_index, msg_list in veh_rating_dict.items():
        for msgs in msg_list:
            rsu_id = veh_meet_rsu[veh_index]
            rsu_rating_dic[rsu_id].append(msgs)

    # 每一个RSU用收到的rate计算对应车辆的offset，使用区块链的来竞争记账权
    rsu_offset_dict = defaultdict(list)
    rsu_pre_offset_dict = defaultdict(list)
    for rsu_offset_id, rsu_ratings in rsu_rating_dic.items():
        pre_offset = offset(rsu_ratings)
        rsu_pre_offset_dict[rsu_offset_id] = pre_offset
        # rsu_offset_dict[rsu_offset_id].append()

    return rsu_rating_dic, rsu_pre_offset_dict


if __name__ == '__main__':
    unfair_msg_ratio_list = []
    unfair_offset_ratio_list = []
    trust_offset_list = []
    rounds = np.arange(0, 1, 0.05)
    for x in rounds:
        # res, rsu_rating_res, veh_ids, accident_list = traditional_version(SIMULATION_ROUND, 0.6)
        rsu_rating_dic, pre_offset_dict = traditional_v2(SIMULATION_ROUND, x)

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


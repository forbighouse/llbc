from test_script.veh_trust.trust_management_simulator import *
from test_script.veh_trust.base_veh_location import *
from utility.utility import *

NUM_REQUEST_VEH = 5
# 车辆请求的内容
REQ_DATA_CONTENT = 0
# 车辆请求的距离要求
REQ_DISTANCE_REQ = 0
# 车辆请求的时间要求
REQ_TIME_REQ = 0
# 观测距离
OBSERVATION_DISTANCE = 100
# 临时参数发起REQ的车辆的数量
NUM_RISE_REQ_FOR_VEH = 0
# 最高速度m/s
MIN_SPEED = 0
MAX_SPEED = 14
# 一轮round_time抵多少秒
SECOND_FOR_ONE_ROUND = 5


def veh_location_init():
    veh_id_list = []
    locaiotn_reading_list = []
    with open('veh_list.txt', 'r') as handler:
        for x in handler:
            x = x.strip('\n').split(';')
            veh_id_list.append(x[0])
            locaiotn_reading_list.append(int(x[1]))
    if DEBUG:
        return veh_id_list, dict(zip(veh_id_list, locaiotn_reading_list))
    else:
        start_point = random.choice(range(5, 20))
        tmp_accumulation_spacing = start_point
        veh_location = defaultdict(int)

        for tmp_veh1 in veh_id_list:
            spacing = random.choice(range(5, 100))
            tmp_accumulation_spacing += spacing
            veh_location[tmp_veh1] = tmp_accumulation_spacing
        return veh_id_list, veh_location


def veh_adjacency_fuc(event_list, veh_location, speed_init_veh_dict, round_time):
    adjacency_dict = defaultdict(dict)
    trajectory_dict = defaultdict(dict)
    # 找到车辆在这一轮的时间和位置
    for tmp_veh_id, tmp_veh_location in veh_location.items():
        tmp_time_location_dict = defaultdict(int)
        time_trajectory = 0
        while time_trajectory < SECOND_FOR_ONE_ROUND:
            tmp_time = round_time*5 + time_trajectory
            moving_distance = time_trajectory * speed_init_veh_dict[tmp_veh_id]
            tmp_location = veh_location[tmp_veh_id] + moving_distance
            tmp_time_location_dict[tmp_time] = tmp_location
            time_trajectory += 1
        trajectory_dict[tmp_veh_id] = tmp_time_location_dict
    # 计算车辆与事件之间的相对距离
    for event1 in event_list:
        adjacency_one_event_dict = defaultdict(dict)
        for tmp_veh, tmp_time_location in trajectory_dict.items():
            tmp_adjacency_dict = defaultdict(int)
            for tmp_time2, tmp_location2 in tmp_time_location.items():
                tmp_adjacency_dict[tmp_time2] = int(distance_cal_x(int(event1[1][0]), tmp_location2))
            adjacency_one_event_dict[tmp_veh] = tmp_adjacency_dict
        adjacency_dict[event1[0]] = adjacency_one_event_dict

    return adjacency_dict, trajectory_dict


def veh_speed_init(veh_ids):
    veh_speed_init_dict = defaultdict(int)
    for tmp_veh1 in veh_ids:
        veh_speed_init_dict[tmp_veh1] = random.choice(range(-MAX_SPEED, MAX_SPEED))
    return veh_speed_init_dict


def veh_valid_fun(adjacency_dict):
    #
    vail_veh = defaultdict(list)
    for event_tag, tmp_id_veh_time_loc in adjacency_dict.items():
        for tmp_id, tmp_veh_time_loc in tmp_id_veh_time_loc.items():
            for tmp_time, tmp_veh_loc in tmp_veh_time_loc.items():
                if tmp_veh_loc < OBSERVATION_DISTANCE:
                    vail_veh[event_tag].append([tmp_id, tmp_time, tmp_veh_loc])
                    # break
    return vail_veh


def bl_address_read(file_address=BLOCKCHAIN_ADDRESS_FILE):
    bl_address_id_list = []
    with open(file_address, 'r') as handler:
        for line in handler:
            line = line.strip('\n').split(';')
            bl_address_id_list.append(line[0])
    return bl_address_id_list


def veh_address_allocation(veh_init_ids, bl_address_ids):
    address_veh_dict = defaultdict(str)
    init_balance_address = defaultdict(int)
    bl_address_ids_list = [bl_address_ids[i:i + 3] for i in range(0, len(bl_address_ids), 3)]
    veh_address_dict = dict(zip(veh_init_ids, bl_address_ids_list))
    for ids, address_list in veh_address_dict.items():
        for address in address_list:
            address_veh_dict[address] = ids
            init_balance_address[address] = random.randint(0,100)
    return veh_address_dict, address_veh_dict, init_balance_address


def count_valid_veh_around_event(msg_list, accident_dict, veh_location):
    re_valid_veh_dic = defaultdict(list)
    for one_msg in msg_list:
        for tmp_veh_id, tmp_veh_location in veh_location.items():
            if tmp_veh_id != one_msg[1]:
                if int(distance_cal_x(accident_dict[one_msg[4][0]][0][0], tmp_veh_location)) <= OBSERVATION_DISTANCE:
                    re_valid_veh_dic[one_msg[4][0]].append(tmp_veh_id)
    return re_valid_veh_dic


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


def random_address(_list): return random.choice(_list)


def bl_reputation_count(veh_id=NUM_RISE_REQ_FOR_VEH): return veh_id


def traditional_v2(round_time, false_ratio):
    # //rsu的位置初始化，dict, (id, location)
    rsu_ids, rsu_location_list = rsu_location()
    # //事件位置初始化 dict, location
    event_list, accident_dict = accident_factory()
    # //车辆id和位置初始化
    veh_ids, veh_location = veh_location_init()
    # //车辆速度及方向初始化
    speed_init_veh_dict = veh_speed_init(veh_ids)
    # //地址钱包初始化
    veh_init_ids = veh_id_fun()
    bl_address_ids = bl_address_read()
    #     //每辆车拥有的地址veh_address_dict，每个地址对应的车address_veh_dict。
    veh_address_dict, address_veh_dict, init_balance = veh_address_allocation(veh_init_ids, bl_address_ids)
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

    # //记录车辆的历史消息或位置等
    veh_seq_for_epoch_dict = defaultdict(list)
    veh_req_for_epoch_dict = defaultdict(list)

    for epoch in range(round_time):
        # //得到所有车辆与每一个事件之间的距离
        adjacency_dict, _ = veh_adjacency_fuc(event_list, veh_location, speed_init_veh_dict, epoch)
        #     //每个事件的有效可观测车辆集合vail_veh
        vail_veh = veh_valid_fun(adjacency_dict)

        send_request_veh_id_list = random.sample(veh_ids, NUM_REQUEST_VEH)
        veh_req_for_epoch_dict[epoch].append(send_request_veh_id_list)
        veh_seq_for_epoch_dict[epoch].append(vail_veh)
        # 消息的发送序列，为简化，并不存在同时发布的消息
        req_msg_order = list(range(len(send_request_veh_id_list)))
        random.shuffle(req_msg_order)
        temp_msg_list = []
        for veh_sending_req in send_request_veh_id_list:
            event_ready_for_veh = random.choice(event_list)
            activate_address = random.choice(veh_address_dict[veh_sending_req])
            # temp_list包含了所有的【请求消息】
            #     0          1           2            3                       4
            # |<-地址->|<-请求车辆->|<-车辆位置->|<-消息次序->|<-[event的编号、距离要求、时间要求]->|
            temp_msg_list.append([
                activate_address,                              # 0请求车辆随机钱包地址
                veh_sending_req,                               # 1请求车辆
                veh_location[veh_sending_req],                 # 2请求位置
                req_msg_order[send_request_veh_id_list.index(veh_sending_req)],   # 3消息时间或排序
                [event_ready_for_veh[0], REQ_DISTANCE_REQ, REQ_TIME_REQ]])        # [event的编号、距离要求、时间要求]
        # veh_valid_for_all_msg_dict = count_valid_for_req(temp_msg_list, veh_location)
        veh_valid_for_all_msg_dict = count_valid_veh_around_event(temp_msg_list, accident_dict, veh_location)
        recv_msg_dict = defaultdict(list)
        # recv_msg_dict包含【反馈消息】
        #     0         1            2           3             4         5             6
        # |<- 地址->|<-反馈车辆->|<-请求地址->|<-事件编号->|<-事件内容->|<-发出位置->|<-发出时间->|
        for tmp_msg in temp_msg_list:
            for one_veh in veh_valid_for_all_msg_dict[tmp_msg[4][0]]:
                recv_msg_dict[tmp_msg[1]].append([
                    random_address(veh_address_dict[one_veh]),  # 0随机钱包地址
                    one_veh,                                    # 1反馈车辆
                    tmp_msg[0],                                 # 2请求车辆
                    tmp_msg[4][0],                              # 3请求时间
                    1,                                          # 4事件内容，magic word
                    veh_location[one_veh],                      # 5反馈位置
                    0                                           # 6反馈时间
                ])

        for tmp_veh, tmp_msg in recv_msg_dict.items():
            veh_history_reputation = bl_reputation_count(tmp_msg[0])




        sorted_temp_list = sorted(temp_msg_list, key=lambda x:x[3])
        for req_msg in sorted_temp_list:
            veh_valid_for_one_msg_list = count_valid_part_fun(req_msg, veh_location)
            for tmp_veh in veh_valid_for_one_msg_list:
                event_for_relay_list = event_owned(tmp_veh, vail_veh)
                # if not len(event_for_relay_list):


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


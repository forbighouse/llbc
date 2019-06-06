from test_script.veh_trust.trust_management_simulator import *
from test_script.veh_trust.config import *
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
# 总共多少轮
ROUNDS = 12


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


def veh_trajectory_fuc1(veh_location, speed_init_veh_dict, all_rounds):
    trajectory_dict = defaultdict(dict)
    # 找到车辆在这一轮的时间和位置

    tmp_time_location_dict = defaultdict(int)
    for tmp_veh_id, tmp_veh_location in veh_location.items():

        for round_time in range(all_rounds):
            time_trajectory = 0
            while time_trajectory < SECOND_FOR_ONE_ROUND:
                tmp_time = round_time*5 + time_trajectory
                moving_distance = tmp_time * speed_init_veh_dict[tmp_veh_id]
                tmp_location = tmp_veh_location + moving_distance
                tmp_time_location_dict[tmp_time] = tmp_location
                time_trajectory += 1
                trajectory_dict[tmp_veh_id] = copy.deepcopy(tmp_time_location_dict)
    return trajectory_dict


def veh_adjacency_fuc(event_list, veh_trajectory_fuc):
    adjacency_dict = defaultdict(dict)
    trajectory_dict = veh_trajectory_fuc
    # 计算车辆与事件之间的相对距离
    for event1 in event_list:
        adjacency_one_event_dict = defaultdict(dict)
        for tmp_veh, tmp_time_location in trajectory_dict.items():
            tmp_adjacency_dict = defaultdict(int)
            for tmp_time2, tmp_location2 in tmp_time_location.items():
                tmp_adjacency_dict[tmp_time2] = int(distance_cal_x(int(event1[1][0]), tmp_location2))
            adjacency_one_event_dict[tmp_veh] = tmp_adjacency_dict
        adjacency_dict[event1[0]] = adjacency_one_event_dict
    return adjacency_dict


def veh_speed_init():
    veh_id_list = []
    speed_reading_list = []
    with open(VEH_SPEED_FILE, 'r') as handler:
        for x in handler:
            x = x.strip('\n').split(';')
            veh_id_list.append(x[0])
            speed_reading_list.append(int(x[1]))
    if DEBUG:
        return dict(zip(veh_id_list, speed_reading_list))
    else:
        veh_speed_init_dict = defaultdict(int)
        for tmp_veh1 in veh_id_list:
            veh_speed_init_dict[tmp_veh1] = random.choice(range(-MAX_SPEED, MAX_SPEED))
        return veh_speed_init_dict


def veh_valid_fun(adjacency_dict):
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


def bl_balance_init(bl_address_init):
    bl_balance_init_dict = defaultdict(int)
    for address1 in bl_address_init:
        bl_balance_init_dict[address1] = random.choice(range(-100, 100))
    return bl_balance_init_dict


def veh_address_allocation(veh_init_ids, bl_address_ids):
    address_veh_dict = defaultdict(str)
    init_balance_address = defaultdict(int)
    bl_address_ids_list = [bl_address_ids[i:i + 3] for i in range(0, len(bl_address_ids), 3)]
    veh_address_dict = dict(zip(veh_init_ids, bl_address_ids_list))
    for ids, address_list in veh_address_dict.items():
        for address in address_list:
            address_veh_dict[address] = ids
            init_balance_address[address] = random.randint(0, 100)
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


def message_cleaning(recv_msg_dict):
    tmp_msg_dict = defaultdict(dict)
    tmp_valid_msg_dict = defaultdict(dict)
    for recv_address, msg_list in recv_msg_dict.items():
        tmp_msg_collection_dict = defaultdict(list)
        tmp_valid_msg_collection_dict = defaultdict(list)
        for msg1 in msg_list:
            tmp_msg_collection_dict[msg1[0]].append(msg1)
            tmp_msg_dict[recv_address] = copy.deepcopy(tmp_msg_collection_dict)
            # 针对请求时间，筛选可用的消息
            little_num = msg1[7] - msg1[4]
            # //可能按时间清洗后出现却req的问题
            if msg1[7] > msg1[4] and little_num < 15:
                tmp_valid_msg_collection_dict[msg1[0]].append(copy.deepcopy(msg1))
                tmp_valid_msg_dict[recv_address] = copy.deepcopy(tmp_valid_msg_collection_dict)
    return tmp_msg_dict, tmp_valid_msg_dict


def message_filter(clean_msg_dict):
    msg_valid_list = []
    for recv_address1, msg_list1 in clean_msg_dict.items():
        for recv_address2, tmp_msg2_list in msg_list1.items():
            if len(tmp_msg2_list) > 1:
                # random.choice(tmp_msg2_list)
                # tmp_msg_valid_collection_dict[recv_address1].append(random.choice(tmp_msg2_list))
                msg_valid_list.append(random.choice(tmp_msg2_list))
            else:
                msg_valid_list.append(copy.deepcopy(tmp_msg2_list[0]))
    return msg_valid_list


def message_disturb(res_valid_for_req_list, fal_rat, answer_dict):
    tmp_list = copy.deepcopy(res_valid_for_req_list)
    num_answer_init = len(tmp_list)

    num_false_msg = int(fal_rat*num_answer_init)

    list_sample = random.sample(tmp_list, num_false_msg)
    for msg4 in list_sample:
        msg4[5] = 0
    for veh_answer in tmp_list:
        answer_dict[hash_str(veh_answer, "answer")] = veh_answer
    return tmp_list


def probability_count_fuc1(msg):
    probability_true_resp_dict = defaultdict(list)
    for items in msg:
        r1 = 1 - math.pow(0.01*items[6], 3)
        r2 = math.exp(-0.084*(items[7]-items[4]))
        pby_resq = ((r1 + r2) / 2)
        probability_true_resp_dict[items[5]].append(pby_resq)
    return probability_true_resp_dict


def Bayes_infer(msg_dict, pe=PE):
    if len(msg_dict) > 1:
        tmp_pro_dict = defaultdict(list)
        for event_id, pby_list in msg_dict.items():
            if event_id == 1:
                for i in pby_list:
                    tmp_pro_dict[event_id].append(i)
                    tmp_pro_dict[event_id-1].append(1-i)
            elif event_id == 0:
                for i in pby_list:
                    tmp_pro_dict[event_id].append(i)
                    tmp_pro_dict[event_id+1].append(1-i)
        tmp_res_dict = defaultdict(float)
        for event_id in tmp_pro_dict.keys():
            if event_id == 1:
                part1 = pe * multi_plicator(tmp_pro_dict[event_id])
                part2 = (1-pe) * multi_plicator(tmp_pro_dict[0])
                tmp_res_dict[event_id] = part1 / (part1 + part2)
            elif event_id == 0:
                part1 = pe * multi_plicator(tmp_pro_dict[event_id])
                part2 = (1-pe) * multi_plicator(tmp_pro_dict[1])
                tmp_res_dict[event_id] = part1 / (part1 + part2)

        return event_pro_compare(tmp_res_dict)
    elif len(msg_dict) == 1:
        return list(msg_dict.keys())[0]


def event_pro_compare(_dict):
    if _dict[0] > _dict[1]:
        return 0
    else:
        return 1


def traditional_v2(false_ratio, round_time=ROUNDS):
    # //事件位置初始化 dict, location
    event_list, accident_dict = accident_factory()
    # //车辆id和位置初始化
    veh_ids, veh_location = veh_location_init()
    # //车辆速度及方向初始化
    speed_init_veh_dict = veh_speed_init()
    # //地址钱包初始化
    veh_init_ids = veh_id_fun()
    bl_address_ids = bl_address_read()
    # //钱包金额初始化
    bl_balance = bl_balance_init(bl_address_ids)
    #     //每辆车拥有的地址veh_address_dict，每个地址对应的车address_veh_dict。
    veh_address_dict, address_veh_dict, init_balance = veh_address_allocation(veh_init_ids, bl_address_ids)

    # //得到所有车辆与每一个事件之间的距离
    veh_trajectory_dict = veh_trajectory_fuc1(veh_location, speed_init_veh_dict, round_time)
    adjacency_dict = veh_adjacency_fuc(event_list, veh_trajectory_dict)
    #     //每个事件的有效可观测车辆集合vail_veh
    vail_veh = veh_valid_fun(adjacency_dict)

    # // 设置请求车辆
    send_request_veh_id_list = random.sample(veh_ids, NUM_REQUEST_VEH)
    # 设置请求消息时间
    req_msg_order = random.sample(range(round_time*5), len(send_request_veh_id_list))
    random.shuffle(req_msg_order)
    temp_msg_list = []
    for veh_sending_req in send_request_veh_id_list:
        event_ready_for_veh = random.choice(event_list)
        activate_address = random.choice(veh_address_dict[veh_sending_req])
        # temp_list包含了所有的【请求消息】
        #     0          1           2            3                       4
        # |<-地址->|<-请求车辆->|<-车辆位置->|<-消息次序->|<-[event的编号、距离要求、时间要求]->|
        temp_msg_list.append([
            activate_address,                                                 # 0请求车辆随机钱包地址
            veh_sending_req,                                                  # 1请求车辆
            veh_location[veh_sending_req],                                    # 2请求位置
            req_msg_order[send_request_veh_id_list.index(veh_sending_req)],   # 3消息时间或排序
            [event_ready_for_veh[0], REQ_DISTANCE_REQ, REQ_TIME_REQ]])        # [event的编号、距离要求、时间要求]
    # veh_valid_for_all_msg_dict = count_valid_for_req(temp_msg_list, veh_location)
    # veh_valid_for_all_msg_dict = count_valid_veh_around_event(temp_msg_list, accident_dict, veh_location)
    recv_msg_dict = defaultdict(list)
    # recv_msg_dict包含【反馈消息】
    #     0         1            2           3             4             5          6             7
    # |<- 地址->|<-反馈车辆->|<-请求地址->|<-请求事件->||<-请求时间->|<-事件内容->|<-反馈位置->|<-反馈时间->|
    for tmp_msg in temp_msg_list:
        veh_id_name = None
        rd_address = None
        for one_veh in vail_veh[tmp_msg[4][0]]:
            if veh_id_name != one_veh[0]:
                veh_id_name = one_veh[0]
                rd_address = random_address(veh_address_dict[one_veh[0]])
                recv_msg_dict[tmp_msg[1]].append([
                    rd_address,     # 0随机钱包地址
                    one_veh[0],     # 1反馈车辆
                    tmp_msg[0],     # 2请求地址
                    tmp_msg[4][0],  # 3请求事件
                    tmp_msg[3],     # 4请求时间
                    1,              # 5事件内容，magic word
                    one_veh[2],     # 6反馈相对位置
                    one_veh[1]      # 7反馈时间
                ])
            else:
                recv_msg_dict[tmp_msg[1]].append([
                    rd_address,     # 0随机钱包地址
                    one_veh[0],     # 1反馈车辆
                    tmp_msg[0],     # 2请求地址
                    tmp_msg[4][0],  # 3请求事件
                    tmp_msg[3],     # 4请求时间
                    1,              # 5事件内容，magic word
                    one_veh[2],     # 6反馈相对位置
                    one_veh[1]      # 7反馈时间
                ])
    # //以反馈地址将反馈信息进行整理，第二个返回值根据请求的时间要求筛选出可用的反馈消息
    clean_msg_v1_dict, clean_valid_msg_v1_dict = message_cleaning(recv_msg_dict)
    # //从筛选后的反馈消息中只随机挑出来一条
    res_valid_for_req_dict = message_filter(clean_valid_msg_v1_dict)
    # //加随机的干扰
    res_disturb_for_req_dict = message_disturb(res_valid_for_req_dict, false_ratio)
    # //将反馈消息按照反馈的事件内容进行分类
    probability_req_dict = defaultdict(dict)
    for tmp_req_id, tmp_valid_msg_list in res_disturb_for_req_dict.items():
        probability_req_dict[tmp_req_id] = probability_count_fuc1(tmp_valid_msg_list)
    # //从反馈消息得到
    res_event_deter_dict = defaultdict(dict)
    for veh_req_id, msg_list_pby in probability_req_dict.items():
        res_event_deter_dict[veh_req_id] = Bayes_infer(msg_list_pby)

    return res_event_deter_dict


def first_picture(pro_msg_dict):
    false0 = 0
    false1 = 0
    for veh_req_id, pro_tru in pro_msg_dict.items():
        if pro_tru == 0:
            false0 += 1
        else:
            false1 += 1
    return false0 / (false0 + false1)


if __name__ == '__main__':
    # false_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    false_list = np.arange(0, 1, 0.01)
    res_first_picture_dict = defaultdict(float)
    for _false_ratio in false_list:
        print("false_ratio = ", _false_ratio)
        pro_event_deter_dict = traditional_v2(_false_ratio, ROUNDS)
        ratio = first_picture(pro_event_deter_dict)
        res_first_picture_dict[_false_ratio] = ratio

    false_msg_ratio_json = json.dumps(res_first_picture_dict)
    a = open(r"first_picture.txt", "w", encoding='UTF-8')
    a.write(false_msg_ratio_json)
    a.close()







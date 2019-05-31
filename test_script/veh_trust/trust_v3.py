from test_script.veh_trust.trust_v2 import *


def veh_location_every_round(veh_location, speed_init_veh_dict, round_time):
    veh_location_all_dict = defaultdict(dict)
    for round in range(round_time*5):
        tmp_veh_location_dict = defaultdict(int)
        for veh_id, veh_loc in veh_location.items():
            tmp_veh_location_dict[veh_id] = veh_loc + (speed_init_veh_dict[veh_id]*round)
        veh_location_all_dict[round] = copy.deepcopy(tmp_veh_location_dict)
    return veh_location_all_dict


def veh_reference_set(res_disturb_for_req_dict, veh_location_all_dict):

    for tmp_veh_id1, tmp_msg_list in res_disturb_for_req_dict.items():
        for tmp_msg in tmp_msg_list:
            for tmp_veh_location in veh_location_all_dict[tmp_msg[7]]:
                tmp_msg[1]



def traditional_v3(false_ratio, round_time=ROUNDS):
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
    # //根据false_ratio改变其中一些消息的内容，组成假消息
    res_disturb_for_req_dict = message_disturb(res_valid_for_req_dict, false_ratio)
    # //每一秒，车辆的位置
    veh_location_all_dict = veh_location_every_round(veh_location, speed_init_veh_dict, round_time)
    # //每一个响应对应的相关车辆集
    veh_reference_set_dict = veh_reference_set(res_disturb_for_req_dict, veh_location_all_dict)

    # //将反馈消息按照反馈的事件内容进行分类
    probability_req_dict = defaultdict(dict)
    for tmp_req_id, tmp_valid_msg_list in res_disturb_for_req_dict.items():
        probability_req_dict[tmp_req_id] = probability_count_fuc1(tmp_valid_msg_list)
    # //从反馈消息得到
    res_event_deter_dict = defaultdict(dict)
    for veh_req_id, msg_list_pby in probability_req_dict.items():
        res_event_deter_dict[veh_req_id] = Bayes_infer(msg_list_pby)

    return res_event_deter_dict


if __name__ == '__main__':
    # false_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    false_list = np.arange(0, 1, 0.01)
    res_first_picture_dict = defaultdict(float)
    for _false_ratio in false_list:
        print("false_ratio = ", _false_ratio)
        pro_event_deter_dict = traditional_v3(_false_ratio, ROUNDS)
        ratio = first_picture(pro_event_deter_dict)
        res_first_picture_dict[_false_ratio] = ratio

    false_msg_ratio_json = json.dumps(res_first_picture_dict)
    a = open(r"first_picture.txt", "w", encoding='UTF-8')
    a.write(false_msg_ratio_json)
    a.close()
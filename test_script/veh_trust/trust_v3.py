from test_script.veh_trust.trust_v2 import *


# 时间节点前的请求权重
TIME1 = 0.5
# 时间节点后的请求权重
TIME2 =0.5
# 累计消费信誉权重
CUSUME = 0.5
# 累计响应次数权重
RESPONCE = 0.5


def bl_operation_init(bl_address_ids):
    bl_operation_init_dict = defaultdict(list)
    for address1 in bl_address_ids:
        # [时间节点之前的请求+响应，时间节点之后的请求+响应]
        bl_operation_init_dict[address1].append([random.choice(range(0, 50)), random.choice(range(0, 50))])
        # [时间节点之前的响应，时间节点之后的响应]
        bl_operation_init_dict[address1].append([random.choice(range(0, 50)), random.choice(range(0, 50))])
    return bl_operation_init_dict


def cache_all_veh_init(veh_ids):
    # 使用车辆而不是钱包，只是为了简化计算，毕竟理论上三个钱包共享内存
    cache_request_veh_dict = defaultdict(list)
    cache_answer_veh_dict = defaultdict(list)
    cache_rating_veh_dict = defaultdict(list)
    return cache_request_veh_dict, cache_answer_veh_dict, cache_rating_veh_dict


def hash_request_msg_init():
    return defaultdict(list)


def hash_answer_msg_init():
    return defaultdict(list)


def hash_rate_msg_init():
    return defaultdict(list)


def status_request_cache(cache_request_veh_dict, tmp_msg_list, hash_request):
    for msgs in tmp_msg_list:
        hash_request[hash_str(msgs, "request")] = msgs
        cache_request_veh_dict[msgs[3]].append(msgs)
    return cache_request_veh_dict


def status_answer_cache(cache_answer_veh_dict_veh_dict, res_disturb_for_req_dict):
    for req_id, recv_msg in res_disturb_for_req_dict.items():
        for tmp_msg in recv_msg:
            cache_answer_veh_dict_veh_dict[tmp_msg[7]].append(tmp_msg)
    return cache_answer_veh_dict_veh_dict


def status_rating_cache(cache_rating_veh_dict, rating_result_dict):
    for rate_veh_id, rate_list in rating_result_dict.items():
        for rates in rate_list:
            cache_rating_veh_dict[rates[3]].append(rates)
    return cache_rating_veh_dict


def veh_location_every_round(veh_location, speed_init_veh_dict, round_time):
    veh_location_all_dict = defaultdict(dict)
    for round in range(round_time*5):
        tmp_veh_location_dict = defaultdict(int)
        for veh_id, veh_loc in veh_location.items():
            tmp_veh_location_dict[veh_id] = veh_loc + (speed_init_veh_dict[veh_id]*round)
        veh_location_all_dict[round] = copy.deepcopy(tmp_veh_location_dict)
    return veh_location_all_dict


# 针对每一个响应消息，找出它的相关车辆集
def veh_reference_set(res_disturb_for_req_list, veh_location_all_dict):
    veh_reference_set_dict = defaultdict(dict)
    veh_for_disturb_msg_v1_dict = defaultdict(list)
    for tmp_msg_ in res_disturb_for_req_list:
        veh_persific_round = veh_location_all_dict[tmp_msg_[7]]
        for tmp_veh_id2, tmp_veh_location in veh_persific_round.items():
            if distance_cal_x(veh_persific_round[tmp_msg_[1]], tmp_veh_location) < 300:
                if tmp_veh_id2 != tmp_msg_[1]:
                    veh_for_disturb_msg_v1_dict[tmp_msg_[1]].append(tmp_veh_id2)

        veh_reference_set_dict[tmp_veh_id1] = copy.deepcopy(veh_for_disturb_msg_v1_dict)
    return veh_reference_set_dict


def rating_for_address(veh_reference_set_dict, bl_blance_set, bl_operation_set):
    rating_list_event_dict = defaultdict(dict)
    test_result_list = []
    # vertify是一个请求下，返回的若干个响应
    for req_id, vertify_msg in veh_reference_set_dict.items():
        for vertify_veh_id, answer_list in vertify_msg.items():
            # credits_list = probability_count_fuc2(answer_list, bl_operation_set)
            credits_list = probability_count_fuc3(answer_list, bl_operation_set)
            # 加入测试代码test_result，
            infer_result, test_result = bayes_infer_v2(credits_list)
            test_result_list.append(test_result)
            tmp_rating_list = []
            for answer1 in answer_list:
                tmp_rating_tag = 0
                if answer1[5] == infer_result:
                    tmp_rating_tag = 1  # 评分
                else:
                    tmp_rating_tag = -1  # 评分
                tmp_rating_list.append([
                    answer1[2],                   # 0请求哈希（地址）
                    answer1[4],                   # 1请求时间
                    answer1[0],                   # 2响应哈希（地址）
                    answer1[7],                   # 3响应时间
                    vertify_veh_id,               # 4评分地址
                    tmp_rating_tag,               # 5评分
                    hash_str(answer1, "answer")   # -1响应的hash
                ])
                rating_list_event_dict[vertify_veh_id] = copy.deepcopy(tmp_rating_list)
    return rating_list_event_dict


def probability_count_fuc2(msg, bl_op):
    probability_true_resp_dict = defaultdict(list)
    tmp_weight_recent_dict = defaultdict(list)
    tmp_weight_past_dict = defaultdict(list)

    for items in msg:
        r1 = 1 - math.pow(0.08*(items[7]-items[4]), 3)
        r2 = math.exp(-0.007*items[6])
        pby_resq = ((r1 + r2) / 2)
        probability_true_resp_dict[items[5]].append(pby_resq)

        # 历史消费信誉，2天或2周时间间隔，例如 近2天/总4天，算出总的活跃度
        tmp_weight_recent_dict[items[5]].append(bl_op[items[0]][0][1])
        tmp_weight_past_dict[items[5]].append(bl_op[items[0]][0][0])

    return probability_true_resp_dict


def probability_count_fuc3(msg, bl_op):
    probability_true_resp_dict = defaultdict(list)
    tmp_weight_recent_dict = defaultdict(list)
    tmp_weight_past_dict = defaultdict(list)

    for items in msg:
        r2 = 0.5 + math.exp(-0.014*(items[6]+50))
        probability_true_resp_dict[items[5]].append(r2)

        # 历史消费信誉，2天或2周时间间隔，例如 近2天/总4天，算出总的活跃度
        tmp_weight_recent_dict[items[5]].append(bl_op[items[0]][0][1])
        tmp_weight_past_dict[items[5]].append(bl_op[items[0]][0][0])

    return probability_true_resp_dict


def bayes_infer_v2(pro_list_dict, pe=PE):
    tmp_pro_dict = defaultdict(list)
    test_result = []
    for event_id, pby_list in pro_list_dict.items():
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
            part2 = (1-pe) * multi_plicator(tmp_pro_dict[event_id-1])
            tmp_res_dict[event_id] = part1 / (part1 + part2)
        elif event_id == 0:
            part1 = pe * multi_plicator(tmp_pro_dict[event_id])
            part2 = (1-pe) * multi_plicator(tmp_pro_dict[1])
            tmp_res_dict[event_id] = part1 / (part1 + part2)
    tmp_res = sorted(tmp_res_dict.items(), key=lambda tmp_res_dict: tmp_res_dict[1], reverse=True)
    test_result.append([tmp_res, pro_list_dict])
    return tmp_res[0][0], test_result


def comparison_rating_answer(rating_result_dict, hash_answer_msg):
    hash_rate_answer_dict = defaultdict(list)
    ratio_dict = defaultdict(list)
    for _, rate_list in rating_result_dict.items():
        for answer2 in rate_list:
            hash_rate_answer_dict[answer2[-1]].append(answer2)
    for hash_id, rating_list in hash_rate_answer_dict.items():
        if hash_answer_msg[hash_id][5] == 1:
            for rates in rating_list:
                if rates[5] == 1:
                    ratio_dict[1].append(rates)
                elif rates[5] == -1:
                    ratio_dict[-1].append(rates)
        elif hash_answer_msg[hash_id][5] == 0:
            for rates in rating_list:
                if rates[5] == 1:
                    ratio_dict[-1].append(rates)
                elif rates[5] == -1:
                    ratio_dict[1].append(rates)
    return ratio_dict


def traditional_v3(false_list, round_time=ROUNDS):
    # //事件位置初始化 dict, location
    event_list, accident_dict = accident_factory()
    # //车辆id和位置初始化
    veh_ids, veh_location = veh_location_init()
    # //车辆速度及方向初始化
    speed_init_veh_dict = veh_speed_init()
    # //地址钱包初始化
    veh_init_ids = veh_id_init()
    bl_address_ids = bl_address_read()
    # //每辆车拥有的地址veh_address_dict，每个地址对应的车address_veh_dict。
    veh_address_dict, address_veh_dict, init_balance = veh_address_allocation(veh_init_ids, bl_address_ids)
    # //钱包金额初始化
    bl_balance = bl_balance_init(bl_address_ids)
    # //钱包网络参与初始化（仿真）
    bl_operation = bl_operation_init(bl_address_ids)
    # //所有车辆节点的请求和响应缓存区初始化（仿真）
    cache_request_veh_dict, cache_answer_veh_dict, cache_rating_veh_dict = cache_all_veh_init(veh_ids)
    # //初始化全局请求字典，键是请求消息的hash值，值是消息本身
    hash_request_msg = hash_request_msg_init()

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
    tmp_msg_list = []
    for veh_sending_req in send_request_veh_id_list:
        event_ready_for_veh = random.choice(event_list)
        activate_address = random.choice(veh_address_dict[veh_sending_req])
        # temp_list包含了所有的【请求消息】
        #     0          1           2            3                       4
        # |<-地址->|<-请求车辆->|<-车辆位置->|<-消息次序->|<-[event的编号、距离要求、时间要求]->|
        tmp_msg_list.append([
            activate_address,                                                 # 0请求地址
            veh_sending_req,                                                  # 1请求车辆
            veh_location[veh_sending_req],                                    # 2请求位置
            req_msg_order[send_request_veh_id_list.index(veh_sending_req)],   # 3请求时间
            [event_ready_for_veh[0], REQ_DISTANCE_REQ, REQ_TIME_REQ]])        # 4[event的编号、距离要求、时间要求]
    # //向仿真参数里写入请求消息
    cache_request_status = status_request_cache(cache_request_veh_dict, tmp_msg_list, hash_request_msg)

    # veh_valid_for_all_msg_dict = count_valid_for_req(tmp_msg_list, veh_location)
    # veh_valid_for_all_msg_dict = count_valid_veh_around_event(tmp_msg_list, accident_dict, veh_location)
    recv_msg_dict = defaultdict(list)
    # recv_msg_dict包含【反馈消息】
    #     0         1            2           3             4             5          6             7
    # |<- 地址->|<-反馈车辆->|<-请求地址->|<-请求事件->||<-请求时间->|<-事件内容->|<-反馈位置->|<-反馈时间->|
    for tmp_msg in tmp_msg_list:
        veh_id_name = None
        rd_address = None
        for one_veh in vail_veh[tmp_msg[4][0]]:
            if veh_id_name != one_veh[0]:
                veh_id_name = one_veh[0]
                rd_address = random_address(veh_address_dict[one_veh[0]])
                recv_msg_dict[tmp_msg[1]].append([
                    rd_address,     # 0响应地址
                    one_veh[0],     # 1响应车辆
                    tmp_msg[0],     # 2请求地址
                    tmp_msg[4][0],  # 3请求事件
                    tmp_msg[3],     # 4请求时间
                    1,              # 5事件内容，magic word
                    one_veh[2],     # 6响应请求相对距离
                    one_veh[1]      # 7响应时间
                ])
            else:
                recv_msg_dict[tmp_msg[1]].append([
                    rd_address,     # 0响应地址
                    one_veh[0],     # 1响应车辆
                    tmp_msg[0],     # 2请求地址
                    tmp_msg[4][0],  # 3请求事件
                    tmp_msg[3],     # 4请求时间
                    1,              # 5事件内容，magic word
                    one_veh[2],     # 6响应请求相对距离
                    one_veh[1]      # 7响应时间
                ])
    # //以反馈地址将反馈信息进行整理，第二个返回值根据请求的时间要求筛选出可用的反馈消息
    clean_msg_v1_dict, clean_valid_msg_v1_dict = message_cleaning(recv_msg_dict)
    # //从筛选后的反馈消息中只随机挑出来一条
    res_valid_for_req_list = message_filter(clean_valid_msg_v1_dict)
    # //存储仿真结果
    res_dict = defaultdict(float)
    for _false_ratio in false_list:
        # //初始化响应、评分字典
        hash_answer_msg = hash_answer_msg_init()
        hash_rate_msg = hash_rate_msg_init()
        # //根据false_ratio改变其中一些消息的内容，组成假消息
        res_disturb_for_req_list = message_disturb(res_valid_for_req_list, 0.7, hash_answer_msg)
        # //每一秒车辆的位置
        veh_location_all_dict = veh_location_every_round(veh_location, speed_init_veh_dict, round_time)
        # //每一个响应对应的相关车辆集
        veh_reference_set_dict = veh_reference_set(res_disturb_for_req_list, veh_location_all_dict)
        # //计算针对响应车辆的评分列表，列表项为：
        #      0            1           2          3
        # |<-请求哈希->|<-响应哈希->|<-评分哈希->|<-响应评分->|
        rating_result_dict = rating_for_address(veh_reference_set_dict, bl_balance, bl_operation)
        result_dict = comparison_rating_answer(rating_result_dict, hash_answer_msg)
        ratio = rate_ratio(result_dict)
        print("{} {} {} {}".format("false_ratio = ", _false_ratio, "ratio = ", ratio))
        res_dict[_false_ratio] = ratio

    # //向仿真参数里写入响应消息
    # cache_answer_status = status_answer_cache(cache_answer_veh_dict, res_disturb_for_req_dict)
    # # //向仿真参数理写入评分
    # cache_rating_status = status_rating_cache(cache_rating_veh_dict, rating_result_dict)

    return res_dict


def rate_ratio(ratio_dict):
    num_pos_rate = len(ratio_dict[1])
    num_neg_rate = len(ratio_dict[-1])
    print("{} {} {} {}".format("*1:", num_pos_rate, "*-1:", num_neg_rate))
    return num_neg_rate / (num_pos_rate + num_neg_rate)


def mean_for_list(input_list):
    sum_num = 0
    for nums in input_list:
        sum_num += nums
    return sum_num / len(input_list)


if __name__ == '__main__':
    # 事务广播出去，然后不论谁在发起事务的时候需要将这些结果打包确认
    # 需要一个随机游走角色，负责检查各个
    # false_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    false_list = np.arange(0, 1.05, 0.05)
    # ==================================================================
    # out_dict = traditional_v3(false_list, ROUNDS)
    # ==================================================================
    average_dict = defaultdict(list)
    for i in range(100):
        print("round: ", i)
        res_dict = traditional_v3(false_list, ROUNDS)
        for ratios, num in res_dict.items():
            average_dict[ratios].append(num)
    out_dict = defaultdict(int)
    for ratios1, num_list in average_dict.items():
        out_dict[ratios1] = mean_for_list(num_list)
    # ================================================================
    false_msg_ratio_json = json.dumps(out_dict)
    a = open(r"first_picture.txt", "w", encoding='UTF-8')
    a.write(false_msg_ratio_json)
    a.close()

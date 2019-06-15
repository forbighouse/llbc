# from test_script.veh_trust.trust_v3 import *
from test_script.veh_trust.trust_v4 import *
from test_script.veh_trust.init_fun import *
from test_script.veh_trust.probability_count import *


def request_generator(veh_ids, event_list, veh_address_dict, veh_trajectory_dict, round_time):
    # 设置请求消息时间
    sending_msg_list = []
    trans_num_list = transaction_emerge_generator(2, round_time)
    for index_id, msg_nums in enumerate(trans_num_list):
        if msg_nums > 0:
            tmp_sending_veh_list = random.sample(veh_ids, msg_nums)
            for tmp_sending_veh in tmp_sending_veh_list:
                event_ready_for_veh = random.choice(event_list)
                activate_address = random.choice(veh_address_dict[tmp_sending_veh])
                # temp_list包含了所有的【请求消息】
                #     0          1           2            3                       4
                # |<-地址->|<-请求车辆->|<-车辆位置->|<-消息次序->|<-[event的编号、距离要求、时间要求]->|
                sending_msg_list.append([
                    activate_address,                                # 0请求地址
                    tmp_sending_veh,                                 # 1请求车辆
                    veh_trajectory_dict[tmp_sending_veh][index_id],  # 2请求位置
                    index_id,                                        # 3请求时间
                    [event_ready_for_veh[0], REQ_DISTANCE_REQ, REQ_TIME_REQ]])
    return sending_msg_list


def answer_generator(tmp_msg_list, vail_veh, veh_address_dict):
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
                    rd_address,  # 0响应地址
                    one_veh[0],  # 1响应车辆
                    tmp_msg[0],  # 2请求地址
                    tmp_msg[4][0],  # 3请求事件
                    tmp_msg[3],  # 4请求时间
                    1,  # 5事件内容，magic word
                    one_veh[2],  # 6响应请求相对距离
                    one_veh[1]  # 7响应时间
                ])
            else:
                recv_msg_dict[tmp_msg[1]].append([
                    rd_address,  # 0响应地址
                    one_veh[0],  # 1响应车辆
                    tmp_msg[0],  # 2请求地址
                    tmp_msg[4][0],  # 3请求事件
                    tmp_msg[3],  # 4请求时间
                    1,  # 5事件内容，magic word
                    one_veh[2],  # 6响应请求相对距离
                    one_veh[1]  # 7响应时间
                ])
    return recv_msg_dict


def transaction_pack(tmp_msg_list, filter_answer_set_dict, rating_veh_dict, hash_answer_msg):
    trans_dict = defaultdict(list)
    for req_msgs in tmp_msg_list:
        transaction_structure = defaultdict(dict)
        transaction_structure["request_msg"] = req_msgs
        transaction_structure["request_hash"] = hash_str(req_msgs, "request")
        transaction_structure["answer_list"] = filter_answer_set_dict[req_msgs[0]]
        transaction_structure["answer_list_hash"] = hash_str(filter_answer_set_dict[req_msgs[0]], "answer")
        transaction_structure["rating_list"] = rating_veh_dict[req_msgs[0]]
        trans_time = transaction_time(hash_answer_msg, rating_veh_dict[req_msgs[0]])
        trans_dict[trans_time].append(copy.deepcopy(transaction_structure))
    return trans_dict


def transaction_time(hash_answer_msg, rating_for_sending_list):
    answer_time = 0
    for rating_msg in rating_for_sending_list:
        answer_msg = hash_answer_msg[rating_msg[1]]
        if answer_msg[7] > answer_time:
            answer_time = answer_msg[7]
    return answer_time


def consensus_simulator(transactions_dict, bl_operation, threshold_op=THRESHOLD_OPERATION):
    waiting_blockchain_status_dict = defaultdict(dict)
    writed_blockchain_status_dict = defaultdict(list)
    #
    for time_trans, trans_list in transactions_dict.items():
        for trans in trans_list:
            tmp_write_dict = {}
            trans_hash = hash_str(trans, "transaction")
            tmp_write_dict["write_time"] = time_trans
            tmp_write_dict["verify_list"] = []
            waiting_blockchain_status_dict[trans_hash] = copy.deepcopy(tmp_write_dict)
    sorted_transactions_dict = sorted(transactions_dict.items(), key=lambda x: x[0])
    for time_trans1, trans_list1 in sorted_transactions_dict.items():
        for trans3 in trans_list1:
            # 字典（可能其他结构也类似）在迭代的时候不能删除里面的元素
            for trans_hash2, trans_record_detail_dict in waiting_blockchain_status_dict.items():
                if trans_record_detail_dict["write_time"] < time_trans1:
                    trans_record_detail_dict["verify_list"].append([time_trans1, trans3])
                    sum_operations = consensus_simulator_verify_count(trans_record_detail_dict["verify_list"], bl_operation)
                    if sum_operations > threshold_op:
                        writed_blockchain_status_dict[trans_hash2] = [time_trans1, waiting_blockchain_status_dict.pop(trans_hash2)]
    return writed_blockchain_status_dict


# 计算验DAG的某一个事务证列表内的事务的操作总和
def consensus_simulator_verify_count(verify_list, bl_operation):
    bl_operation_keys_list = list(bl_operation.keys())
    sorted(bl_operation_keys_list)
    sum_operation = 0
    for records in verify_list:
        if bl_operation_keys_list[-1] < records[0]:
            request_id = records[1]["request_msg"][0]
            sum_operation += bl_operation[bl_operation_keys_list[-1]][request_id]
        else:
            raise Exception("bl_operation的最终时间大于当前事务的发起时间，检查consensus_simulator_verify_count")
    return sum_operation


def consensus_v1(false_list, message_disturb_func, probability_count_fuc, bayes_infer_func, trickers, round_time=ROUNDS):
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
    request_msg_list = request_generator(veh_ids, event_list, veh_address_dict, veh_trajectory_dict, round_time)
    # //向仿真参数里写入请求消息
    cache_request_status = status_request_cache(cache_request_veh_dict, request_msg_list, hash_request_msg)
    # //产生响应消息
    recv_msg_dict = answer_generator(request_msg_list, vail_veh, veh_address_dict)
    # //以反馈地址将反馈信息进行整理，第二个返回值根据请求的时间要求筛选出可用的反馈消息
    clean_msg_v1_dict, clean_valid_msg_v1_dict = message_cleaning(recv_msg_dict)
    # //从筛选后的反馈消息中只随机挑出来一条
    res_valid_for_req_list = message_filter(clean_valid_msg_v1_dict)
    # //存储仿真结果
    res_rate_dict = defaultdict(float)

    # //初始化响应、评分字典
    hash_answer_msg = hash_answer_msg_init()
    hash_rate_msg = hash_rate_msg_init()

    _false_ratio = 0.1
    # //根据false_ratio改变其中一些消息的内容，组成假消息,并向缓存写入响应消息
    res_disturb_for_req_list = message_disturb_func(res_valid_for_req_list, _false_ratio, hash_answer_msg, trickers)
    # res_disturb_for_req_list = message_disturb(res_valid_for_req_list, _false_ratio, hash_answer_msg)
    # //每一秒车辆的位置
    veh_location_all_dict = veh_location_every_round(veh_location, speed_init_veh_dict, round_time)
    # //每一个响应对应的相关车辆集
    veh_reference_set_all_dict = veh_reference_collect(res_disturb_for_req_list, veh_location_all_dict)
    # //将相关集维持在[0,10]范围内，键是请求车辆，值是得到的响应列表
    filter_answer_set_dict = answer_filter(res_disturb_for_req_list)
    # //给相关集内的车辆分配响应，键是请求车辆，值是对响应的评分
    rating_veh_dict = rating_collect(filter_answer_set_dict, probability_count_fuc, bayes_infer_func, bl_operation)
    # //【仿真2】共识协议
    transactions_dict = transaction_pack(request_msg_list, filter_answer_set_dict, rating_veh_dict, hash_answer_msg)
    # // 一个事务被最终写入区块链或者状态“不可变”的时间，或者叫以很大概率保持确定性的时间
    mean_time_consume = consensus_simulator(transactions_dict, bl_operation)

    return res_rate_dict


if __name__ == '__main__':
    # 事务广播出去，然后不论谁在发起事务的时候需要将这些结果打包确认
    # 需要一个随机游走角色，负责检查各个
    # false_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    false_list = np.arange(0, 1.05, 0.05)
    # ==================================================================
    # out_dict = traditional_v3(false_list, ROUNDS)
    # ==================================================================
    message_disturb_func = message_disturb
    probability_func = probability_count_fuc2
    bayer_func = bayes_infer_v2
    trick = 60
    average_dict = defaultdict(list)
    for i in range(50):
        print("[round:{}] ".format(i))
        res_dict = consensus_v1(false_list, message_disturb_func, probability_func, bayer_func, trick, ROUNDS)
        for ratios, num in res_dict.items():
            average_dict[ratios].append(num)
    out_dict = defaultdict(int)
    for ratios1, num_list in average_dict.items():
        out_dict[ratios1] = mean_for_list(num_list)
    # ================================================================

    false_msg_ratio_json = json.dumps(out_dict)
    fn1 = "{}{}_{}_{}.txt".format("output/", message_disturb_func.__name__, probability_func.__name__, PE)
    a = open(fn1, "w", encoding='UTF-8')
    a.write(false_msg_ratio_json)
    a.close()

    # res_offset_dict = collect_offset(false_list)
    # res_offset_dict_json = json.dumps(res_offset_dict)
    # b = open(r"output/second_picture.txt", "w", encoding='UTF-8')
    # b.write(res_offset_dict_json)
    # b.close()
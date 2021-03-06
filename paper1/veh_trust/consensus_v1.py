# from paper1.veh_trust.trust_v3 import *
from paper1.veh_trust.trust_v4 import *
from paper1.veh_trust.init_fun import *
from paper1.veh_trust.probability_count import *


def request_generator(veh_ids, event_list, veh_address_dict, veh_trajectory_dict, round_time):
    # 设置请求消息时间
    sending_msg_list = []
    trans_num_list = transaction_emerge_generator(POISSON_MEAN, round_time)
    for index_id, msg_nums in enumerate(trans_num_list):
        if msg_nums > 0:
            # tmp_sending_veh_list = random.sample(veh_ids, msg_nums)
            for tmp_sending_veh1 in range(msg_nums):
                tmp_sending_veh = random.choice(veh_ids)
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
    count_transaction_num = 0
    for req_msgs in tmp_msg_list:
        transaction_structure = defaultdict(dict)
        transaction_structure["request_msg"] = req_msgs
        transaction_structure["request_hash"] = hash_str(req_msgs, "request")
        transaction_structure["answer_list"] = filter_answer_set_dict[req_msgs[0]]
        transaction_structure["answer_list_hash"] = hash_str(filter_answer_set_dict[req_msgs[0]], "answer")
        transaction_structure["rating_list"] = rating_veh_dict[req_msgs[0]]
        trans_time = transaction_time(hash_answer_msg, rating_veh_dict[req_msgs[0]])
        trans_dict[trans_time].append(copy.deepcopy(transaction_structure))
        count_transaction_num += 1
    print("{}{}".format("transaction num: ", count_transaction_num))
    return trans_dict


# transaction的时间定义为其所包含的所有响应里面最大的时间
def transaction_time(hash_answer_msg, rating_for_sending_list):
    answer_time = 0
    for rating_msg in rating_for_sending_list:
        answer_msg = hash_answer_msg[rating_msg[1]]
        if answer_msg[7] > answer_time:
            answer_time = answer_msg[7]
    return answer_time


def ex_flat_sorted_transactions(issue_time_trans, flat_sorted_transactions_list):
    # 必须是排好序的transaction列表
    tmp_trans_list = []
    for tmp_issue_time_trans in flat_sorted_transactions_list:
        if tmp_issue_time_trans[0] < issue_time_trans[0]:
            tmp_trans_list.append(tmp_issue_time_trans)
        else:
            break
    return tmp_trans_list


def consensus_simulator(transactions_dict, bl_operation, threshold_op=THRESHOLD_OPERATION):
    waiting_blockchain_status_dict = defaultdict(dict)
    writed_blockchain_status_dict = defaultdict(list)
    # // 对输入的trans按时间进行排序，主要是为了后面计算方便
    sorted_transactions_list = sorted(transactions_dict.items(), key=lambda x: x[0])
    flat_sorted_transactions_list = flat_transaction(sorted_transactions_list)
    # // 构造等待缓存
    for issue_time_trans_ in flat_sorted_transactions_list:
        tmp_write_dict = {}
        trans_hash = issue_time_trans_[1]
        tmp_write_dict["write_time"] = issue_time_trans_[0]
        tmp_write_dict["front_list"] = []
        tmp_write_dict["behind_list"] = []
        waiting_blockchain_status_dict[trans_hash] = copy.deepcopy(tmp_write_dict)

    # //开始迭代列表内的所有事务，此刻time_trans表示要发布的trans
    for issue_time_trans in flat_sorted_transactions_list:
        tmp_waiting_trans_list = []
        time_trans2_list = ex_flat_sorted_transactions(issue_time_trans, flat_sorted_transactions_list)
        if time_trans2_list:
            for time_trans2 in time_trans2_list:
                len_front_list = len(waiting_blockchain_status_dict[issue_time_trans[1]]["front_list"])
                tmp_behind_list = waiting_blockchain_status_dict[time_trans2[1]]["behind_list"]

                if len(tmp_behind_list) > 0:
                    behind_count_score = 0
                    for time_trans3 in tmp_behind_list:
                        behind_count_score += time_trans3[2]['trust_score']
                    # //判断这个trans的后向列表内的信誉值是不是超了，如果超了就放到writed里面，且不做操作
                    if behind_count_score > THRESHOLD_OPERATION:
                        waiting_blockchain_status_dict[time_trans2[1]]['behind_count_score'] = behind_count_score
                        writed_blockchain_status_dict[time_trans2[1]] = waiting_blockchain_status_dict[time_trans2[1]]
                        tmp_waiting_trans_list.append(time_trans2)
                        continue
                    else:
                        if len_front_list < VERIFY_NUM:
                            waiting_blockchain_status_dict[issue_time_trans[1]]['front_list'].append(time_trans2)
                            waiting_blockchain_status_dict[time_trans2[1]]["behind_list"].append(issue_time_trans)
                else:
                    tmp_behind_list.append(issue_time_trans)
                    if len_front_list < VERIFY_NUM:
                        waiting_blockchain_status_dict[issue_time_trans[1]]['front_list'].append(time_trans2)
        if not time_trans2_list:
            continue
        elif len(tmp_waiting_trans_list) == len(time_trans2_list):
            tag_time = 0
            tmp_trans = 0
            for trans5 in time_trans2_list:
                if trans5[0] > tag_time:
                    tag_time = trans5[0]
                    tmp_trans = trans5
            if tmp_trans == 0:
                tmp_trans1 = random.choice(time_trans2_list)
                waiting_blockchain_status_dict[tmp_trans1[1]]["behind_list"].append(issue_time_trans)
                waiting_blockchain_status_dict[issue_time_trans[1]]['front_list'].append(tmp_trans1)
            else:
                waiting_blockchain_status_dict[tmp_trans[1]]["behind_list"].append(issue_time_trans)
                waiting_blockchain_status_dict[issue_time_trans[1]]['front_list'].append(tmp_trans)

    return writed_blockchain_status_dict


def flat_transaction(sorted_transactions_list):
    tmp_sorted_list = []
    for trans_list in sorted_transactions_list:
        for trans in trans_list[1]:
            trans["trust_score"] = random.randint(1, 100)
            tmp_sorted_list.append([trans_list[0], hash_str(trans, "transaction"), trans])
    return tmp_sorted_list


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
    # bl_balance = bl_balance_init(bl_address_ids)
    # //钱包网络参与初始化（仿真）
    bl_operation = bl_operation_init(bl_address_ids)
    # //所有车辆节点的请求和响应缓存区初始化（仿真）
    # cache_request_veh_dict, cache_answer_veh_dict, cache_rating_veh_dict = cache_all_veh_init(veh_ids)
    # //初始化全局请求字典，键是请求消息的hash值，值是消息本身
    # hash_request_msg = hash_request_msg_init()

    # //得到所有车辆与每一个事件之间的距离
    veh_trajectory_dict = veh_trajectory_fuc1(veh_location, speed_init_veh_dict, round_time)
    adjacency_dict = veh_adjacency_fuc(event_list, veh_trajectory_dict)
    #     //每个事件的有效可观测车辆集合vail_veh
    vail_veh = veh_valid_fun(adjacency_dict)

    # // 设置请求车辆
    # send_request_veh_id_list = random.sample(veh_ids, NUM_REQUEST_VEH)
    request_msg_list = request_generator(veh_ids, event_list, veh_address_dict, veh_trajectory_dict, round_time)
    print("{}{}".format("request message: ", len(request_msg_list)))
    # //向仿真参数里写入请求消息
    # cache_request_status = status_request_cache(cache_request_veh_dict, request_msg_list, hash_request_msg)
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
    # hash_rate_msg = hash_rate_msg_init()

    _false_ratio = 0.1
    # //根据false_ratio改变其中一些消息的内容，组成假消息,并向缓存写入响应消息
    res_disturb_for_req_list = message_disturb_func(res_valid_for_req_list, _false_ratio, hash_answer_msg, trickers)
    print("{}{}".format("answer message: ", len(res_disturb_for_req_list)))
    # //每一秒车辆的位置
    # veh_location_all_dict = veh_location_every_round(veh_location, speed_init_veh_dict, round_time)
    # //每一个响应对应的相关车辆集
    # veh_reference_set_all_dict = veh_reference_collect(res_disturb_for_req_list, veh_location_all_dict)
    # //将相关集维持在[0,10]范围内，键是请求车辆，值是得到的响应列表
    filter_answer_set_dict = answer_filter(res_disturb_for_req_list)
    # //给相关集内的车辆分配响应，键是请求车辆，值是对响应的评分
    rating_veh_dict = rating_collect(filter_answer_set_dict, probability_count_fuc, bayes_infer_func, bl_operation)
    # //【仿真2】共识协议
    transactions_dict = transaction_pack(request_msg_list, filter_answer_set_dict, rating_veh_dict, hash_answer_msg)
    transaction_save(transactions_dict)
    # transaction_save(transactions_dict)
    # // 一个事务被最终写入区块链或者状态“不可变”的时间，或者叫以很大概率保持确定性的时间
    # mean_time_consume = consensus_simulator(transactions_dict, bl_operation)

    return res_rate_dict


def transaction_save(transactions_dict):
    fn2 = "{}{}_{}_{}.json".format("transactions/", "Transaction", POISSON_MEAN, time.strftime("%m%d_%H-%M", time.localtime()))
    a1 = open(fn2, "w", encoding='utf-8')
    json.dump(transactions_dict, a1, ensure_ascii=False)
    a1.close()


def transaction_read(fn3):
    handler = open(fn3, 'r', encoding='utf-8')
    _dict = json.load(handler)
    b = defaultdict(dict)
    for _keys in _dict.keys():
        b[int(_keys)] = _dict[_keys]
    return b


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
    # for i in range(2):
    #     print("[round:{}] ".format(i))
    #     res_dict = consensus_v1(false_list, message_disturb_func, probability_func, bayer_func, trick, ROUNDS)
    res_dict = consensus_v1(false_list, message_disturb_func, probability_func, bayer_func, trick, ROUNDS)
    #     for ratios, num in res_dict.items():
    #         average_dict[ratios].append(num)
    # out_dict = defaultdict(int)
    # for ratios1, num_list in average_dict.items():
    #     out_dict[ratios1] = mean_for_list(num_list)
    # ================================================================

    # false_msg_ratio_json = json.dumps(out_dict)
    # fn1 = "{}{}_{}_{}.txt".format("output/", message_disturb_func.__name__, probability_func.__name__, PE)
    # a = open(fn1, "w", encoding='UTF-8')
    # a.write(false_msg_ratio_json)
    # a.close()

    # res_offset_dict = collect_offset(false_list)
    # res_offset_dict_json = json.dumps(res_offset_dict)
    # b = open(r"output/second_picture.txt", "w", encoding='UTF-8')
    # b.write(res_offset_dict_json)
    # b.close()
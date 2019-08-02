from test_script.veh_trust.consensus_v1 import *
import os


def bl_address_read(file_address=BLOCKCHAIN_ADDRESS_FILE):
    bl_address_id_list = []
    with open(file_address, 'r') as handler:
        for line in handler:
            line = line.strip('\n').split(';')
            bl_address_id_list.append(line[0])
    return bl_address_id_list


def writed_consume_save(mean_time_consume):
    fn2 = "{}{}_{}.json".format("dag_result/", "dag", time.strftime("%m%d_%H-%M", time.localtime()))
    a1 = open(fn2, "w", encoding='utf-8')
    json.dump(mean_time_consume, a1, ensure_ascii=False)
    a1.close()


def writed_consume_read(fn4):
    handler = open(fn4, 'r', encoding='utf-8')
    _dict = json.load(handler)
    # b = defaultdict(dict)
    # for _keys in _dict.keys():
    #     b[int(_keys)] = _dict[_keys]
    return _dict


def count_mean_time(time_dict):
    mean_dict = defaultdict(float)
    for mean_trans_num, time_dict2 in time_dict.items():
        _num = 0
        _sum = 0
        for time_num, time_list in time_dict2.items():
            for i in time_list:
                _num += 1
                _sum += i
        _mean_time = _sum / _num
        mean_dict[mean_trans_num] = _mean_time
    return mean_dict


def consensus_simulator_v2(transactions_dict, bl_operation, threshold_op=THRESHOLD_OPERATION):
    waiting_blockchain_status_dict = defaultdict(dict)
    writed_blockchain_status_dict = defaultdict(dict)
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

    # 可能要改成数据库，如果前面没有足够的事务，一轮迭代会有事务的前置事务不足2个
    for issue_time_trans in flat_sorted_transactions_list:
        tmp_waiting_trans_list = []
        time_trans2_list = ex_flat_sorted_transactions(issue_time_trans, flat_sorted_transactions_list)
        if len(time_trans2_list) > 2:
            time_trans2_list = random.sample(time_trans2_list, 2)
            for time_trans2 in time_trans2_list:
                waiting_blockchain_status_dict[issue_time_trans[1]]['front_list'].append(time_trans2)
                waiting_blockchain_status_dict[time_trans2[1]]["behind_list"].append(issue_time_trans)

    for trans_hash1, trans_chain in waiting_blockchain_status_dict.items():
        sum_behind_trust = 0
        tmp_writed_dict = {}
        tmp_writed_dict["write_time"] = trans_chain["write_time"]
        tmp_writed_dict["front_list"] = trans_chain["front_list"]
        tmp_writed_dict["behind_list"] = []
        for trans2 in trans_chain["behind_list"]:
            sum_behind_trust += trans2[2]["trust_score"]
            tmp_writed_dict["behind_list"].append(trans2)
            if sum_behind_trust > threshold_op:
                tmp_writed_dict['behind_count_score'] = sum_behind_trust
                writed_blockchain_status_dict[trans_hash1] = copy.deepcopy(tmp_writed_dict)
                break

    return writed_blockchain_status_dict


def consensus_v2():
    # //地址钱包初始化
    bl_address_ids = bl_address_read()
    # //钱包网络参与初始化（仿真）
    bl_operation = bl_operation_init(bl_address_ids)
    file_list = os.listdir("transactions")
    time_dict = defaultdict(list)
    for file_name in file_list:
        path_file_name = "transactions/{}".format(file_name)
        transactions_dict = transaction_read(path_file_name)
        # transactions_dict = transaction_read("transactions/Transaction_100_0624_15-24.json")
        split_list = file_name.split("_")
        # // 一个事务被最终写入区块链或者状态“不可变”的时间，或者叫以很大概率保持确定性的时间
        # mean_time_consume = consensus_simulator_v2(transactions_dict, bl_operation)
        mean_time_consume = consensus_simulator(transactions_dict, bl_operation)
        # writed_consume_save(mean_time_consume)

        time_interval = defaultdict(list)
        for tran_hash, writed_tran in mean_time_consume.items():
            if writed_tran["front_list"]:
                tmp_time_interval_num = 0
                for trans6 in writed_tran["behind_list"]:
                    if (trans6[0] - writed_tran["write_time"]) > tmp_time_interval_num:
                        tmp_time_interval_num = trans6[0] - writed_tran["write_time"]
                time_interval[writed_tran["write_time"]].append(tmp_time_interval_num)
        time_dict[int(split_list[1])] = copy.deepcopy(time_interval)
    mean_dict = count_mean_time(time_dict)
    pass


def consensus_test_v2():
    # //地址钱包初始化
    bl_address_ids = bl_address_read()
    # //钱包网络参与初始化（仿真）
    bl_operation = bl_operation_init(bl_address_ids)

    time_dict = defaultdict(list)

    file_name = "Transaction_100_0624_10-20.json"
    path_file_name = "transactions/{}".format(file_name)

    transactions_dict = transaction_read(path_file_name)
    split_list = file_name.split("_")
    # // 一个事务被最终写入区块链或者状态“不可变”的时间，或者叫以很大概率保持确定性的时间
    mean_time_consume = consensus_simulator_v2(transactions_dict, bl_operation)
    # writed_consume_save(mean_time_consume)

    time_interval = defaultdict(list)
    for tran_hash, writed_tran in mean_time_consume.items():
        if writed_tran["front_list"]:
            tmp_time_interval_num = 0
            for trans6 in writed_tran["behind_list"]:
                if (trans6[0] - writed_tran["write_time"]) > tmp_time_interval_num:
                    tmp_time_interval_num = trans6[0] - writed_tran["write_time"]
            time_interval[writed_tran["write_time"]].append(tmp_time_interval_num)
    time_dict[int(split_list[1])] = copy.deepcopy(time_interval)
    mean_dict = count_mean_time(time_dict)
    pass


if __name__ == '__main__':
    consensus_v2()
    # consensus_test_v2()
    # mean_result_dict = writed_consume_read("dag_result/dag_0621_16-14.json")
    # time_interval = defaultdict(list)
    # for tran_hash, writed_tran in mean_result_dict.items():
    #     if writed_tran["front_list"]:
    #         tmp_time_interval_num = 0
    #         for trans6 in writed_tran["behind_list"]:
    #             if (trans6[0] - writed_tran["write_time"]) > tmp_time_interval_num:
    #                 tmp_time_interval_num = trans6[0] - writed_tran["write_time"]
    #         time_interval[writed_tran["write_time"]].append(tmp_time_interval_num)

    pass
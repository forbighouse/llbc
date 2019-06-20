from test_script.veh_trust.consensus_v1 import *


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


def consensus_v2():
    # //地址钱包初始化
    bl_address_ids = bl_address_read()
    # //钱包网络参与初始化（仿真）
    bl_operation = bl_operation_init(bl_address_ids)
    transactions_dict = transaction_read("transactions/Transaction_0619_08-33.json")

    # // 一个事务被最终写入区块链或者状态“不可变”的时间，或者叫以很大概率保持确定性的时间
    mean_time_consume = consensus_simulator(transactions_dict, bl_operation)
    # writed_consume_save(mean_time_consume)


if __name__ == '__main__':
    # consensus_v2()
    mean_result_dict = writed_consume_read("dag_result/dag_0620_16-59.json")
    time_interval = defaultdict(list)
    for tran_hash, writed_tran in mean_result_dict.items():
        if writed_tran["front_list"]:
            tmp_time_interval_num = 0
            for trans6 in writed_tran["behind_list"]:
                if (trans6[0] - writed_tran["write_time"]) > tmp_time_interval_num:
                    tmp_time_interval_num = trans6[0] - writed_tran["write_time"]
            time_interval[writed_tran["write_time"]].append(tmp_time_interval_num)



    pass
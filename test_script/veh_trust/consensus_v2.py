from test_script.veh_trust.consensus_v1 import *


def consensus_simulator(transactions_dict, bl_operation, threshold_op=THRESHOLD_OPERATION):
    waiting_blockchain_status_dict = defaultdict(dict)
    writed_blockchain_status_dict = defaultdict(list)
    # // 对输入的trans按时间进行排序，主要是为了后面计算方便
    sorted_transactions_list = sorted(transactions_dict.items(), key=lambda x: x[0])
    flat_sorted_transactions_list = flat_transaction(sorted_transactions_list)
    # // 构造等待缓存
    for issue_time_trans in flat_sorted_transactions_list:
        tmp_write_dict = {}
        trans_hash = issue_time_trans[1]
        tmp_write_dict["write_time"] = issue_time_trans[0]
        tmp_write_dict["front_list"] = []
        tmp_write_dict["behind_list"] = []
        waiting_blockchain_status_dict[trans_hash] = copy.deepcopy(tmp_write_dict)

    # //开始迭代列表内的所有事务，此刻time_trans表示要发布的trans
    for i, issue_time_trans in enumerate(flat_sorted_transactions_list):
        tmp_waiting_trans_list = []
        # //从头往后找，只要时间比time_trans的要早，都要进行计算
        # //条件1：判断issue_trans的front里面的trans的个数，如果超过预定义就不能再往里加了
        len_front_list = len(waiting_blockchain_status_dict[issue_time_trans[1]]["front_list"])
        # //待添加前向节点列表
        time_trans2_list = flat_sorted_transactions_list[0:i]
        # //条件2：判断time_trans2的behind里面的trans所涉及的发起request的车辆的信誉，如果达到预定义，就不能再选了

        if time_trans2_list:
            for time_trans2 in time_trans2_list:
                tmp_behind_list = waiting_blockchain_status_dict[time_trans2[1]]["behind_list"]
                if len(tmp_behind_list) > 0:
                    behind_count_score = 0
                    for time_trans3 in tmp_behind_list:
                        behind_count_score += time_trans3[2]['trust_score']

                    if behind_count_score > THRESHOLD_OPERATION:
                        waiting_blockchain_status_dict[time_trans2[1]]['behind_count_score'] = behind_count_score
                        writed_blockchain_status_dict[time_trans2[1]] = copy.deepcopy(waiting_blockchain_status_dict[time_trans2[1]])
                        continue
                    else:
                        waiting_blockchain_status_dict[time_trans2[1]]["behind_list"].append(issue_time_trans)
                        waiting_blockchain_status_dict[issue_time_trans[1]]['front_list'].append(time_trans2)
                else:
                    tmp_behind_list.append(issue_time_trans)

    return writed_blockchain_status_dict


def bl_address_read(file_address=BLOCKCHAIN_ADDRESS_FILE):
    bl_address_id_list = []
    with open(file_address, 'r') as handler:
        for line in handler:
            line = line.strip('\n').split(';')
            bl_address_id_list.append(line[0])
    return bl_address_id_list


def consensus_v2():
    # //地址钱包初始化
    bl_address_ids = bl_address_read()
    # //钱包网络参与初始化（仿真）
    bl_operation = bl_operation_init(bl_address_ids)
    transactions_dict = transaction_read("transactions/Transaction_0617_16-56.json")

    # // 一个事务被最终写入区块链或者状态“不可变”的时间，或者叫以很大概率保持确定性的时间
    mean_time_consume = consensus_simulator(transactions_dict, bl_operation)


if __name__ == '__main__':
    consensus_v2()

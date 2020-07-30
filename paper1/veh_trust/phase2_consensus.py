from paper1.veh_trust.consensus_v1 import *

def p2_consensus(path_file_name):
    # 读入仿真车辆的id，300地址代替50辆车
    transactions_dict = transaction_read(path_file_name)
    sorted_transactions_list = sorted(transactions_dict.items(), key=lambda x: x[0])
    flat_sorted_transactions_list = flat_transaction(sorted_transactions_list)
    waiting_blockchain_status_dict = defaultdict(dict)
    for _time_trans_ in flat_sorted_transactions_list:
        tmp_write_dict = {}
        trans_hash = _time_trans_[1]
        tmp_write_dict["write_time"] = _time_trans_[0]
        tmp_write_dict["front_list"] = []

        waiting_blockchain_status_dict[trans_hash] = copy.deepcopy(tmp_write_dict)

    for _time_trans2 in flat_sorted_transactions_list:
        time_trans2_list = ex_flat_sorted_transactions(_time_trans2, flat_sorted_transactions_list)
        if len(time_trans2_list) > 2:
            time_trans2_list = random.sample(time_trans2_list, 2)
            for time_trans2 in time_trans2_list:
                waiting_blockchain_status_dict[_time_trans2[1]]['front_list'].append(time_trans2)

    writed_blockchain_status_dict = defaultdict(dict)
    for trans_hash1, trans_chain in waiting_blockchain_status_dict.items():
        sum_behind_trust = 0
        tmp_writed_dict = {}   
        tmp_writed_dict["write_time"] = trans_chain["write_time"]
        tmp_writed_dict["front_list"] = trans_chain["front_list"]
        for store_txn, chain_content in  waiting_blockchain_status_dict.items():
            behind_count_score = 0
            if chain_content['write_time'] > trans_chain['write_time']:
                if trans_hash1 in chain_content['front_list']:
                    behind_count_score += time_trans3[2]['trust_score']

        for trans2 in trans_chain["behind_list"]:
            sum_behind_trust += trans2[2]["trust_score"]
            tmp_writed_dict["behind_list"].append(trans2)
            if sum_behind_trust > threshold_op:
                tmp_writed_dict['behind_count_score'] = sum_behind_trust
                writed_blockchain_status_dict[trans_hash1] = copy.deepcopy(tmp_writed_dict)
                break

    pass

if __name__ == "__main__":
    file_name = "Transaction_100_0624_10-20.json"
    path_file_name = "transactions/{}".format(file_name)
    p2_consensus(path_file_name)

    pass
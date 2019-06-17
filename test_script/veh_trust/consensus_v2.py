from test_script.veh_trust.consensus_v1 import *


def consensus_v2():
    # //地址钱包初始化
    bl_address_ids = bl_address_read()
    # //钱包网络参与初始化（仿真）
    bl_operation = bl_operation_init(bl_address_ids)
    transactions_dict = transaction_read("transactions/Transaction_0617_23-01.json")

    # // 一个事务被最终写入区块链或者状态“不可变”的时间，或者叫以很大概率保持确定性的时间
    mean_time_consume = consensus_simulator(transactions_dict, bl_operation)


if __name__ == '__main__':
    consensus_v2()

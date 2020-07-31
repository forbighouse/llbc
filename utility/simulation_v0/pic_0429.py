import json
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
from matplotlib.ticker import MultipleLocator, FuncFormatter
import math


import seaborn as sns

# http://liyangbit.com/pythonvisualization/matplotlib-top-50-visualizations/

distance_json_path07 = 'distance_data_statistics07.json'
distance_json_path04 = 'distance_data_statistics04.json'
distance_json_path02 = 'distance_data_statistics02.json'
ditribution_json_path07 = 'picklocation_data_statistics07.json'
ditribution_json_path04 = 'picklocation_data_statistics04.json'
ditribution_json_path02 = 'picklocation_data_statistics02.json'


def read_from_json(input_dict):
    b = open(input_dict, "r", encoding='UTF-8')
    out = b.read()
    out = json.loads(out)
    c_dict = dict(out)
    return c_dict


def sum_list(inpurt_list):
    # 求列表的累积和
    sum_ = 0
    for k, l in inpurt_list.items():
        sum_ += l
    return sum_


def get_std(input_list):
    return round(np.std(input_list), 2)


def hours_and_vehicle_numbers_func(input_dict):
    # input_dict: 从文件读进来的一个key是小时，value是每个区的车辆的数目的列表
    # output:
    #       hours_list: “小时”的列表，排序好的
    #       vehicle_numbers_list: “小时”对应的车的数量
    #       list_std_vehicle_per_hour: “车的平均差”

    c_dict = read_from_json(input_dict)
    numbers_per_hours_list = []
    hours_list = []
    for i in c_dict.keys():
        hours_list.append(int(i))

    hours_list = [k for k in sorted(hours_list)]
    list_std_vehicle_per_hour = []
    for hours in hours_list:
        sum_ = sum_list(c_dict[str(hours)])
        numbers_per_hours_list.append(round(sum_/10000, 1))

        list_vehicle = list(c_dict[str(hours)].values())
        list_std_vehicle_per_hour.append(get_std(list_vehicle))

    return hours_list, numbers_per_hours_list, list_std_vehicle_per_hour


def hours_and_transactions_func(input_dict):
    # input_dict: 从文件读进来的，key是小时，value是每个区内的里程数
    # Output:
    #       hours_list: “小时”
    #       tansactions_numbers_list: “事务的数量”

    c1_dict = read_from_json(input_dict)

    numbers_per_hours_list = []
    hours_list = []
    for i in c1_dict.keys():
        hours_list.append(int(i))
    hours_list = [k for k in sorted(hours_list)]

    list_miles_per_hour = []
    list_std_per_hour = []
    for i in hours_list:
        int_sum_miles_per_hour = 0
        for region_id, miles_float in c1_dict[str(i)].items():
            int_sum_miles_per_hour += miles_float
        list_miles_per_hour.append(int_sum_miles_per_hour)
        list_miles = list(c1_dict[str(i)].values())
        list_std_per_hour.append(get_std(list_miles))

    return hours_list, list_miles_per_hour, list_std_per_hour


def vehicle_number_pic_func():

    hours_07_list,  vehicle_numbers_07_list, list_std_per_hours_07 = hours_and_vehicle_numbers_func(ditribution_json_path07)
    hours_04_list,  vehicle_numbers_04_list, list_std_per_hours_04 = hours_and_vehicle_numbers_func(ditribution_json_path04)
    hours_02_list,  vehicle_numbers_02_list, list_std_per_hours_02 = hours_and_vehicle_numbers_func(ditribution_json_path02)

    _, transactions_numbers_07_list, _ = hours_and_transactions_func(distance_json_path07)
    _, transactions_numbers_04_list, _ = hours_and_transactions_func(distance_json_path04)
    _, transactions_numbers_02_list, _ = hours_and_transactions_func(distance_json_path02)

    int_07_sum_miles = 0
    for i in transactions_numbers_07_list:
        int_07_sum_miles += i
    int_04_sum_miles = 0
    for j in transactions_numbers_04_list:
        int_04_sum_miles += j
    int_02_sum_miles = 0
    for k in transactions_numbers_02_list:
        int_02_sum_miles += k

    print("07 transaction = ", int_07_sum_miles)
    print("04 transaction = ", int_04_sum_miles)
    print("02 transaction = ", int_02_sum_miles)

    newlinewidth = 1.5
    fig, ax = plt.subplots(1, 3, figsize=(24, 8), sharey='row', sharex='col', dpi=300)
    ax[0].bar(hours_02_list, vehicle_numbers_02_list, label="01-02 ", color='tab:blue', alpha=.3)
    ax[1].bar(hours_04_list, vehicle_numbers_04_list, label="01-04 ", color='tab:blue', alpha=.3)
    ax[2].bar(hours_07_list, vehicle_numbers_07_list, label="01-07 ", color='tab:blue', alpha=.3)
    ax1_2 = ax[0].twinx()  # instantiate a second axes that shares the same x-axis
    ax2_2 = ax[1].twinx()  # instantiate a second axes that shares the same x-axis
    ax3_2 = ax[2].twinx()  # instantiate a second axes that shares the same x-axis
    ax1_2.plot(hours_02_list, list_std_per_hours_02, label="01-02 ", color='tab:red', linewidth=4)
    ax2_2.plot(hours_02_list, list_std_per_hours_04, label="01-04 ", color='tab:red', linewidth=4)
    ax3_2.plot(hours_02_list, list_std_per_hours_07, label="01-02 ", color='tab:red', linewidth=4)
    ax1_2.hlines(163.73, -0.5, 24, colors='0.5', linewidth=newlinewidth*2, linestyles="dashed")
    ax1_2.hlines(11.3, -0.5, 24, colors='0.5', linewidth=newlinewidth*2, linestyles="dashed")
    ax2_2.hlines(183.12, -0.5, 24, colors='0.5', linewidth=newlinewidth*2, linestyles="dashed")
    ax2_2.hlines(15.86, -0.5, 24, colors='0.5', linewidth=newlinewidth*2, linestyles="dashed")
    ax3_2.hlines(195.7, -0.5, 24, colors='0.5', linewidth=newlinewidth*2, linestyles="dashed")
    ax3_2.hlines(13.1, -0.5, 24, colors='0.5', linewidth=newlinewidth*2, linestyles="dashed")
    # ax[0].set_title("19-01-02")
    # ax[1].set_title("19-01-04")
    # ax[2].set_title("19-01-07")

    y1_newsticks = [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8]
    ax[0].set_xlabel('Hours (Holidays)', fontsize=18)
    ax[1].set_xlabel('Hours (Weekends)', fontsize=18)
    ax[2].set_xlabel('Hours (Weekdays)', fontsize=18)
    ax[0].tick_params(axis='x', rotation=0, labelsize=18)
    ax[1].tick_params(axis='x', rotation=0, labelsize=18)
    ax[2].tick_params(axis='x', rotation=0, labelsize=18)
    ax[0].set_ylabel('Number of vehicles  (${10^4}$)', color='tab:blue', fontsize=18)
    ax[0].tick_params(axis='y', labelcolor='tab:blue', labelsize=18)
    ax[0].set_yticks(y1_newsticks)
    ax[1].set_yticks(y1_newsticks)
    ax[2].set_yticks(y1_newsticks)
    ax[0].tick_params(axis='y', rotation=0, labelcolor='tab:blue')
    ax[0].grid(alpha=.4)
    ax[1].grid(alpha=.4)
    ax[2].grid(alpha=.4)

    y1_2_newsticks = [11.3, 163.73]
    y2_2_newsticks = [15.86, 183.12]
    y3_2_newsticks = [13.1, 25, 50, 75, 100, 125, 150, 175, 190, 195.7]
    ax3_2.set_ylabel("Standard deviation", color='tab:red', fontsize=18)
    ax1_2.tick_params(axis='y', labelcolor='tab:red', labelsize=18)
    ax2_2.tick_params(axis='y', labelcolor='tab:red', labelsize=18)
    ax3_2.tick_params(axis='y', labelcolor='tab:red', labelsize=18)
    ax1_2.set_yticks(y1_2_newsticks)
    ax2_2.set_yticks(y2_2_newsticks)
    ax3_2.set_yticks(y3_2_newsticks)
    # ax1_2.set_xticklabels(x[::60], rotation=90, fontdict={'fontsize': 10})
    # ax1_2.set_title("Numbers and Mean", fontsize=22)

    ax[0].set_xlim(-0.5, 23.5)
    ax[1].set_xlim(-0.5, 23.5)
    ax[2].set_xlim(-0.5, 23.5)
    ax1_2.set_ylim(0, 200)
    ax2_2.set_ylim(0, 200)
    ax3_2.set_ylim(0, 200)
    fig.tight_layout()


    # plt.legend(loc='upper left', prop={'family': 'Times New Roman', 'size': 12})
    # plt.xlim([0, 100])
    # plt.ylim([0, 1])
    # plt.xlabel("Percentage of false messages", fontdict={'family': 'Times New Roman', 'size': 12})
    # plt.ylabel("Ratio of unfair ratings", fontdict={'family': 'Times New Roman', 'size': 12})
    fig.savefig('(1)vehicle_number.pdf', dpi=300)
    plt.show()


def sort_key_dict(input_time):
    key_list = input_time.keys()
    key_int_list = []
    for i in key_list:
        key_int_list.append(int(i))
    z17 = [(k, input_time[str(k)]) for k in sorted(key_int_list)]
    x17 = []
    y17 = []
    for i in z17:
        x17.append(i[0])
        y17.append(i[1])
    return x17, y17


def sort_key_dict_scle(input_time):
    # 把车的数量按10的4次方缩小
    key_list = input_time.keys()
    key_int_list = []
    for i in key_list:
        key_int_list.append(int(i))
    z17 = [(k, input_time[str(k)]) for k in sorted(key_int_list)]
    x17 = []
    y17 = []
    for i in z17:
        x17.append(i[0])
        y17.append(round(((i[1]*3)), 1))
    return x17, y17


def count_txn_number(input_lst):
    txn_num = 0
    for i in input_lst:
        txn_num += i
    return txn_num


def count_all_trip():
    d07_dict = read_from_json(distance_json_path07)
    d04_dict = read_from_json(distance_json_path04)
    d02_dict = read_from_json(distance_json_path02)

    _sum_1 = 0
    for values in d02_dict.values():
        for values_2 in values.values():
            _sum_1 += int(values_2)

    _sum_2 = 0
    for values in d04_dict.values():
        for values_3 in values.values():
            _sum_2 += int(values_3)

    _sum_3 = 0
    for values in d07_dict.values():
        for values_4 in values.values():
            _sum_3 += int(values_4)

    print(_sum_1)
    print(_sum_2)
    print(_sum_3)


def vehilce_ditribution_pic():

    c07_dict = read_from_json(ditribution_json_path07)
    c04_dict = read_from_json(ditribution_json_path04)
    c02_dict = read_from_json(ditribution_json_path02)

    d07_dict = read_from_json(distance_json_path07)
    d04_dict = read_from_json(distance_json_path04)
    d02_dict = read_from_json(distance_json_path02)



    # 车的请求，求事务
    x7_d_08, y7_d_08 = sort_key_dict_scle(d07_dict['8'])
    x4_d_08, y4_d_08 = sort_key_dict_scle(d04_dict['8'])
    x2_d_08, y2_d_08 = sort_key_dict_scle(d02_dict['8'])
    x7_d_18, y7_d_18 = sort_key_dict_scle(d07_dict['18'])
    x4_d_18, y4_d_18 = sort_key_dict_scle(d04_dict['18'])
    x2_d_18, y2_d_18 = sort_key_dict_scle(d02_dict['18'])

    # 车的数量，求分布
    x7_08, y7_08 = sort_key_dict(c07_dict['8'])
    x4_08, y4_08 = sort_key_dict(c04_dict['8'])
    x2_08, y2_08 = sort_key_dict(c02_dict['8'])
    x7_18, y7_18 = sort_key_dict(c07_dict['18'])
    x4_18, y4_18 = sort_key_dict(c04_dict['18'])
    x2_18, y2_18 = sort_key_dict(c02_dict['18'])

    x7_08 = np.array(x7_08)
    x4_08 = np.array(x4_08)
    x2_08 = np.array(x2_08)
    x7_18 = np.array(x7_18)
    x4_18 = np.array(x4_18)
    x2_18 = np.array(x2_18)

    a08_ = np.intersect1d(x4_08, x2_08)
    a08 = np.intersect1d(x7_08, a08_)
    a18_ = np.intersect1d(x4_18, x2_18)
    a18 = np.intersect1d(x7_18, a18_)

    #
    x08 = a08.tolist()
    x18 = a18.tolist()

    print("7_08:", count_txn_number(y7_d_08))
    print("4_08:", count_txn_number(y4_d_08))
    print("2_08:", count_txn_number(y2_d_08))
    print("7_18:", count_txn_number(y7_d_18))
    print("4_18:", count_txn_number(y4_d_18))
    print("2_18:", count_txn_number(y2_d_18))


    # x17_value_sort_list, y17_value_sort_list = sort_value_dict(clock17, len(clock17.keys()))
    # x7_value_sort_list, y7_value_sort_list = sort_value_dict(clock7, 15)
    # x21_value_sort_list, y21_value_sort_list = sort_value_dict(clock21, 15)

    # plt.bar(list(z1.keys()), list(z1.values()))
    # plt.bar(x0, y0)
    # plt.bar(x17, y17, color='r')

    fig, ax = plt.subplots(2, 1, figsize=(16, 9), dpi=300)
    ax0_2 = ax[0].twinx()
    # 未累积面积图
    ax[0].fill_between(x7_08, y1=y7_08, y2=0, label="Midweek 08 o'clock", alpha=0.3, color='blue')
    ax[0].fill_between(x4_08, y1=y4_08, y2=0, label="Weekend 08 o'clock", alpha=0.3, color='green')
    ax[0].fill_between(x2_08, y1=y2_08, y2=0, label="Holiday 08 o'clock", alpha=0.3, color='red')
    # transaction图
    ax0_2.plot(x7_d_08, y7_d_08, label="Midweek 08 o'clock", linestyle="dashed", color='blue')
    ax0_2.plot(x4_d_08, y4_d_08, label="Weekend 08 o'clock", linestyle="dashed", color='green')
    ax0_2.plot(x2_d_08, y2_d_08, label="Holiday 08 o'clock", linestyle="dashed", color='red')
    ax[0].set_xlabel('zones', fontsize=14)
    ax[0].tick_params(axis='x', rotation=60, labelsize=14)
    ax[0].set_ylabel('Number of vehicles', fontsize=16)
    # ax.set_yticks(y1_newsticks)
    ax[0].grid(alpha=.4)
    ax[0].set_xticks(x08[::3])
    ax[0].legend(loc='upper left', prop={'size': 16}, framealpha=0.5)
    ax0_2.legend(loc='upper right', prop={'size': 16}, framealpha=0.5)
    ax[0].set_ylim(0, 1000)
    ax0_2.set_ylabel("Number of transaction", fontsize=16)


    ax1_2 = ax[1].twinx()
    ax[1].fill_between(x7_18, y1=y7_18, y2=0, label="Midweek 18 o'clock", alpha=0.3, color='blue')
    ax[1].fill_between(x4_18, y1=y4_18, y2=0, label="Weekend 18 o'clock", alpha=0.3, color='green')
    ax[1].fill_between(x2_18, y1=y2_18, y2=0, label="Holiday 18 o'clock", alpha=0.3, color='red')
    # transaction图
    ax1_2.plot(x7_d_18, y7_d_18, label="Midweek 18 o'clock", linestyle="dashed", color='blue')
    ax1_2.plot(x4_d_18, y4_d_18, label="Weekend 18 o'clock", linestyle="dashed", color='green')
    ax1_2.plot(x2_d_18, y2_d_18, label="Holiday 18 o'clock", linestyle="dashed", color='red')
    ax[1].set_xlabel('zones', fontsize=14)
    ax[1].tick_params(axis='x', rotation=60, labelsize=14)
    ax[1].set_ylabel('Number of vehicles', fontsize=16)
    # ax.set_yticks(y1_newsticks)
    ax[1].grid(alpha=.4)
    ax[1].legend(loc='upper left', prop={'size': 16}, framealpha=0.5)
    ax1_2.legend(loc='upper right', prop={'size': 16}, framealpha=0.5)
    ax1_2.set_ylabel("Number of transactions", fontsize=16)
    ax[1].set_ylim(0, 1000)
    ax[1].set_xticks(x18[::3])

    fig.tight_layout()

    # plt.grid(linestyle='-.')
    plt.savefig('(2)transaction distribution.pdf')
    plt.show()


def account_vehicle_number():
    c04 = open(ditribution_json_path04, "r", encoding='UTF-8')
    out04 = c04.read()
    out04 = json.loads(out04)
    c04_dict = dict(out04)

    x4_d_08, y4_d_08 = sort_key_dict_scle(c04_dict['8'])
    account_8_oclock_vehicle = 0
    for i in y4_d_08:
        account_8_oclock_vehicle += i

    x4_d_18, y4_d_18 = sort_key_dict_scle(c04_dict['18'])
    account_18_oclock_vehicle = 0
    for j in y4_d_18:
        account_18_oclock_vehicle += j
    print("04-8 o'clock, Region number = ", len(x4_d_08))
    print("04-8 o'clock, Vehicle number = ", account_8_oclock_vehicle)
    print("04-18 o'clock, Region number = ", len(x4_d_18))
    print("04-18 o'clock, Vehicle number = ", account_18_oclock_vehicle)

    c02 = open(ditribution_json_path02, "r", encoding='UTF-8')
    out02 = c02.read()
    out02 = json.loads(out02)
    c02_dict = dict(out02)

    x2_d_08, y2_d_08 = sort_key_dict_scle(c02_dict['8'])
    account_8_oclock_vehicle = 0
    for i in y2_d_08:
        account_8_oclock_vehicle += i

    x2_d_18, y2_d_18 = sort_key_dict_scle(c02_dict['18'])
    account_18_oclock_vehicle = 0
    for j in y2_d_18:
        account_18_oclock_vehicle += j
    print("02-8 o'clock, Region number = ", len(x2_d_08))
    print("02-8 o'clock, Vehicle number = ", account_8_oclock_vehicle)
    print("02-18 o'clock, Region number = ", len(x2_d_18))
    print("02-18 o'clock, Vehicle number = ", account_18_oclock_vehicle)

    c07 = open(ditribution_json_path07, "r", encoding='UTF-8')
    out07 = c07.read()
    out07 = json.loads(out07)
    c07_dict = dict(out07)

    x7_d_08, y7_d_08 = sort_key_dict_scle(c07_dict['8'])
    account_8_oclock_vehicle = 0
    for i in y2_d_08:
        account_8_oclock_vehicle += i

    x7_d_18, y7_d_18 = sort_key_dict_scle(c07_dict['18'])
    account_18_oclock_vehicle = 0
    for j in y2_d_18:
        account_18_oclock_vehicle += j
    print("07-8 o'clock, Region number = ", len(x7_d_08))
    print("07-8 o'clock, Vehicle number = ", account_8_oclock_vehicle)
    print("07-18 o'clock, Region number = ", len(x7_d_18))
    print("07-18 o'clock, Vehicle number = ", account_18_oclock_vehicle)


def vehicle_to_tps():
    def lines_func(x):
        y = []
        for i in x:
            _res = (0.5686 * i) - 4.3135
            y.append(round(_res))
        return y
    input_vehicle_number = [25, 50, 75, 100, 250, 500, 750, 1000, 3500, 5000, 7500, 10000, 18000]
    input_line_number = np.arange(10, 18000, 10)
    input_line_number = list(input_line_number)
    y_tps = lines_func(input_vehicle_number)
    y_base = lines_func(input_line_number)


    fig, ax = plt.subplots(1, 1, figsize=(16, 6), dpi=300)
    ax.plot(input_line_number, y_base, label="Holiday 08 o'clock", color='red')
    ax.scatter(input_vehicle_number, y_tps, color='red')
    ax.set_ylabel("TPS", fontsize=18)
    ax.set_xlabel("Number of peers", fontsize=18)
    ax.tick_params(axis='y', labelsize=18)
    ax.tick_params(axis='x', labelsize=18)
    # new_yticks = [1, 10, 100, 1000, 10000]
    # ax.set_yticks(new_yticks)
    xminorLocator = MultipleLocator(10)
    ax.xaxis.set_minor_locator(xminorLocator)
    plt.ylim(10, 11000)
    plt.xlim(10, 20000)

    plt.xscale('log')
    plt.yscale('log')
    plt.savefig('(5)TPS increase.pdf')
    plt.show()


if __name__ == "__main__":
    # vehicle_number_pic_func()
    # vehilce_ditribution_pic()
    # vehicle_distribution_one_zone_pic(164)
    # account_vehicle_number()
    vehicle_to_tps()
    # count_all_trip()

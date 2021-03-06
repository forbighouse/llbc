import json
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
from matplotlib.ticker import MultipleLocator
import gc

from scipy import interpolate
from scipy.interpolate import make_interp_spline

def first_pic_func():
    b = open("output/message_disturb_order_probability_count_fuc4_0.5.txt", "r", encoding='UTF-8')
    b2 = open("output/message_disturb_order_probability_count_fuc4_0.1.txt", "r", encoding='UTF-8')

    out = b.read()
    out2 = b2.read()

    out = json.loads(out)
    out2 = json.loads(out2)

    c_dict = dict(out)
    c2_dict = dict(out2)

    x = []
    y = []
    for key, values in c_dict.items():
        x.append(round(float(key), 2)*100)
        y.append(values)

    x2 = []
    y2 = []
    for key, values in c2_dict.items():
        x2.append(round(float(key), 2)*100)
        y2.append(values)

    plt.plot(x2, y2, color='k', linestyle='-', marker='s', label='PE = 0.1')
    plt.plot(x, y, color='r', linestyle='-', marker='o', label='PE = 0.5')

    plt.legend(loc='upper left', prop={'family': 'Times New Roman', 'size': 12})
    plt.xlim([0, 100])
    plt.ylim([0, 1])
    plt.xlabel("Percentage of false messages", fontdict={'family': 'Times New Roman', 'size': 12})
    plt.ylabel("Ratio of unfair ratings", fontdict={'family': 'Times New Roman', 'size': 12})
    plt.grid(linestyle='-.')
    # plt.savefig('output/1.pdf')
    plt.show()


def second_pic_func():
    b = open("output/second_picture.txt", "r", encoding='UTF-8')
    out = b.read()
    out = json.loads(out)
    c_dict = dict(out)

    x_y_dict = defaultdict(list)
    for key, y_list in c_dict.items():
        x_y_dict["x"].append(round(float(key), 2)*100)
        x_y_dict["linear"].append(y_list[0])
        x_y_dict["square"].append(y_list[1])
        x_y_dict["cube"].append(y_list[2])
        x_y_dict["e"].append(y_list[3])

    plt.plot(x_y_dict["x"], x_y_dict["linear"], color='k', linestyle='-', marker='s', label='F(x) = x')
    plt.plot(x_y_dict["x"], x_y_dict["square"], color='r', linestyle='-', marker='o', label='F(x) = x²')
    plt.plot(x_y_dict["x"], x_y_dict["cube"], color='b', linestyle='-', marker='v', label='F(x)= x³')
    plt.plot(x_y_dict["x"], x_y_dict["e"], color='g', linestyle='-', marker='^', label='F(x) = eˣ')

    plt.legend(loc='upper right', prop={'family': 'Times New Roman', 'size': 12})
    plt.xlim([0, 100])
    plt.ylim([-1, 1])
    plt.xlabel("Percentage of negative ratings", fontdict={'family': 'Times New Roman', 'size': 12})
    plt.ylabel("Trust value offsets", fontdict={'family': 'Times New Roman', 'size': 12})
    plt.grid(linestyle='-.')
    # plt.savefig('output/2.pdf')
    plt.show()


def optimized_first_pic_func():
    b = open("output/message_disturb_probability_count_fuc3_0.5.txt", "r", encoding='UTF-8')  # 0.5
    b2 = open("output/message_disturb_order_probability_count_fuc3_0.5.txt", "r", encoding='UTF-8')  # 0.1
    b3 = open("output/message_disturb_order_probability_count_fuc2_0.5.txt", "r", encoding='UTF-8')  # 0.1 new
    b4 = open("output/message_disturb_probability_count_fuc2_0.5.txt", "r", encoding='UTF-8')  # 0.5 new

    c_dict = dict(json.loads(b.read()))
    c2_dict = dict(json.loads(b2.read()))
    c3_dict = dict(json.loads(b3.read()))
    c4_dict = dict(json.loads(b4.read()))

    x = []
    y = []
    for key, values in c_dict.items():
        x.append(round(float(key), 2)*100)
        y.append(round(values, 2))
    y[-1] = 1

    x2 = []
    y2 = []
    for key, values in c2_dict.items():
        x2.append(round(float(key), 2)*100)
        y2.append(round(values, 2))
    y2[-1] = 1

    x3 = []
    y3 = []
    for key, values in c3_dict.items():
        x3.append(round(float(key), 2)*100)
        y3.append(round(values, 2))
    y3[-1] = 1

    x4 = []
    y4 = []
    for key, values in c4_dict.items():
        x4.append(round(float(key), 2) * 100)
        y4.append(round(values, 2))
    y4[-1] = 1

    # fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=300)
    fig, ax = plt.subplots(1, 1, dpi=300)
    newlinewidth = 1
    markersize = 4
    x_newticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    y_newticks = np.arange(0, 1.1, 0.1)
    ax.plot(x3, y3, color='g', linewidth=newlinewidth, marker='v', markersize=markersize,
            label='BDTM with Non-subjective fake response')
    ax.plot(x2, y2, color='k', linewidth=newlinewidth, marker='s', markersize=markersize,
            label='DRMWT with Non-subjective fake response')
    ax.plot(x, y, color='r', linewidth=newlinewidth, marker='o', markersize=markersize,
            label='BDTM with subjective fake response')
    ax.plot(x4, y4, color='b', linewidth=newlinewidth, marker='^', markersize=markersize,
            label='DRMWT with subjective fake response')

    ax.hlines(0.5, x_newticks[0], x_newticks[-1], colors='0.5', linewidth=newlinewidth*2, linestyles="dashed",
              label='Threshold of answer inference δ')
    plt.legend(loc='upper left', prop={'size': 10})

    ax.set_xticks(x_newticks)
    ax.set_yticks(y_newticks)
    ax.set_xlabel("Percentage of fake response", fontdict={'size': 10})
    ax.set_ylabel("Ratio of false request result", fontdict={'size': 10})
    ax.grid(linestyle='-.')
    plt.xlim(x_newticks[0], 100)
    plt.ylim(0, 1)

    fig.tight_layout()
    fig.savefig('output/(4)ratio.pdf', dpi=300)
    plt.show()


def final_pic_func():
    x_TPS = np.array([10, 15, 30, 65, 98, 200, 400, 600, 1050, 1500])
    y_blcok_75 = np.array([8.9, 12.1, 14.8, 13.9, 15.9, 17.3, 19.5, 24.6, 29.5, 38])
    y_blcok_50 = np.array([8.9, 12.2, 13.8, 14.5, 15.4, 16.3, 20.5, 26.6, 28.5, 37])
    y_blcok_25 = np.array([8.9, 12.2, 13.8, 13.2, 16.7, 17.3, 21.5, 24.5, 27.5, 38])

    # y_random = [20.4, 15.6, 9.05, 6.85, 8.69]
    y_75 = np.array([3, 5.09, 7.22, 7.52, 7.95, 7.96, 8.00, 7.98, 8.09, 8.04])
    y_75_min = np.array([2.6, 2.09, 3.9, 4.7, 4.1, 4.2, 4.3, 4.3, 4.5, 4.5])
    y_75_max = np.array([3.5, 7.09, 10.1, 11.7, 11.1, 11.7, 11.4, 12.1, 12.3, 12.1])

    y_50 = np.array([1, 3.19, 4.22, 4.48, 4.48, 4.54, 4.47, 4.56, 4.58, 4.54])
    y_50_min = np.array([0.8, 3.1, 2.7, 2.5, 2.5, 2.7, 2.5, 2.6, 2.5, 2.5])
    y_50_max = np.array([1.5, 5.4, 7.9, 7.0, 7.1, 7.3, 6.9, 7.1, 7.2, 7.15])

    y_25 = np.array([0.5, 2.26, 3.25, 3.98, 3.96, 3.94, 3.98, 4.01, 3.96, 3.88])
    y_25_min = np.array([0.3, 1.6, 1.7, 2.1, 1.6, 2, 2.2, 2.1, 2.2, 2.25])
    y_25_max = np.array([1, 3.5, 4.7, 5.6, 5.5, 5.8, 5.8, 5.6, 5.75, 5.8])

    # # y_first_random = [1.4, 2.0, 2.5, 2.8, 3.75]
    y_first_25 = [0.1, 0.2, 0.3, 0.65, 0.85, 1.05, 1.2, 1.2, 1.2, 1.1]
    y_first_50 = [0.1, 0.2, 0.4, 0.7, 0.85, 1.05, 1.1, 1.1, 1.2, 1.1]
    y_first_75 = [0.1, 0.2, 0.5, 0.7, 0.85, 1.1, 1.2, 1.2, 1.3, 1.3]

    # def y_func(a, b, lst):
    #     _lst = []
    #     for i in lst:
    #         _lst.append((a * math.log(i)) + b)
    #     return _lst
    #
    # y_75_lst = y_func(1.0294, 1.6153, x_TPS)
    # y_50_lst = y_func(0.5958, 1.1514, x_TPS)
    # y_25_lst = y_func(0.5525, 0.4171, x_TPS)

    # x_new = np.linspace(x_TPS.min(), x_TPS.max(), 12)
    # y_75_smooth = make_interp_spline(x_TPS, y_75)(x_new)
    # y_50_smooth = make_interp_spline(x_TPS, y_50)(x_new)
    # y_25_smooth = make_interp_spline(x_TPS, y_25)(x_new)


    newlinewidth = 1.5
    markersize = 10
    fig, ax = plt.subplots(1, 3, figsize=(16, 18), dpi=300)
    plt.subplots_adjust(wspace=0.2, hspace=0)  # 调整子图间距
    # fig, ax = plt.subplots(3, 1, dpi=300)
    # ax.plot(x_TPS, y_random, color='k', linewidth=newlinewidth, marker='s', markersize=markersize,
    #         label='Confirmed with random selection')

    ax[0].plot(x_TPS, y_75, color='r', linewidth=newlinewidth, marker='o', markersize=markersize,
            label='Average Time')
    ax[0].plot(x_TPS, y_75_min, color='g', linewidth=newlinewidth, marker='v', markersize=markersize,
            label='Lower Bounds')
    ax[0].plot(x_TPS, y_75_max, color='b', linewidth=newlinewidth, marker='^', markersize=markersize,
            label='Upper Bounds')
    ax[0].plot(x_TPS, y_first_75, color='0.5', linestyle='--', linewidth=newlinewidth, marker='*', markersize=markersize,
            label='Frist confirming')
    ax[0].plot(x_TPS, y_blcok_75, color='m', linestyle='--', linewidth=newlinewidth, marker='D', markersize=markersize,
            label='Private Ethereum confirming')
    ax[1].plot(x_TPS, y_50, color='r', linewidth=newlinewidth, marker='o', markersize=markersize,
            label='Average Time')
    ax[1].plot(x_TPS, y_50_min, color='g', linewidth=newlinewidth, marker='v', markersize=markersize,
            label='Lower Bounds')
    ax[1].plot(x_TPS, y_50_max, color='b', linewidth=newlinewidth, marker='^', markersize=markersize,
            label='Upper Bounds')
    ax[1].plot(x_TPS, y_first_50, color='0.5', linestyle='--', linewidth=newlinewidth, marker='*',markersize=markersize,
            label='Frist_confirming')
    ax[1].plot(x_TPS, y_blcok_50, color='m', linestyle='--', linewidth=newlinewidth, marker='D',markersize=markersize,
            label='Private Ethereum confirming')
    ax[2].plot(x_TPS, y_25, color='r', linewidth=newlinewidth, marker='o', markersize=markersize,
            label='Average Time')
    ax[2].plot(x_TPS, y_25_min, color='g', linewidth=newlinewidth, marker='v', markersize=markersize,
            label='Lower Bounds')
    ax[2].plot(x_TPS, y_25_max, color='b', linewidth=newlinewidth, marker='^', markersize=markersize,
            label='Upper Bounds')
    # ax.plot(x_TPS, y_first_random, color='0.5', linestyle='--', linewidth=newlinewidth, marker='', markersize=markersize,
    #         label='Frist_confirming_random')
    ax[2].plot(x_TPS, y_first_25, color='0.5', linestyle='--', linewidth=newlinewidth, marker='*', markersize=markersize,
            label='Frist confirming')
    ax[2].plot(x_TPS, y_blcok_25, color='m', linestyle='--', linewidth=newlinewidth, marker='D', markersize=markersize,
            label='Private Ethereum confirming')
    ax[0].set_xlim(10, 1500)
    ax[0].set_ylim(0, 40)
    ax[0].grid(linestyle='-.')
    ax[1].set_xlim(10, 1500)
    ax[1].set_ylim(0, 40)
    ax[1].grid(linestyle='-.')
    ax[2].set_xlim(10, 1500)
    ax[2].set_ylim(0, 40)
    ax[2].grid(linestyle='-.')

    xminorLocator = MultipleLocator(10)
    ax[0].xaxis.set_minor_locator(xminorLocator)
    ax[0].set_xscale('log')
    ax[0].legend(loc='upper left', prop={'size': 16})
    ax[0].set_xlabel("Transactions per second (TPS)  L/N = 1", fontdict={'size': 16})
    ax[0].set_ylabel("Confirming latency (sec)", fontdict={'size': 16})
    ax[1].xaxis.set_minor_locator(xminorLocator)
    ax[1].set_xscale('log')
    ax[1].legend(loc='upper left', prop={'size': 16})
    ax[1].set_xlabel("Transactions per second (TPS)  L/N = 1/2", fontdict={'size': 16})
    ax[1].set_ylabel("Confirming latency (sec)", fontdict={'size': 16})
    ax[2].xaxis.set_minor_locator(xminorLocator)
    ax[2].set_xscale('log')
    ax[2].legend(loc='upper left', prop={'size': 16})
    ax[2].set_xlabel("Transactions per second (TPS) L/N = 1/4", fontdict={'size': 16})
    ax[2].set_ylabel("Confirming latency (sec)", fontdict={'size': 16})
    ax[0].tick_params(labelsize=14)
    ax[1].tick_params(labelsize=14)
    ax[2].tick_params(labelsize=14)


    fig.savefig('output/(3)TPS v2.pdf', dpi=300)

    plt.show()
    gc.collect()


def final_pic_func_test():
    x_TPS = np.array([10, 15, 30, 65, 98, 200, 400, 600, 1050, 1500])
    # y_blcok_75 = np.array([8.9, 12.1, 14.8, 13.9, 15.9, 17.3, 19.5, 24.6, 29.5, 38])
    # y_blcok_50 = np.array([8.9, 12.2, 13.8, 14.5, 15.4, 16.3, 20.5, 26.6, 28.5, 37])
    y_blcok_25 = np.array([8.9, 12.2, 13.8, 13.2, 16.7, 17.3, 21.5, 24.5, 27.5, 38])

    # y_random = [20.4, 15.6, 9.05, 6.85, 8.69]
    # y_75 = np.array([3, 5.09, 7.22, 7.52, 7.95, 7.96, 8.00, 7.98, 8.09, 8.04])
    # y_75_min = np.array([2.6, 2.09, 3.9, 4.7, 4.1, 4.2, 4.3, 4.3, 4.5, 4.5])
    # y_75_max = np.array([3.5, 7.09, 10.1, 11.7, 11.1, 11.7, 11.4, 12.1, 12.3, 12.1])

    # y_50 = np.array([1, 3.19, 4.22, 4.48, 4.48, 4.54, 4.47, 4.56, 4.58, 4.54])
    # y_50_min = np.array([0.8, 3.1, 2.7, 2.5, 2.5, 2.7, 2.5, 2.6, 2.5, 2.5])
    # y_50_max = np.array([1.5, 5.4, 7.9, 7.0, 7.1, 7.3, 6.9, 7.1, 7.2, 7.15])
    #
    y_25 = np.array([0.5, 2.26, 3.25, 3.98, 3.96, 3.94, 3.98, 4.01, 3.96, 3.88])
    y_25_min = np.array([0.3, 1.6, 1.7, 2.1, 1.6, 2, 2.2, 2.1, 2.2, 2.25])
    y_25_max = np.array([1, 3.5, 4.7, 5.6, 5.5, 5.8, 5.8, 5.6, 5.75, 5.8])

    # # y_first_random = [1.4, 2.0, 2.5, 2.8, 3.75]
    y_first_25 = [0.1, 0.2, 0.3, 0.65, 0.85, 1.05, 1.2, 1.2, 1.2, 1.1]
    # y_first_50 = [0.1, 0.2, 0.4, 0.7, 0.85, 1.05, 1.1, 1.1, 1.2, 1.1]
    # y_first_75 = [0.1, 0.2, 0.5, 0.7, 0.85, 1.1, 1.2, 1.2, 1.3, 1.3]

    # def y_func(a, b, lst):
    #     _lst = []
    #     for i in lst:
    #         _lst.append((a * math.log(i)) + b)
    #     return _lst
    #
    # y_75_lst = y_func(1.0294, 1.6153, x_TPS)
    # y_50_lst = y_func(0.5958, 1.1514, x_TPS)
    # y_25_lst = y_func(0.5525, 0.4171, x_TPS)

    # x_new = np.linspace(x_TPS.min(), x_TPS.max(), 12)
    # y_75_smooth = make_interp_spline(x_TPS, y_75)(x_new)
    # y_50_smooth = make_interp_spline(x_TPS, y_50)(x_new)
    # y_25_smooth = make_interp_spline(x_TPS, y_25)(x_new)


    newlinewidth = 1.5
    fig, ax = plt.subplots(1, 1, figsize=(7.1, 5), dpi=400)
    ax.plot(x_TPS, y_25, color='r', linewidth=newlinewidth, marker='o',
            label='Average latency(TAG confirming latency)')
    ax.plot(x_TPS, y_25_min, color='g', linewidth=newlinewidth, marker='v',
            label='Lower Bounds(TAG confirming latency)')
    ax.plot(x_TPS, y_25_max, color='b', linewidth=newlinewidth, marker='^',
            label='Upper Bounds(TAG confirming latency)')
    ax.plot(x_TPS, y_first_25, color='0.5', linestyle='--', linewidth=newlinewidth, marker='*',
            label='Frist confirming(TAG confirming latency)')
    ax.plot(x_TPS, y_blcok_25, color='m', linestyle='--', linewidth=newlinewidth, marker='D',
            label='Private Ethereum confirming latency')

    ax.set_xlim(10, 1500)
    ax.set_ylim(0, 40)
    ax.grid(linestyle='-.')

    xminorLocator = MultipleLocator(10)
    ax.xaxis.set_minor_locator(xminorLocator)
    ax.set_xscale('log')
    ax.legend(loc='upper left', prop={'size': 12})
    ax.set_xlabel("Transactions per second (TPS)  L/N = 1/4", fontdict={'size': 12})
    ax.set_ylabel("Confirming latency (sec)", fontdict={'size': 12})

    fig.savefig('output/(3)TPS v3.pdf', dpi=400)

    plt.show()
    gc.collect()


def reputation_calculation_v1(num_of_good, num_of_bad, consensus_behavior):

    def func_f(x):
        return x
    theta_1 = func_f(num_of_good) / (func_f(num_of_good) + func_f(num_of_bad))
    theta_2 = func_f(num_of_bad) / (func_f(num_of_good) + func_f(num_of_bad))
    sigma_sharing_metric = ((theta_1 * num_of_good) - (theta_2 * num_of_bad)) / (num_of_good + num_of_bad)

    def consensus_process(behaviors):
        a = 0.0
        b = 0.0
        for i in behaviors:
            a += i
            b += abs(i)

        return a / b
    eta_consensus_metric = consensus_process(consensus_behavior)
    return sigma_sharing_metric, eta_consensus_metric


def reputation_calculation_v2(num_of_good, num_of_bad, consensus_behavior):

    def func_f(x):
        return x * x * x
    theta_1 = func_f(num_of_good) / (func_f(num_of_good) + func_f(num_of_bad))
    theta_2 = func_f(num_of_bad) / (func_f(num_of_good) + func_f(num_of_bad))
    sigma_sharing_metric = ((theta_1 * num_of_good) - (theta_2 * num_of_bad)) / (num_of_good + num_of_bad)

    def consensus_process(behaviors):
        a = 0.0
        b = 0.0
        for i in behaviors:
            a += i
            b += abs(i)

        return a / b
    eta_consensus_metric = consensus_process(consensus_behavior)
    return sigma_sharing_metric, eta_consensus_metric


def consensus_contri_generation(input_ratio, bad_para):
    real_ration = (100-input_ratio) / 100
    bad_contri = 10 * real_ration
    default_consensus_contri_list = []
    for i in range(10-int(bad_contri)):
        default_consensus_contri_list.append(10)
    for j in range(int(bad_contri)):
        default_consensus_contri_list .append(bad_para)
    return default_consensus_contri_list


def normlization_func(input_value):
    return (input_value - -1) / 2


def reputation_process():
    good_and_bad = range(100, -5, -5)
    consensus = [1, 1]
    x_range = []
    list_sharing_res_v1 = []
    list_sharing_res_with_1_v1 = []
    list_sharing_res_with_2_v1 = []

    list_sharing_res_v2 = []
    list_sharing_res_with_1_v2 = []
    list_sharing_res_with_2_v2 = []
    for i in good_and_bad:
        consensus_contri_list_1 = consensus_contri_generation(i, -10)
        consensus_contri_list_2 = consensus_contri_generation(i, -20)
        sharing_res_with_1_v1, consensus_res_with_1_v1 = reputation_calculation_v1(i, 100-i, consensus_contri_list_1)
        sharing_res_with_2_v1, consensus_res_with_2_v1 = reputation_calculation_v1(i, 100-i, consensus_contri_list_2)
        sharing_res_v1, consensus_res_v1 = reputation_calculation_v1(i, 100-i, consensus)

        sharing_res_with_1_v2, consensus_res_with_1_v2 = reputation_calculation_v2(i, 100-i, consensus_contri_list_1)
        sharing_res_with_2_v2, consensus_res_with_2_v2 = reputation_calculation_v2(i, 100-i, consensus_contri_list_2)
        sharing_res_v2, consensus_res_v2 = reputation_calculation_v2(i, 100-i, consensus)

        x_range.append(100-i)
        list_sharing_res_v1.append(normlization_func(((0.5 * sharing_res_v1)+(0.5 * consensus_res_v1))))
        list_sharing_res_with_1_v1.append(normlization_func(((0.5 * sharing_res_with_1_v1)+(0.5 * consensus_res_with_1_v1))))
        list_sharing_res_with_2_v1.append(normlization_func(((0.5 * sharing_res_with_2_v1)+(0.5 * consensus_res_with_2_v1))))

        list_sharing_res_v2.append(normlization_func(((0.5 * sharing_res_v2) + (0.5 * consensus_res_v2))))
        list_sharing_res_with_1_v2.append(normlization_func(((0.5 * sharing_res_with_1_v2) + (0.5 * consensus_res_with_1_v2))))
        list_sharing_res_with_2_v2.append(normlization_func(((0.5 * sharing_res_with_2_v2) + (0.5 * consensus_res_with_2_v2))))

    x_TWSL_list = [10, 20, 30, 40, 50, 60, 70, 80]
    y_TWSL_list = [0.9, 0.81, 0.71, 0.66, 0.59, 0.5, 0.41, 0.32]
    fig, ax = plt.subplots(1, 1, dpi=300)
    newlinewidth = 1
    markersize = 4
    x_newticks = range(10, 85, 5)
    y_newticks = np.arange(0.0, 1.1, 0.1)

    ax.plot([10, 80], [0.95, 0.61], color='k', linewidth=newlinewidth,
            linestyle="dashed", label='TSL Scheme')
    ax.plot(x_TWSL_list, y_TWSL_list, color='r', linewidth=newlinewidth, marker='o', markersize=markersize,
            linestyle="dashed", label='TWSL Scheme')
    ax.plot(x_range, list_sharing_res_v1, color='g', linewidth=newlinewidth, marker='v', markersize=markersize,
            label='DRMWT without CM F(x)=${x}$')
    ax.plot(x_range, list_sharing_res_v2, color='g', linewidth=newlinewidth, marker='v', markersize=markersize,
            linestyle="dashdot", label='DRMWT without CM F(x)=${x^3}$')
    ax.plot(x_range, list_sharing_res_with_1_v1, color='b', linewidth=newlinewidth, marker='^', markersize=markersize,
            label='DRMWT with CM F(x)=${x}$')
    ax.plot(x_range, list_sharing_res_with_1_v2, color='b', linewidth=newlinewidth, marker='^', markersize=markersize,
            linestyle="dashdot", label='DRMWT with CM F(x)=${x^3}$')
    ax.plot(x_range, list_sharing_res_with_2_v1, color='m', linewidth=newlinewidth, marker='p', markersize=markersize,
            label='DRMWT with CM (lazy node) F(x)=${x}$')
    ax.plot(x_range, list_sharing_res_with_2_v2, color='m', linewidth=newlinewidth, marker='p', markersize=markersize,
            linestyle="dashdot", label='DRMWT with CM (lazy node) F(x)=${x^3}$')

    ax.hlines(0.5, x_newticks[0], x_newticks[-1], colors='0.5', linewidth=newlinewidth*2, linestyles="dashed",
              label='Threshold of answer inference δ')
    plt.legend(loc='upper right', prop={'size': 8})

    ax.set_xticks(x_newticks)
    ax.set_yticks(y_newticks)
    ax.set_xlabel("Percentage of misbehavior of an abnormal vehicle", fontdict={'size': 10})
    ax.set_ylabel("Reputation value", fontdict={'size': 10})
    ax.grid(linestyle='-.')
    plt.xlim(10, 80)
    plt.ylim(0.3, 1.0)

    fig.tight_layout()
    fig.savefig('output/(5)ratio.pdf', dpi=300)
    plt.show()


if __name__ == "__main__":
    # first_pic_func()
    # second_pic_func()
    # optimized_first_pic_func()
    # final_pic_func()
    # final_pic_func_test()
    reputation_process()
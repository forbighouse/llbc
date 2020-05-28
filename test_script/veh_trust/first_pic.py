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
    plt.savefig('output/1.pdf')
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
    plt.savefig('output/2.pdf')
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
    newlinewidth = 1.5
    markersize = 6
    x_newticks = range(0, 105, 10)
    y_newticks = np.arange(0, 1.1, 0.1)
    ax.plot(x3, y3, color='g', linewidth=newlinewidth, marker='v', markersize=markersize,
            label='BDTM')
    ax.plot(x2, y2, color='k', linewidth=newlinewidth, marker='s', markersize=markersize,
            label='DRMWT')
    ax.plot(x, y, color='r', linewidth=newlinewidth, marker='o', markersize=markersize,
            label='BDTM with Malicious Nodes')
    ax.plot(x4, y4, color='b', linewidth=newlinewidth, marker='^', markersize=markersize,
            label='DRMWT with Malicious Nodes')

    ax.hlines(0.5, x_newticks[0], x_newticks[-1], colors='0.5', linewidth=newlinewidth*2, linestyles="dashed")
    plt.legend(loc='upper left', prop={'size': 12})

    ax.set_xticks(x_newticks)
    ax.set_yticks(y_newticks)
    ax.set_xlabel("Percentage of fake response", fontdict={'size': 14})
    ax.set_ylabel("Ratio of false request result", fontdict={'size': 14})
    ax.grid(True)
    plt.xlim(x_newticks[0], 100)
    plt.ylim(0, 1)


    # fig.tight_layout()
    fig.savefig('output/(4)ratio.pdf', dpi=300)
    plt.show()


def final_pic_func():
    x_TPS = np.array([10, 15, 30, 65, 98, 200, 400, 600, 1050, 1500])
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
    fig, ax = plt.subplots(3, 1, figsize=(16, 14), dpi=300)
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
            label='Frist_confirming')
    ax[1].plot(x_TPS, y_50, color='r', linewidth=newlinewidth, marker='o', markersize=markersize,
            label='Average Time')
    ax[1].plot(x_TPS, y_50_min, color='g', linewidth=newlinewidth, marker='v', markersize=markersize,
            label='Lower Bounds')
    ax[1].plot(x_TPS, y_50_max, color='b', linewidth=newlinewidth, marker='^', markersize=markersize,
            label='Upper Bounds')
    ax[1].plot(x_TPS, y_first_50, color='0.5', linestyle='--', linewidth=newlinewidth, marker='*',
               markersize=markersize, label='Frist_confirming')
    ax[2].plot(x_TPS, y_25, color='r', linewidth=newlinewidth, marker='o', markersize=markersize,
            label='Average Time')
    ax[2].plot(x_TPS, y_25_min, color='g', linewidth=newlinewidth, marker='v', markersize=markersize,
            label='Lower Bounds')
    ax[2].plot(x_TPS, y_25_max, color='b', linewidth=newlinewidth, marker='^', markersize=markersize,
            label='Upper Bounds')
    # ax.plot(x_TPS, y_first_random, color='0.5', linestyle='--', linewidth=newlinewidth, marker='', markersize=markersize,
    #         label='Frist_confirming_random')
    ax[2].plot(x_TPS, y_first_25, color='0.5', linestyle='--', linewidth=newlinewidth, marker='*', markersize=markersize,
            label='Frist_confirming')
    ax[0].set_xlim(10, 1500)
    ax[0].set_ylim(0, 12.5)
    ax[0].grid(linestyle='-.')
    ax[1].set_xlim(10, 1500)
    ax[1].set_ylim(0, 12.5)
    ax[1].grid(linestyle='-.')
    ax[2].set_xlim(10, 1500)
    ax[2].set_ylim(0, 12.5)
    ax[2].grid(linestyle='-.')

    xminorLocator = MultipleLocator(10)
    ax[0].xaxis.set_minor_locator(xminorLocator)
    ax[0].set_xscale('log')
    ax[0].legend(loc='upper left', prop={'size': 16})
    ax[0].set_xlabel("Transactions per second (TPS)  L/N = 1", fontdict={'size': 16})
    ax[0].set_ylabel("Confirming time (sec)", fontdict={'size': 16})
    ax[1].xaxis.set_minor_locator(xminorLocator)
    ax[1].set_xscale('log')
    ax[1].set_xscale('log')
    ax[1].legend(loc='upper left', prop={'size': 16})
    ax[1].set_xlabel("Transactions per second (TPS)  L/N = 1/2", fontdict={'size': 16})
    ax[1].set_ylabel("Confirming time (sec)", fontdict={'size': 16})
    ax[2].xaxis.set_minor_locator(xminorLocator)
    ax[2].set_xscale('log')
    ax[2].set_xscale('log')
    ax[2].legend(loc='upper left', prop={'size': 16})
    ax[2].set_xlabel("Transactions per second (TPS) L/N = 1/4", fontdict={'size': 16})
    ax[2].set_ylabel("Confirming time (sec)", fontdict={'size': 16})
    ax[0].tick_params(labelsize=14)
    ax[1].tick_params(labelsize=14)
    ax[2].tick_params(labelsize=14)


    fig.savefig('output/(3)TPS v2.pdf', dpi=300)

    plt.show()
    gc.collect()


if __name__ == "__main__":
    # first_pic_func()
    # second_pic_func()
    # optimized_first_pic_func()
    final_pic_func()

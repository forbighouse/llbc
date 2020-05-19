import json
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
from matplotlib.ticker import MultipleLocator


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

    fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=300)
    newlinewidth = 1.5
    markersize = 10
    x_newticks = range(0, 105, 10)
    y_newticks = np.arange(0, 1.1, 0.1)
    ax.plot(x3, y3, color='g', linewidth=newlinewidth, marker='v', markersize=markersize,
            label='No reputation scheme')
    ax.plot(x2, y2, color='k', linewidth=newlinewidth, marker='s', markersize=markersize,
            label='Proposed scheme')
    ax.plot(x, y, color='r', linewidth=newlinewidth, marker='o', markersize=markersize,
            label='No reputation scheme with random fake response')
    ax.plot(x4, y4, color='b', linewidth=newlinewidth, marker='^', markersize=markersize,
            label='Proposed scheme with random fake response')

    ax.hlines(0.5, x_newticks[0], x_newticks[-1], colors='0.5', linewidth=newlinewidth*2, linestyles="dashed")
    plt.legend(loc='upper left', prop={'size': 16})

    ax.set_xticks(x_newticks)
    ax.set_yticks(y_newticks)
    ax.set_xlabel("Percentage of fake response", fontdict={'size': 14})
    ax.set_ylabel("Ratio of unfair rating on response", fontdict={'size': 14})
    # ax.grid(True)
    plt.xlim(x_newticks[0], 100)
    plt.ylim(0, 1)


    # fig.tight_layout()
    # fig.savefig('output/(4)ratio.pdf', dpi=300)
    plt.show()


def final_pic_func():
    x_TPS = [1, 5, 10, 250, 5000, 10000]
    y_random = [20.4, 15.6, 9.05, 6.85, 8.69]
    y_75 = [15.5, 9.32, 5.86, 5.36, 4.8]
    y_50 = [10.45, 7.99, 5.17, 4.18, 3.79]
    y_25 = [6.7, 4.5, 3.6, 3.3, 2.7]
    y_first_random = [1.4, 2.0, 2.5, 2.8, 3.75]
    y_first_proposed = [0.5, 0.7, 1.05, 1.45, 1.8]
    newlinewidth = 1.5
    markersize = 10
    fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=300)
    ax.plot(x_TPS, y_random, color='k', linewidth=newlinewidth, marker='s', markersize=markersize,
            label='Confirmed with random selection')
    ax.plot(x_TPS, y_75, color='r', linewidth=newlinewidth, marker='o', markersize=markersize,
            label='Confirmed with L/N=1')
    ax.plot(x_TPS, y_50, color='b', linewidth=newlinewidth, marker='v', markersize=markersize,
            label='Confirmed with L/N=1/2')
    ax.plot(x_TPS, y_25, color='g', linewidth=newlinewidth, marker='^', markersize=markersize,
            label='Confirmed with L/N=1/4')
    ax.plot(x_TPS, y_first_random, color='0.5', linestyle='--', linewidth=newlinewidth, marker='', markersize=markersize,
            label='Frist_confirming_random')
    ax.plot(x_TPS, y_first_proposed, color='0.5', linestyle='--', linewidth=newlinewidth, marker='*', markersize=markersize,
            label='Frist_confirming')

    xminorLocator = MultipleLocator(10)
    ax.xaxis.set_minor_locator(xminorLocator)

    # ax.set_xlim(0, 10000)
    plt.legend(loc='upper right', prop={'size': 12})
    # plt.xlim([0, 100])
    # plt.ylim([-1, 1])
    plt.xlabel("Transactions per second (TPS)", fontdict={'size': 12})
    plt.ylabel("Confirming time (sec)", fontdict={'size': 12})
    plt.grid(linestyle='-.')
    plt.xscale('log')
    # fig.savefig('output/(3)TPS.pdf', dpi=300)

    plt.show()


if __name__ == "__main__":
    # first_pic_func()
    # second_pic_func()
    # optimized_first_pic_func()
    final_pic_func()

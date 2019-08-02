import json
import matplotlib.pyplot as plt
from collections import defaultdict


def first_pic_func():
    b = open("output/message_disturb_order_probability_count_fuc4_0.5", "r", encoding='UTF-8')
    b2 = open("output/message_disturb_order_probability_count_fuc4_0.1", "r", encoding='UTF-8')

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
    b2 = open("output/message_disturb_probability_count_fuc3_0.1.txt", "r", encoding='UTF-8')  # 0.1
    b3 = open("output/message_disturb_probability_count_fuc2_0.1.txt", "r", encoding='UTF-8')  # 0.1 new
    b4 = open("output/message_disturb_probability_count_fuc2_0.5.txt", "r", encoding='UTF-8')  # 0.5 new

    out = b.read()
    out2 = b2.read()
    out3 = b3.read()
    out4 = b4.read()

    out = json.loads(out)
    out2 = json.loads(out2)
    out3 = json.loads(out3)
    out4 = json.loads(out4)

    c_dict = dict(out)
    c2_dict = dict(out2)
    c3_dict = dict(out3)
    c4_dict = dict(out4)

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

    x3 = []
    y3 = []
    for key, values in c3_dict.items():
        x3.append(round(float(key), 2)*100)
        y3.append(values)

    x4 = []
    y4 = []
    for key, values in c4_dict.items():
        x4.append(round(float(key), 2) * 100)
        y4.append(values)

    plt.plot(x2, y2, color='k', linestyle='-', marker='s', label='PE = 0.1')
    plt.plot(x, y, color='r', linestyle='-', marker='o', label='PE = 0.5')
    plt.plot(x3, y3, color='g', linestyle='-', marker='p', label='PE = 0.1 new')
    plt.plot(x4, y4, color='b', linestyle='-', marker='h', label='PE = 0.5 new')

    plt.legend(loc='upper left', prop={'family': 'Times New Roman', 'size': 12})
    plt.xlim([0, 100])
    plt.ylim([0, 1])
    plt.xlabel("Percentage of false messages", fontdict={'family': 'Times New Roman', 'size': 12})
    plt.ylabel("Ratio of unfair ratings", fontdict={'family': 'Times New Roman', 'size': 12})
    plt.grid(linestyle='-.')
    plt.savefig('output/5.pdf')
    plt.show()


def final_pic_func():
    x_TPS = [5, 10, 25, 50, 100]
    y_random = [20.4, 15.6, 9.05, 6.25, 5.69]
    y_250 = [15.5, 9.32, 5.7, 3.86, 3.5]
    y_200 = [10.45, 7.99, 3.87, 2.88, 2.49]
    y_150 = [6.7, 4.5, 2.3, 1.6, 1.4]

    plt.plot(x_TPS, y_random, color='k', linestyle='-', marker='s', label='random selection')
    plt.plot(x_TPS, y_250, color='r', linestyle='-', marker='o', label='Θ=250')
    plt.plot(x_TPS, y_200, color='b', linestyle='-', marker='v', label='Θ=200')
    plt.plot(x_TPS, y_150, color='g', linestyle='-', marker='^', label='Θ=150')

    plt.legend(loc='upper right', prop={'family': 'Times New Roman', 'size': 12})
    # plt.xlim([0, 100])
    # plt.ylim([-1, 1])
    plt.xlabel("Transactions per second (TPS)", fontdict={'family': 'Times New Roman', 'size': 12})
    plt.ylabel("Average time of transaction confirm (s)", fontdict={'family': 'Times New Roman', 'size': 12})
    plt.grid(linestyle='-.')
    plt.savefig('output/time-TPS.pdf')
    plt.show()


if __name__ == "__main__":
    # first_pic_func()
    # second_pic_func()
    # optimized_first_pic_func()
    final_pic_func()

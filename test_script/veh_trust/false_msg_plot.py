import json
import matplotlib.pyplot as plt


if __name__ == "__main__":
    b = open("unfair_msg1.txt", "r", encoding='UTF-8')
    b2 = open("unfair_msg2.txt", "r", encoding='UTF-8')
    out = b.read()
    out2 = b2.read()
    out = json.loads(out)
    out2 = json.loads(out2)
    c_dict = dict(out)
    c2_dict = dict(out2)
    x = []
    y = []
    for key, values in c_dict.items():
        x.append(round(float(key), 2))
        y.append(values)

    x2 = []
    y2 = []
    for key, values in c2_dict.items():
        x2.append(round(float(key), 2))
        y2.append(values)

    plt.plot(x, y, color='r', linestyle='-', marker='s', label='Pe = 0.1')
    plt.plot(x2, y2, color='k', linestyle='-', marker='o', label='Pe = 0.5')
    # plt.plot(x, arrs[2], color='b', linestyle='-', marker='v', label='line 3')
    # plt.plot(x, arrs[3], color='g', linestyle='-', marker='^', label='line 4')

    plt.legend(loc='upper right')
    plt.show()

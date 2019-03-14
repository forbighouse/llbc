import json
import matplotlib.pyplot as plt


if __name__ == "__main__":
    b = open("data_source_list.txt", "r", encoding='UTF-8')
    out = b.read()
    out = json.loads(out)
    c_dict = dict(out)
    x = []
    y = []
    for key, values in c_dict.items():
        x.append(key)
        y.append(values)

    plt.plot(x, y, color='k', linestyle='-', marker='s', label='line 1')
    # plt.plot(x, arrs[1], color='r', linestyle='-', marker='o', label='line 2')
    # plt.plot(x, arrs[2], color='b', linestyle='-', marker='v', label='line 3')
    # plt.plot(x, arrs[3], color='g', linestyle='-', marker='^', label='line 4')

    plt.legend(loc='upper right')
    plt.show()

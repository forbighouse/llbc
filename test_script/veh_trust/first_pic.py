import json
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np


if __name__ == "__main__":
    b = open("first_picture.txt", "r", encoding='UTF-8')
    # b2 = open("trust_offset1.txt", "r", encoding='UTF-8')
    # b3 = open("trust_offset2.txt", "r", encoding='UTF-8')
    # b4 = open("trust_offset3.txt", "r", encoding='UTF-8')
    out = b.read()
    # out2 = b2.read()
    # out3 = b3.read()
    # out4 = b4.read()
    out = json.loads(out)
    # out2 = json.loads(out2)
    # out3 = json.loads(out3)
    # out4 = json.loads(out4)
    c_dict = dict(out)
    # c2_dict = dict(out2)
    # c3_dict = dict(out3)
    # c4_dict = dict(out4)

    x = []
    y = []
    for key, values in c_dict.items():
        x.append(round(float(key), 2))
        y.append(values)

    xnew = np.arange(0, 1, 0.01)
    func = interpolate.interp1d(x, y, kind='slinear')

    ynew = func(xnew)

    # x2 = []
    # y2 = []
    # for key, values in c2_dict.items():
    #     x2.append(round(float(key), 2))
    #     y2.append(values)
    #
    # x3 = []
    # y3 = []
    # for key, values in c3_dict.items():
    #     x3.append(round(float(key), 2))
    #     y3.append(values)
    #
    # x4 = []
    # y4 = []
    # for key, values in c4_dict.items():
    #     x4.append(round(float(key), 2))
    #     y4.append(values)

    plt.plot(x, y, color='k', linestyle='-', marker='s', label='ori')
    # plt.plot(xnew, ynew, color='r', linestyle='-', marker='o', label='cha')
    # plt.plot(x3, y3, color='b', linestyle='-', marker='v', label='x³')
    # plt.plot(x4, y4, color='g', linestyle='-', marker='^', label='eˣ')

    plt.legend(loc='upper right')
    plt.show()

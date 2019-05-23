import json
import matplotlib.pyplot as plt
import math

if __name__ == "__main__":
    x1 = list(range(1, 100))

    y1 = []
    y2 = []
    y3 = []
    y4 = []
    y5 = []
    for i in x1:
        y1.append(math.exp(-0.084*i))
        y2.append(1 - math.pow(0.01*i, 3))
        y3.append(1 - math.pow(0.010*i, 3) + math.exp(-0.014*i))
        y4.append(math.pow(2*i, 2))
        y5.append(math.pow(0.2*i, 2))

    plt.plot(x1, y1, color='r', linestyle='-', label='y1')
    plt.plot(x1, y2, color='k', linestyle='-', label='y2')
    # plt.plot(x1, y3, color='b', linestyle='-', label='y3')
    # plt.plot(x, y4, color='g', marker='v', linestyle='-', label='2*i')
    # plt.plot(x, y5, color='b', marker='^', linestyle='-', label='0.2*i')
    # plt.plot(x2, y2, color='k', linestyle='-', marker='o', label='Pe = 0.5')
    # plt.plot(x, arrs[2], color='b', linestyle='-', marker='v', label='line 3')
    # plt.plot(x, arrs[3], color='g', linestyle='-', marker='^', label='line 4')
    # a.yaxis.set_ticks_position('left')
    # a.spines['left'].set_position(('data', 0))
    plt.xlabel('x label')
    plt.ylabel('y label')
    plt.legend(loc='upper right')
    plt.show()

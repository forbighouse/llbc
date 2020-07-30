import random
import sha3
import json
import numpy as np


def distance_cal_x(loc1, loc2):
    assert isinstance(loc1, int)
    assert isinstance(loc2, int)
    if loc1 < loc2:
        return int(loc2 - loc1)
    else:
        return int(loc1 - loc2)


def random_int_list(start, stop, length):
    start, stop = (int(start), int(stop)) if start <= stop else (int(stop), int(start))
    length = int(abs(length)) if length else 0
    random_list = []
    for i in range(length):
        random_list.append(random.randint(start, stop))
    return random_list


def hash_str(address, msg_type):
    x = sha3.shake_128()
    output1 = json.dumps(address)
    output = output1.encode('utf-8')
    x.update(output)
    if msg_type == "request":
        return x.hexdigest(4)
    elif msg_type == "answer":
        return x.hexdigest(8)
    elif msg_type == "rate":
        return x.hexdigest(8)
    elif msg_type == "transaction":
        return x.hexdigest(16)
    else:
        raise TypeError


def transaction_emerge_generator(mean, timer):
    return list(np.random.poisson(lam=mean, size=timer))


def company():
    f = open("2.txt", "rb")
    line = f.readlines()
    # a = line.split(";")
    line = str(line)
    a = line.split(",")

    print(len(a))


    f.close()


if __name__ == '__main__':
    company()
    pass

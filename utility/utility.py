import random
import sha3
import json
from collections import defaultdict


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
    else:
        raise TypeError

if __name__ == '__main__':
    pass

from score.score_gen import Score
from score.node_manager import Monitor
from score.observation import Observation
from blockchain.transactions import Transaction
from blockchain.blocks import *
import score.simulator as s_simulator
from score.nodemanager import ServiceNode
import time
import matplotlib.pyplot as plt
from score.simulator import *

LOCATION_FILE = './test_script/location_test.txt'


def main():
    node1 = ServiceNode(node_type=0, veh_id='00', location=None, observe_vehs=None)
    location_list = s_simulator.file_location(LOCATION_FILE)
    for loc in location_list:
        node1.location = loc
        node1.current_time = time.time()


def simu_test():
    block_body = set()
    for i in range(20):
        block_body.add(Transaction('ASDJIWDJX', 'SDHUWDHI',i, 'MUI'))

    b1 = Block(BlockHeader('GENISS', 'ICSDE', 12, time.perf_counter()),
          block_body)

    return b1


def simu_test1():
    a = accident_factory()
    plt.figure(1)
    plt.plot(list(a))
    plt.show()

if __name__ == "__main__":
    # a = simu_test()
    # print(len(a))
    # b = simu_test1()
    # print(b)
    a = trajectory()
    print(type(a))


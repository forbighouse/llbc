from score.score_gen import Score
from score.node_manager import Monitor
from score.observation import Observation
from blockchain.transactions import Transaction
import score.simulator as s_simulator
from score.nodemanager import ServiceNode
import time

LOCATION_FILE = './test_script/location_test.txt'


def main():
    node1 = ServiceNode(node_type=0, veh_id='00', location=None, observe_vehs=None)
    location_list = s_simulator.file_location(LOCATION_FILE)
    for loc in location_list:
        node1.location = loc
        node1.current_time = time.time()



if __name__ == "__main__":
    main()

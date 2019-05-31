import uuid
import random
from collections import defaultdict
from test_script.veh_trust.trust_v2 import MAX_SPEED
from test_script.veh_trust.config import *


def veh_test_location(veh_num):
    distance_veh = random.sample(range(5, 100), veh_num)
    start_point = random.sample(range(5, 100), 1)
    veh_locations = []
    d_location = 0
    for i in distance_veh:
        d_location += start_point[0] + i
        veh_locations.append(d_location)
    veh_id_list = [str(uuid.uuid3(uuid.NAMESPACE_DNS, str(i))) for i in range(veh_num)]
    with open(VEH_LOCATION_FILE, 'w')as w:
        for id_index in range(veh_num):
            strw = '{};{}'.format(str(veh_id_list[id_index]), veh_locations[id_index])
            w.write(strw)
            w.write('\n')


def accident_test_location(accident_num, accident_type, road_len):
    accident_type = accident_type
    accidents = []
    write_to_file = []
    for i in range(accident_num):
        accidents.append([str(i), (random.randint(0, ROAD_LEN), 0), accident_type])
        write_to_file.append('{};{};{}'.format(str(i), str((random.randint(0, road_len), 0)), str(accident_type)))

    with open(ACCIDENT_LOCATION_FILE, 'w') as w:
        for strs in write_to_file:
            w.write(strs)
            w.write('\n')


def bl_address(bl_address_num=BLOCKCHAIN_ADDRESS_TOTAL_NUM , bl_address_file=BLOCKCHAIN_ADDRESS_FILE):
    bl_address_list = [str(uuid.uuid3(uuid.NAMESPACE_DNS, str(i))) for i in range(bl_address_num)]
    with open(bl_address_file, 'w')as w:
        for address in bl_address_list:
            address = address.split('-')
            stra = ''
            address = stra.join(address)
            w.write(address)
            w.write('\n')


def veh_speed_test():
    veh_ids = []
    with open('veh_list.txt', 'r') as handler:
        for x in handler:
            x = x.strip('\n').split(';')
            veh_ids.append(x[0])

    veh_speed_init_dict = defaultdict(int)
    for tmp_veh1 in veh_ids:
        veh_speed_init_dict[tmp_veh1] = random.choice(range(-MAX_SPEED, MAX_SPEED))
    with open(VEH_SPEED_FILE, 'w')as w:
        for veh_id, veh_spped in veh_speed_init_dict.items():
            strw = '{};{}'.format(str(veh_id), str(veh_spped))
            w.write(strw)
            w.write('\n')


if __name__ == "__main__":
    # veh_test_location(VEH_NUM)
    # accident_test_location(ACCIDENT_NUM, ACCIDENT_TYPE, ROAD_LEN)
    # bl_address()
    veh_speed_test()

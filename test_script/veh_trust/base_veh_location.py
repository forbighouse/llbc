import uuid
import random

# 仿真车辆的数量
VEH_NUM = 50
# veh位置的文件名称
VEH_LOCATION_FILE = 'veh_list.txt'
# accident的文件名称
ACCIDENT_LOCATION_FILE = 'accident_list.txt'
# 事件的类型，例如车祸、红绿灯、限行、拥堵等
ACCIDENT_TYPE = 0
# 仿真的事件数量
ACCIDENT_NUM = 5
# 道路长度，目前只有一条直路
ROAD_LEN = 5000


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


if __name__ == "__main__":
    veh_test_location(VEH_NUM)
    accident_test_location(ACCIDENT_NUM, ACCIDENT_TYPE, ROAD_LEN)

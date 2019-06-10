from test_script.veh_trust.config import *


def accident_factory(accident_fast_mode=0):
    accident_type = ACCIDENT_TYPE
    accidents = []
    ids = []
    contents = []
    for i in range(ACCIDENT_NUM):
        x = random.randint(0, ROAD_LEN)
        accidents.append([str(i), (x, 0), accident_type])
        ids.append(str(i))
        contents.append([(x, 0), accident_type])

    if accident_fast_mode:
        accident_dict = dict(zip(ids, contents))
        return accidents, accident_dict
    else:
        accidents2 = []
        ids_2 = []
        contents_2 = []
        with open(ACCIDENT_LOCATION_FILE, 'r') as handler:
            for x in handler:
                x = x.strip('\n').split(';')
                y = x[1].split(',')
                int1 = int(y[0][1:])
                int2 = int(y[1][1:-1])
                accidents2.append([x[0], (int1, int2), int(x[2])])
                ids_2.append(x[0])
                contents_2.append([(int1, int2), int(x[2])])
        accident_dict_2 = dict(zip(ids_2, contents_2))
        return accidents2, accident_dict_2


def veh_location_init():
    veh_id_list = []
    location_reading_list = []
    with open(VEH_LOCATION_FILE, 'r') as handler:
        for x in handler:
            x = x.strip('\n').split(';')
            veh_id_list.append(x[0])
            location_reading_list.append(int(x[1]))
    if DEBUG:
        return veh_id_list, dict(zip(veh_id_list, location_reading_list))
    else:
        start_point = random.choice(range(5, 20))
        tmp_accumulation_spacing = start_point
        veh_location = defaultdict(int)

        for tmp_veh1 in veh_id_list:
            spacing = random.choice(range(5, 100))
            tmp_accumulation_spacing += spacing
            veh_location[tmp_veh1] = tmp_accumulation_spacing
        return veh_id_list, veh_location


def veh_speed_init():
    veh_id_list = []
    speed_reading_list = []
    with open(VEH_SPEED_FILE, 'r') as handler:
        for x in handler:
            x = x.strip('\n').split(';')
            veh_id_list.append(x[0])
            speed_reading_list.append(int(x[1]))
    if DEBUG:
        return dict(zip(veh_id_list, speed_reading_list))
    else:
        veh_speed_init_dict = defaultdict(int)
        for tmp_veh1 in veh_id_list:
            veh_speed_init_dict[tmp_veh1] = random.choice(range(-MAX_SPEED, MAX_SPEED))
        return veh_speed_init_dict


def veh_id_init():
    veh_id_list = []
    with open(VEH_LOCATION_FILE, 'r') as handler:
        for x in handler:
            x = x.strip('\n').split(';')
            veh_id_list.append(x[0])
    return veh_id_list


def bl_address_read(file_address=BLOCKCHAIN_ADDRESS_FILE):
    bl_address_id_list = []
    with open(file_address, 'r') as handler:
        for line in handler:
            line = line.strip('\n').split(';')
            bl_address_id_list.append(line[0])
    return bl_address_id_list


def bl_balance_init(bl_address_init):
    bl_balance_init_dict = defaultdict(int)
    for address1 in bl_address_init:
        bl_balance_init_dict[address1] = random.choice(range(-100, 100))
    return bl_balance_init_dict


def veh_address_allocation(veh_init_ids, bl_address_ids):
    address_veh_dict = defaultdict(str)
    init_balance_address = defaultdict(int)
    bl_address_ids_list = [bl_address_ids[i:i + 3] for i in range(0, len(bl_address_ids), 3)]
    veh_address_dict = dict(zip(veh_init_ids, bl_address_ids_list))
    for ids, address_list in veh_address_dict.items():
        for address in address_list:
            address_veh_dict[address] = ids
            init_balance_address[address] = random.randint(0, 100)
    return veh_address_dict, address_veh_dict, init_balance_address


def bl_operation_init(bl_address_ids):
    bl_operation_init_dict = defaultdict(list)
    for address1 in bl_address_ids:
        # [时间节点之前的请求+响应，时间节点之后的请求+响应]
        bl_operation_init_dict[address1].append([random.choice(range(0, 50)), random.choice(range(0, 50))])
        # [时间节点之前的响应，时间节点之后的响应]
        bl_operation_init_dict[address1].append([random.choice(range(0, 50)), random.choice(range(0, 50))])
    return bl_operation_init_dict


def cache_all_veh_init(veh_ids):
    # 使用车辆而不是钱包，只是为了简化计算，毕竟理论上三个钱包共享内存
    cache_request_veh_dict = defaultdict(list)
    cache_answer_veh_dict = defaultdict(list)
    cache_rating_veh_dict = defaultdict(list)
    return cache_request_veh_dict, cache_answer_veh_dict, cache_rating_veh_dict


def hash_request_msg_init():
    return defaultdict(list)


def hash_answer_msg_init():
    return defaultdict(list)


def hash_rate_msg_init():
    return defaultdict(list)

import json
import sys
import pandas as pd
import math
import uuid
import random
import matplotlib.pyplot as plt
from collections import defaultdict
from utility.simulation_v0.pic_0429 import *
import numpy as np



# http://liyangbit.com/pythonvisualization/matplotlib-top-50-visualizations/

excel_path = '2019-01-04.xlsx'
miles_json_path04 = 'miles_s_m_h_04.json'
miles_json_path04_20 = 'miles_s_m_h_04_20.json'

ditribution_json_path07 = 'picklocation_data_statistics07.json'
ditribution_json_path04 = 'picklocation_data_statistics04.json'
ditribution_json_path02 = 'picklocation_data_statistics02.json'
ditribution_json_path04_20 = 'picklocation_data_statistics04_20.json'

TRANSACTION_MLITIPLE = 3
SYS_L = 1


def defaultdict_dd():
    return defaultdict(int)


def read_miles(excel_path):
    statistics_result = defaultdict(lambda:defaultdict(defaultdict_dd))
    pickup_location = pd.read_excel(excel_path, usecols=[1, 4], header=0)
    pickup_location = pickup_location.values
    for pickup in pickup_location:
        pickup_time = pickup[0]
        miles_ = pickup[1]
        pickup_ = pd.to_datetime((pickup_time))
        hours = pickup_.hour
        minuites = pickup_.minute
        seconds = pickup_.second

        statistics_result[int(hours)][int(minuites)][int(seconds)] += math.ceil(miles_)

    json_str = json.dumps(statistics_result, sort_keys=True, indent=4)
    with open('miles_s_m_h_04.json', 'w') as json_file:
        json_file.write(json_str)


def sort_value_dict(input_dict):
    reversed_dict = {v: k for k, v in input_dict.items()}
    top_elm = sorted(list(reversed_dict.keys()))[0]
    return reversed_dict[top_elm]


class VehicleDatabase:
    def __init__(self, num_vehicle):
        dict_vehicle = defaultdict(int)
        for i in range(num_vehicle):
            vehicle_id = 'vK' + ''.join(str(uuid.uuid4()).split('-'))
            vehicle_weight = random.randint(3, 12)
            dict_vehicle[vehicle_id] = vehicle_weight

        self.vehicle_database = dict_vehicle
        self.dict_active_vehicle = defaultdict(int)

    def get_vehicle(self):
        selected_vehicle_id = random.choice(list(self.vehicle_database))
        if selected_vehicle_id not in self.dict_active_vehicle.keys():
            vehicle_id = selected_vehicle_id
            vehicle_weight = self.vehicle_database[vehicle_id]
            self.active_vehicle_push(vehicle_id, vehicle_weight)
        else:
            vehicle_id = selected_vehicle_id
            vehicle_weight = self.dict_active_vehicle[vehicle_id]
        return {'id': vehicle_id, 'weight': vehicle_weight}

    def vehicle_database_update(self):
        update_ratio = random.uniform(0.05, 0.2)
        update_num = math.ceil(len(self.dict_active_vehicle) * round(update_ratio, 2))
        lst_update_vehicle_id = random.sample(list(self.dict_active_vehicle), update_num)
        update_value = [-2, -1, -1, 1, 1, 2, 2]
        for i in lst_update_vehicle_id:
            self.dict_active_vehicle[i] += random.choice(update_value)

    def active_vehicle_push(self, id, weight):
        self.dict_active_vehicle[id] = weight

    def get_condition(self):
        sum_ = 0
        lst_active_vehicle = list(self.dict_active_vehicle.values())
        if len(lst_active_vehicle) < 15:
            for i in lst_active_vehicle:
                sum_ += i
            return SYS_L * sum_
        else:
            lst_calculating_condition = random.sample(lst_active_vehicle, 15)
            for i in lst_calculating_condition:
                sum_ += i
            # return SYS_L * sum_
            return 3000


class Txn:
    def __init__(self, _hours, _minutes, _seconds, vehicle, num_parent=2):
        self.id = ''.join(str(uuid.uuid4()).split('-'))
        self.timestamp = (_hours*3600) + (int(_minutes) * 60) + int(_seconds) + self._get_ms()  # ms级
        self.vehicle_id = vehicle['id']
        self.weight = vehicle['weight']
        self.ac_weight = vehicle['weight']
        self._num_parent = num_parent
        self.parent_txn = []

    def _get_ms(self):
        f_str = random.uniform(0, 0.9)
        return round(f_str, 1)

    def get_txn_body(self):
        dict_txn_body = {
            'timestamp': self.timestamp,
            'vehicle_id': self.vehicle_id,
            'weight': self.weight,
        }
        return dict_txn_body

    def get_txn(self):
        dict_txn_body = {
            'id': self.id,
            'timestamp': self.timestamp,
            'vehicle_id': self.vehicle_id,
            'weight': self.weight,
        }
        return dict_txn_body

    def select_parent(self, a_txndatabase, input_vehicle_database):
        sorted(a_txndatabase.tail_txn, key=lambda txn: txn.ac_weight)
        num_vehicles = len(input_vehicle_database.dict_active_vehicle)
        consensus_condition = input_vehicle_database.get_condition()
        # if consensus_condition <= 100:
        #     consensus_condition = 100
        lst_confirmed_txn_index = []
        if len(a_txndatabase.tail_txn) > self._num_parent:
            for i in range(self._num_parent):
                selected_txn = self.select_txn_from_tail(a_txndatabase.tail_txn, i)
                is_confrimed = a_txndatabase.txn_consensus(selected_txn, self.ac_weight, self.timestamp,
                                                           i, consensus_condition, num_vehicles)
                self.parent_txn.append(selected_txn)
                if is_confrimed:
                    lst_confirmed_txn_index.append(i)
        else:
            for j in range(len(a_txndatabase.tail_txn)):
                selected_txn = self.select_txn_from_tail(a_txndatabase.tail_txn, j)
                is_confrimed = a_txndatabase.txn_consensus(selected_txn, self.ac_weight, self.timestamp,
                                                           j, consensus_condition, num_vehicles)
                self.parent_txn.append(selected_txn)
                if is_confrimed:
                    lst_confirmed_txn_index.append(j)

        a_txndatabase.del_confrimed_txn_from_tail(lst_confirmed_txn_index)

    def select_txn_from_tail(self, txn_tail, txn_index):
        return txn_tail[txn_index]


class TxnDatabase:
    def __init__(self):
        self.all_txn = defaultdict(Txn)
        self.confirmed_txn = []
        self.tail_txn = []
        self.cache_txn_lst = []
        self.confirmed_txn_stastic = defaultdict(dict)

    def search_txn_from_all(self, input_txn_id):
        return self.all_txn[input_txn_id]

    def txn_into_cache(self, input_txn):
        self.cache_txn_lst.append(input_txn)

    def insert_cache_to_base(self):
        for i in self.cache_txn_lst:
            self.all_txn[i.id] = i
            self.tail_txn.append(i)
        self.clear_cache()

    def clear_cache(self):
        self.cache_txn_lst.clear()

    def txn_consensus(self, _selected_txn, child_weight, child_timestamp, txn_index, consensus_condition, num_vehicles):
        _current_ac_weight = _selected_txn.ac_weight + child_weight
        if _current_ac_weight >= consensus_condition:
            _selected_txn.ac_weight += child_weight
            self.confirmed_txn.append(_selected_txn)
            confirmed_id = _selected_txn.id
            confirm_time_delay = child_timestamp - _selected_txn.timestamp
            self.confirmed_txn_stastic[confirmed_id] = {
                'confirm_time_delay': confirm_time_delay,
                'active_vehicle': num_vehicles,
                'txn_ac_weight': _current_ac_weight,
                'consensus_condition': consensus_condition,
            }
            self.all_txn[_selected_txn.id].ac_weight += child_weight
            return True
        else:
            self.tail_txn[txn_index].ac_weight += child_weight
            self.all_txn[_selected_txn.id].ac_weight += child_weight
            return False

    def del_confrimed_txn_from_tail(self, lst_confirmed_txn):
        for i in lst_confirmed_txn:
            self.tail_txn.pop(0)


def sorded_txn_dict(dict_txn):
    result_txn_dict = sorted(dict_txn, key=lambda Txn: Txn.ac_weight)
    x = result_txn_dict
    return x


def collect_vehicle(file_path, input_hours=18):
    file_handle = read_from_json(file_path)
    sum_int_vehicles = 0
    for vehicles in file_handle[str(input_hours)].values():
        sum_int_vehicles += vehicles
    return sum_int_vehicles


def generate_txn(input_hours, input_minutes, input_seconds, input_miles, input_vk):
    lst_txn = []
    multiple = math.ceil(len(input_vk.dict_active_vehicle)/1000)
    # 设置TPS，强制将TPS设置成10的数量级
    if input_miles < 3300 :
        input_miles = random.randint(3000, 3400)

    if multiple > 1:
        for i in  range(multiple*100):
            new_txn = Txn(input_hours, input_minutes, input_seconds, input_vk.get_vehicle())
            lst_txn.append(new_txn)
    for i in range(input_miles * TRANSACTION_MLITIPLE):
        new_txn = Txn(input_hours, input_minutes, input_seconds, input_vk.get_vehicle())
        lst_txn.append(new_txn)
    result_lst = sorted(lst_txn, key=lambda txn: txn.timestamp)
    return result_lst


def tps_to_confirm_time(input_hours, file_path):
    # num_vehicles = collect_vehicle(ditribution_json_path04, input_hours)
    new_vehicle_database = VehicleDatabase(900)

    txn_database = TxnDatabase()

    ml_04 = read_from_json(miles_json_path04)
    start_time = input_hours * 3600
    tag_num = 0
    for minutes, miles_per_minutes in ml_04[str(input_hours)].items():
        for seconds, miles_per_seconds in miles_per_minutes.items():
            tag_num += 1
            if tag_num < 100:
                lst_transaction_per_seconds = 0
                lst_txn = generate_txn(input_hours, minutes, seconds, miles_per_seconds, new_vehicle_database)
                current_time = (input_hours * 3600) + (int(minutes) * 60)
                int_tag_confirmed_txn = len(txn_database.confirmed_txn)
                for _txn in lst_txn:
                    if _txn.timestamp == current_time and current_time == start_time:
                        current_time = _txn.timestamp
                        txn_database.txn_into_cache(_txn)
                    elif _txn.timestamp == current_time and current_time != start_time:
                        _txn.select_parent(txn_database, new_vehicle_database)
                        txn_database.txn_into_cache(_txn)
                    elif _txn.timestamp > current_time:
                        txn_database.insert_cache_to_base()
                        if len(txn_database.tail_txn):
                            _txn.select_parent(txn_database, new_vehicle_database)
                            txn_database.txn_into_cache(_txn)
                            current_time = _txn.timestamp
                        else:
                            txn_database.txn_into_cache(_txn)
                            current_time = _txn.timestamp
                    else:
                        print("Trasaction time is over the systime time, please check")
                        sys.exit(0)
                    lst_transaction_per_seconds += 1
                print("TPS:", lst_transaction_per_seconds)
                # print("[second]:", seconds, "[active_vehicle]:", len(new_vehicle_database.dict_active_vehicle),
                #       "[raise_txn]:", len(lst_txn), "[raise_confirm]:", len(txn_database.confirmed_txn) - int_tag_confirmed_txn,
                #       "[tail]:", len(txn_database.tail_txn), "[confirmed]:", len(txn_database.confirmed_txn, ),
                #       "[condition]:", new_vehicle_database.get_condition())

                new_vehicle_database.vehicle_database_update()

    json_str = json.dumps(txn_database.confirmed_txn_stastic, indent=4)
    with open(file_path, 'w') as json_file:
        json_file.write(json_str)


def count_res():
    input_fime_path = "TPS=1000.json"
    c_dict = read_from_json(input_fime_path)

    int_num_transaction = 0
    ft_time_delay_sum = 0
    lst_delay = []
    tag_num = 0
    for _id, values in c_dict.items():
        tag_num += 1
        if 10 < tag_num < 80:
            int_num_transaction += 1
            ft_time_delay_sum += round(values["confirm_time_delay"], 1)
            lst_delay.append(round(values["confirm_time_delay"], 1))

    res = round(ft_time_delay_sum / int_num_transaction, 2)


    df = pd.DataFrame(lst_delay)
    df.plot.box(title="TPS=100")
    plt.grid(linestyle="--", alpha=0.3)

    # fig, ax = plt.boxplot(lst_delay)

    plt.show()
    print(df.describe())
    print("***")


if __name__ == "__main__":
    # read_miles(excel_path)
    # b()
    tps_to_confirm_time(8, 'TPS=10000.json')
    # count_res()

    with open('miles_s_m_h_04.json', 'w') as json_file:
        json_file.write((10, res))



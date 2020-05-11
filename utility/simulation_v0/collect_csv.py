import pandas as pd
import json
from collections import defaultdict

excel_path = '2019-01-04_20.xlsx'
excel_path_of_full_file = 'yellow_tripdata_2019-01.csv'


def defaultdict_dd():
    return defaultdict(int)


def pickup_location():
    statistics_result = defaultdict(defaultdict_dd)
    pickup_location = pd.read_excel(excel_path, usecols=[1, 7], header=0)
    pickup_location = pickup_location.values
    for pickup in pickup_location:
        pickup_time = pickup[0]
        pickup_location = pickup[1]
        pickup_ = pd.to_datetime((pickup_time))
        hour = pickup_.hour

        statistics_result[int(hour)][int(pickup_location)] += 1
        # statistics_result[int(hour)]['sum'] += 1
        # statistics_result[int(minute)] += 1



    json_str = json.dumps(statistics_result, indent=4)
    with open('picklocation_data_statistics04_20.json', 'w') as json_file:
        json_file.write(json_str)


def trip_distance():
    statistics_result = defaultdict(defaultdict_dd)
    distance_ = pd.read_excel(excel_path, usecols=[1, 4, 7], header=0)
    distance_ = distance_.values
    for pickup in distance_:
        pickup_ = pickup[0]
        trip_dis = pickup[1]
        location_ = pickup[2]
        pickup_ = pd.to_datetime(pickup_)
        hour = pickup_.hour
        minute = pickup_.minute
        statistics_result[int(hour)][location_] += round(trip_dis,2)
        # statistics_result[int(hour)]['sum'] += 1
        # statistics_result[int(hour)]['distance'] += trip_dis

    json_str = json.dumps(statistics_result, indent=4)
    with open('distance_data_statistics04_20.json', 'w') as json_file:
        json_file.write(json_str)


def extract_date_based():
     pickup_location = pd.read_csv(excel_path_of_full_file, header=0)
     row_num, column_num = pickup_location.shape

     for i in range(0, 10):
         save_data = pickup_location.iloc[i * 200000 + 1:(i + 1) * 200000 + 1, :]  # 每隔20万循环一次
         file_name = '0/' + excel_path + str(i) + '.xlsx'
         save_data.to_excel(file_name, index=False)



if __name__ == "__main__":
    # trip_distance()
    pickup_location()
    # extract_date_based()


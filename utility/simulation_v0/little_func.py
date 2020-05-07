import json
import pandas as pd
import math
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np


import seaborn as sns

# http://liyangbit.com/pythonvisualization/matplotlib-top-50-visualizations/

excel_path = '2019-01-04.xlsx'


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
        pass
        # statistics_result[int(hour)]['sum'] += 1
        # statistics_result[int(minute)] += 1


    json_str = json.dumps(statistics_result, sort_keys=True, indent=4)
    with open('miles_s_m_h_04.json', 'w') as json_file:
        json_file.write(json_str)


def b():



if __name__ == "__main__":
    read_miles(excel_path)
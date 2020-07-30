import pandas as pd
import os
import geohash


path = "./taxi_test" #文件夹目录


def to_split_txt_line(str_list):
    _vehicle_id = int(str_list[0])
    _report_time = str_list[1]
    _latitude = float(str_list[2])
    _longitude = float(str_list[3][:-1])
    return _vehicle_id, _report_time, _latitude, _longitude


def get_filelist(dir):
    Filelist = []
    for home, dirs, files in os.walk(dir):
        for filename in files:
            Filelist.append(os.path.join(home, filename))
            file_name = os.path.join(home, filename)
            f = open(file_name, 'r')
            lines = f.readlines()
            for line in lines:
                str_list = line.split(',')
                vehicle_id, report_time, latitude, longitude = to_split_txt_line(str_list)
                report_time_ = pd.to_datetime(report_time)
                geohash_str = geohash.encode(latitude, longitude)


            print(filename)
            pass

    return Filelist


if __name__ == "__main__":
    filelist = get_filelist(path)
    for i in filelist:
        print(i)

import codecs
import datetime
from datetime import datetime
import json
import math
import numpy as np
import os
from random import random
import pandas as pd
import shutil
import statistics
from statistics import mean
import time


from admin import reset_df
from admin import retrieve_list
from admin import retrieve_path
from admin import retrieve_ref


def main():
    """
    analyze data
    """

    print("running main")

    # build json from csv
    #build_json()

    # create js file
    # sets json equal to a unique variable
    #json_to_js()


    print("completed main")

def build_timestamps(meas, inc):
    """
    return a timestamp list of times
    """
    t_mins = []
    for i in range(len(meas)):
        t = i/inc/60
        t_mins.append(t)

    return(t_mins)


def build_unixstamps(meas, inc, unix_begin):
    """
    return a timestamp list of times
    """
    t_unix = []
    for i in range(len(meas)):
        t = i/inc + float(unix_begin)
        t_unix.append(t)

    return(t_unix)


def build_json():
    """
    create a json file describing each study
    for each study
    find all records, including check if multiple wearable belong to same record
    add wearables to records, finding shared start and end time
    read in csv for each sensor
    """

    for study in retrieve_ref('study_name'):

        print('study = ' + study)

        study_dict = {}
        study_dict['study'] = study
        study_dict['records'] = 0
        study_dict['cumulative time  (hrs)'] = 0

        # create key for the list of records
        study_dict['record'] = []

        # find each folder
        src_dir = os.path.join(retrieve_path('source_data'), study)
        folders = os.listdir(src_dir)[:4]
        record_number = 1
        for folder in folders:
            #print('folder = ' + str(folder))

            # check if the folder was already analyzed
            if check_if_paired(folder, study_dict['record']) == True: continue

            record_folders = find_pairs(folder, folders)
            print('record_folders = ' + str(record_folders))

            # assign a record number
            i = folders.index(folder) + 1
            study_dict['records'] = record_number

            # build record dictionary
            record_dict = {}
            record_dict['record_name'] = str(study + str(i).zfill(record_number))
            record_dict['src_dir'] = src_dir
            record_dict['record_folders'] = record_folders

            unix_begin, unix_end = find_record_time(src_dir, record_folders)
            record_dict['date'] = 0
            record_dict['unix_begin'] = unix_begin
            record_dict['unix_end'] = unix_end
            record_dict['dur_mins'] = (unix_end - unix_begin)/60
            ts = datetime.fromtimestamp(int(unix_begin))
            record_dict['date'] = ts.strftime('%Y-%m-%d %H:%M:%S')

            if float(record_dict['dur_mins']) < 5: continue

            record_number = record_number + 1

            record_dict['wearable'] = []

            # for all folder associated with the record, could be one or two
            for record_folder in record_folders:

                print('record_folder = ' + str(record_folder))
                #wearable_keys = ['unix_begin', 'wearable_id', 'sensors']
                #wearable_dict = dict.fromkeys(wearable_keys, [])
                wearable_dict = {}
                wearable_dict['wearable_id'] = record_folder.split('_')[1]
                wearable_dict['unix_begin'] = record_folder.split('_')[0]

                #wearable_dict['sensors'] = retrieve_ref('sensors')

                for sensor in retrieve_ref('sensors'):

                    src_file = os.path.join(src_dir, folder, sensor + '.csv')

                    t0, dur, inc, meas = parse_records(record_dict, src_file)
                    #t0, dur, inc, meas = parse_source_data(src_file)
                    sensor_dict = {}
                    sensor_dict['sensor_type'] = sensor
                    sensor_dict['sensor_unit'] = retrieve_ref(str(sensor + '_unit'))
                    sensor_dict['sam_freq'] = inc
                    sensor_dict['dur'] = dur
                    sensor_dict['mean'] = statistics.mean(meas)
                    sensor_dict['median'] = statistics.median(meas)
                    sensor_dict['mode'] = statistics.mode(meas)
                    sensor_dict['min'] = min(meas)
                    sensor_dict['max'] = max(meas)
                    sensor_dict['range'] = max(meas)-min(meas)
                    sensor_dict['len'] = len(meas)

                    t_mins = build_timestamps(meas, inc)
                    for p_degree in [0,1,2]:
                        p_degree_label = str('pfit_' + str(p_degree).zfill(2))
                        p_fits = np.polyfit(t_mins,meas,p_degree)

                        sensor_dict[p_degree_label] = []
                        for p_fit in p_fits:
                            sensor_dict[p_degree_label].append(p_fit)

                    sensor_dict['meas'] = meas[:3000]
                    sensor_dict['tmin'] = build_timestamps(sensor_dict['meas'], sensor_dict['sam_freq'])
                    #sensor_dict['tunix'] = build_unixstamps(sensor_dict['meas'], sensor_dict['sam_freq'], sensor_dict['sam_freq'])

                    sensor_dict['color_fill'] = calculate_color_fill(sensor_dict['meas'], record_folders.index(record_folder))

                    print('sensor_dict = ')
                    print(sensor_dict)

                    #wearable_dict['sensors'][sensor] = sensor_dic

                    #print('wearable_dict[sensors][ACC] = ')
                    #print(wearable_dict['sensors']['ACC'])
                    #wearable_dict['sensors'] = 5
                    wearable_dict[sensor] = sensor_dict

                record_dict['wearable'].append(wearable_dict)


            # add the record time
            study_dict['cumulative time  (hrs)'] = 1/60*float(study_dict['cumulative time  (hrs)']) + dur
            study_dict['record'].append(record_dict)


        # save the dictionary as json
        dst_json = os.path.join(retrieve_path('dst_json'), study + '.json')
        with open(dst_json, "w") as fp:
            json.dump(study_dict , fp, indent = 5)


def calculate_color_fill(meas, wearable_num):
    """
    return list of rgb colors in js readable format
    """

    fill_colors = []
    for mea in meas:

        w_index = (mea - min(meas)) / (max(meas) - min(meas))
        assert w_index >= 0 and w_index <= 1

        r = int(255 - 0.5*w_index*255)
        g = int(w_index*255*0.25)
        b = int(w_index*255)


        if wearable_num == 0:
            r = int(w_index*255)
            g = int(255-w_index*255*0.5)
            b = int(255-w_index*255*0.5)


        fill_color = str('rgb(')
        fill_color = str(fill_color +  ' ' + str(r) + ' , ')
        fill_color = str(fill_color +  ' ' + str(g) + ' , ')
        fill_color = str(fill_color +  ' ' + str(b))
        fill_color = str(fill_color +  ' )')
        fill_colors.append(fill_color)

        #print(str(100*float(meas.index(mea))/len(meas)) + '% found ' + 'fill_color = ' + str(fill_color))

    assert len(fill_colors) == len(meas)

    return(fill_colors)


def check_if_paired(folder, records):
    """
    return True if paired
    return False if not
    """

    for record in records:
        record_folders = record['record_folders']
        for record_ref in record['record_folders']:
            if folder in record_ref:
                return(True)


def find_pairs(folder, folders):
    """
    return a list of folders related to a record
    """

    f_index = folders.index(folder)

    unix_begins, wearables = [], []
    for i in range(len(folders)):
        unix_begin = folders[i].split('_')[0]
        wearable = folders[i].split('_')[1]
        unix_begins.append(unix_begin)
        wearables.append(wearable)

    record_folders = [folder]

    for i in range(len(folders)):

            if wearables[i] == wearables[f_index]: continue

            if abs(float(unix_begins[i]) - float(unix_begins[f_index])) > 300: continue

            if len(record_folders) >= 2: continue

            if folder[i] not in record_folders:

                record_folders.append(folders[i])

                # sort the list by wearale id
                df = pd.DataFrame()
                df['record_folders'] = record_folders
                df['unix_begins'] = [unix_begins[f_index], unix_begins[i]]
                df['wearables'] = [wearables[f_index], wearables[i]]
                df = df.sort_values(by='wearables')
                record_folders = list(df['record_folders'])


    return(record_folders)


def find_record_time(src_dir, records):
    """
    return the unix time the record begins and ends
    """

    # find common start point in unix time
    unix_begin = 0
    for record in records:
        if unix_begin < float(record.split('_')[0]):
            unix_begin = float(record.split('_')[0]) + 2


    # find common end point in unix time
    unix_end = int(time.time())
    for record in records:
        print('unix_end = ' + str(unix_end))
        src_file = os.path.join(src_dir, record, 'TEMP' + '.csv')
        unix_t0, dur, inc, meas = parse_source_data(src_file)

        unix_time, mins_time = [], []
        for i in range(len(meas)):
            unix = i/inc + float(unix_t0)
            unix_time.append(unix)
            mins = (i/inc)/60
            mins_time.append(mins)

        if max(unix_time) < unix_end:
            unix_end = max(unix_time) - 2

    return(unix_begin, unix_end)


def json_to_js():
    """
    save a .js
    declares a unique variable
    sets equal to json
    """

    for file in os.listdir(retrieve_path('dst_json')):

        # read in the json
        f_src = os.path.join(retrieve_path('dst_json'), file)
        f = open(f_src, 'r')
        data = json.load(f)
        f.close()

        # identify the filename
        filename = list(file.split('.'))[0]

        # create a .js file that declares
        # a unique variable as the geojson
        file_dst = os.path.join(retrieve_path('dst_js'), filename + '.js')
        with open(file_dst, "w") as f:
            f.write('var ' + filename + ' = ' + '\n')
            json.dump(data, f)
        f.close()

        file_dst = os.path.join(retrieve_path('dst_js'), filename + '.json')
        with open(file_dst, "w") as f:
            json.dump(data, f, indent = 5)
        f.close()


def parse_records(record_dict, src_file):
    """
    if a record has multiple wearables,
    coregister the two datasets to the
    same begin and end point
    """

    unix_t0, dur, inc, meas = parse_source_data(src_file)
    df = pd.DataFrame()
    df['meas'] = meas
    df['mins'] = build_timestamps(meas, inc)
    df['unix'] = build_unixstamps(meas, inc, unix_t0)

    df = df[df['unix'] >= float(record_dict['unix_begin'])]
    df = df[df['unix'] <= float(record_dict['unix_end'])]
    df = df[df['mins'] <= 100]

    return(min(list(df['unix'])), max(list(df['mins'])), inc, list(df['meas']))


def parse_source_data(src_file):
    """
    return metrics in source data
    read in source data
    """

    #print('src_fi = ' + str(src_file))
    src_file_split = src_file.split('/')
    file = src_file_split[-1]
    sensor_type = file.split('.')[0]
    folder = src_file_split[-2]
    t0_unix = folder.split('_')[0]
    wearable_id = folder.split('_')[1]
    #print('sensor_type = ' + str(sensor_type))

    try:
        df = pd.read_csv(src_file)
    except:
        return(' ', ' ', ' ')

    unix_t0 = df.columns[0]
    #print(str(float(t0) - float(t0_unix)))
    #assert float(t0) - float(t0_unix) == 0


    # build measurement and time list
    mea = list(df[unix_t0])[1:]
    meas = mea

    """
    if 'ACC' in sensor_type:
        meas = []
        for i in range(len(mea)):
            me = 0
            for col in df.columns:
                item = list(df[col])[i]
                me = me + math.pow(item,2)
            me = math.sqrt(me)
            meas.append(me)
    """


    inc = list(df[unix_t0])[0]
    dur = round(1/60*len(meas)/inc,4)
    t_mins = build_timestamps(meas, inc)

    # truncate measurements and time
    df_meas = pd.DataFrame()
    df_meas['t_mins'] = t_mins
    df_meas['meas'] = meas
    #df_meas = df_meas[df_meas['t_mins'] <= 70]
    meas = list(df_meas['meas'])
    t_mins = list(df_meas['t_mins'])

    return(unix_t0, dur, inc, meas)


def pair_folders():
    """
    save a df with paired wearable records
    """

    for study in retrieve_ref('study_name'):

        print('study = ' + study)

        unix_begins = []
        wearables = []
        src_fol = os.path.join(retrieve_path('source_data'), study)
        folders = os.listdir(src_fol)
        for folder in folders:

            unix_begins.append(list(folder.split('_'))[0])
            wearables.append(list(folder.split('_'))[1])

        df = pd.DataFrame()

        # list wearables:
        wearable_ids = []
        for wearable in wearables:
            if wearable not in wearable_ids:
                wearable_ids.append(wearable)
                df[wearable] = [0]

        df['unix_begin'] = [0]
        df['unix_end'] = [0]
        df['dur_mins'] = [0]

        df_temp = df
        for i in range(len(unix_begins)):

            for j in range(len(unix_begins)):

                if abs(float(unix_begins[i]) - float(unix_begins[j])) <= 30: continue

                if wearables[i] == wearables[j]: continue

                df_record = df_temp
                df_record.loc[0 , str(wearables[i])] = folders[i]
                df_record.loc[0 , str(wearables[j])] = folders[j]
                unix_begin_max = 5+max([float(unix_begins[i]), float(unix_begins[j])])
                df_record.loc[0,'unix_begin'] = unix_begin_max
                df = df.append(df_record)
                df =df.drop_duplicates(subset=None, keep='first', inplace=False)
                df = reset_df(df)
                continue


        for i in range(len(unix_begins)):

            for wearable_id in wearable_ids:

                if folders[i] not in list(df[wearable_id]):

                    df_record = df_temp
                    df_record.loc[0 , str(wearables[i])] = folders[i]
                    df_record.loc[0 , str(wearables[j])] = folders[j]
                    unix_begin_max = 5+max([float(unix_begins[i]), float(unix_begins[j])])
                    df_record.loc[0,'unix_begin'] = unix_begin_max
                    df = df.append(df_record)
                    df =df.drop_duplicates(subset=None, keep='first', inplace=False)
                    df = reset_df(df)

        #df['paired_records'] = paired_list
        df.to_csv(retrieve_path('paired_records'))



if __name__ == "__main__":
    main()

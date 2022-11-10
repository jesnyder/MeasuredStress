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
from admin import retrieve_df
from admin import retrieve_json
from admin import retrieve_list
from admin import retrieve_path
from admin import retrieve_ref

from build_scatter_record import build_scatter_record



def build_json():
    """
    create a json file describing each study
    for each study
    find all records, including check if multiple wearable belong to same record
    add wearables to records, finding shared start and end time
    read in csv for each sensor
    """

    tasks = [1,2,3,4]

    # count and pair records in the study
    if 1 in tasks: included_records()

    # add data for each included record
    if 2 in tasks: find_data()

    # add statistics
    if 3 in tasks: add_statistics()

    # summarize statistics
    if 4 in tasks: summarize_statistics()


def summarize_statistics():
    """
    summarize statistics
    """

    # for each study
    for study in retrieve_ref('study_types'):

        # find the rough json
        fol_src = retrieve_path('dst_json')
        for fil in os.listdir(fol_src):

            # skip if the json does not match study or rough
            #print('fil = ' + str(fil))
            if str(study) not in str(fil): continue
            if 'data' not in str(fil): continue

            fil_src = os.path.join(fol_src, fil)
            json_src = retrieve_json(fil_src)
            study_json = json_src

            study_json['stats'] = {}

            for sensor in json_src['records'][0]['stats'].keys():

                study_json['stats'][sensor] = {}
                for stat in  json_src['records'][0]['stats'][sensor].keys():

                    if 'quantiles' in str(stat): continue

                    values = []
                    for record in json_src['records']:

                        value = record['stats'][sensor][stat]
                        values.append(value)

                    value = sum(values)/len(values)
                    if 'min' == str(stat): value = min(values)
                    if 'max' == str(stat): value = max(values)
                    study_json['stats'][sensor][stat] = value

            # save the dictionary as json
            fil_dst = os.path.join(retrieve_path('dst_json'), study + '_data' + '.json')
            #print('fil_dst = ' + str(fil_dst))
            with open(fil_dst, "w") as fp:
                json.dump(study_json, fp, indent = 8)
            fp.close()


def add_statistics():
    """
    add statistics to json
    """

    # for each study
    for study in retrieve_ref('study_types'):

        # find the rough json
        fol_src = retrieve_path('dst_json')
        for fil in os.listdir(fol_src):

            # skip if the json does not match study or rough
            #print('fil = ' + str(fil))
            if str(study) not in str(fil): continue
            if 'data' not in str(fil): continue

            fil_src = os.path.join(fol_src, fil)
            json_src = retrieve_json(fil_src)
            study_json = json_src

            for record in json_src['records']:

                i = list(json_src['records']).index(record)

                stats = {}
                polyfit = {}
                for key in record['sensor'].keys():

                    sensor = key

                    for wearable in record['sensor'][sensor]:

                        #print('fil_src = ')
                        #print(wearable['fil_src'])

                        #print('wearable.keys() = ')
                        #print(wearable.keys())
                        fil_src = wearable['meas']

                        #print(retrieve_meas(fil_src))
                        meas = list(retrieve_meas(fil_src)['meas'])
                        tmin = list(retrieve_meas(fil_src)['tmins'])

                        stats_key = {}
                        stats_key['mean'] = mean(meas)
                        stats_key['fmean'] = statistics.fmean(meas)
                        stats_key['median'] = statistics.median(meas)
                        stats_key['mode'] = statistics.mode(meas)
                        stats_key['quantiles'] = statistics.quantiles(meas)
                        stats_key['pstdev'] = statistics.pstdev(meas)
                        stats_key['pvariance'] = statistics.pvariance(meas)
                        stats_key['stdev'] = statistics.stdev(meas)
                        stats_key['max'] = max(meas)
                        stats_key['min'] = min(meas)
                        stats[key] = stats_key


                        polyfit[sensor] = []
                        polyfits = []
                        for ii in [0, 1, 2, 3]:

                            z = list(np.polyfit(tmin, meas, ii))
                            polyfits.append(z)

                        polyfit[sensor] = polyfits

                #print('polyfit = ')
                #print(polyfit)

                study_json['records'][i]['stats'] = stats
                study_json['records'][i]['polyfit'] = polyfit

        # save the dictionary as json
        fil_dst = os.path.join(retrieve_path('dst_json'), study + '_data' + '.json')
        #print('fil_dst = ' + str(fil_dst))
        with open(fil_dst, "w") as fp:
            json.dump(study_json, fp, indent = 8)
        fp.close()


def retrieve_meas(fil_src):
    """
    return a json file of saved data
    """
    #print('fil_src = ' + str(fil_src))
    df = retrieve_df(fil_src)
    data = {}
    data['meas'] = list(df['meas'])
    data['tmins'] = list(df['tmins'])
    data['tunix'] = list(df['tunix'])
    #print('data = ')
    #print(data)
    return(data)


def find_data():
    """
    save dictionary/json with data
    building on the included record
    """

    # for each study
    for study in retrieve_ref('study_types'):

        # find the rough json
        fol_src = retrieve_path('dst_json')
        for fil in os.listdir(fol_src):

            # skip if the json does not match study or rough
            #print('fil = ' + str(fil))
            if str(study) not in str(fil): continue
            if 'rough' not in str(fil): continue

            fil_src = os.path.join(fol_src, fil)
            json_src = retrieve_json(fil_src)
            study_json = json_src

            for record in json_src['records']:

                print(str(fil) + ' ' + str(list(json_src['records']).index(record)) + ' file of ' +  str(len(list(json_src['records']))))

                #print('record = ')
                #print(record)
                i = list(study_json['records']).index(record)

                for key in record['sensor']:

                    for wearable in record['sensor'][key]:

                        j = list(record['sensor'][key]).index(wearable)
                        data_simple = format_src_data(wearable['fil_src'])

                        df_info = {}
                        df_info['record_name'] = record['name']
                        df_info['wearable_name'] = wearable['wearable_name']
                        df_info['sensor'] = key
                        df_info['record_begin'] = record['record_begin']
                        df_info['record_end'] = record['record_end']
                        df_info['fil_src'] = wearable['fil_src']
                        data_simple = df_src_data(df_info)

                        for key_data in data_simple:
                            study_json['records'][i]['sensor'][key][j][key_data] = data_simple[key_data]


        # save the dictionary as json
        fil_dst = os.path.join(retrieve_path('dst_json'), study + '_data' + '.json')
        #print('fil_dst = ' + str(fil_dst))
        with open(fil_dst, "w") as fp:
            json.dump(study_json, fp, indent = 8)


def df_src_data(df_info):
    """
    save the measurements to dataframes
    to be able to load the comprehensive json faster
    """

    fil_src = df_info['fil_src']
    meas_src = format_src_data(fil_src)
    #print(fil_src)
    #print(meas_src.keys())

    if 'meas' not in meas_src.keys(): return(meas_src)

    df = pd.DataFrame()
    df['meas'] = meas_src['meas']
    df['tmins'] =  meas_src['tmins']
    df['tunix'] =  meas_src['tunix']

    # limit the dataframe to the record begin and end
    df = df[df['tunix'] >= df_info['record_begin']]
    df = df[df['tunix'] <= df_info['record_end']]

    # reset the tmins
    tmins = []
    for i in range(len(df['meas'])):

        tmin = i*1/meas_src['freq']/60
        tmins.append(tmin)

    df['tmins'] = tmins

    filename = str(df_info['record_name'] + '_' + df_info['wearable_name'] + '_' + df_info['sensor'] + '.csv')
    df_fol_dst = os.path.join(retrieve_path('dst_df_data'), df_info['record_name'])
    if os.path.exists(df_fol_dst) == False: os.mkdir(df_fol_dst)
    df_fil_dst = os.path.join(df_fol_dst, filename)
    df.to_csv(df_fil_dst)

    meas_src['meas'] = df_fil_dst
    meas_src['tmins'] = df_fil_dst
    meas_src['tunix'] = df_fil_dst

    return(meas_src)


def format_src_data(fil_src):
    """
    return data
    """

    #print('fil_src = ' + str(fil_src))

    if str('.txt') in str(fil_src[-5:]): return({})
    if 'IBI' in str(fil_src[-7:]): return({})
    #if 'BVP' in str(fil_src[-7:]): return({})
    #if 'ACC' in str(fil_src[-7:]): return({})

    df = retrieve_df(fil_src)
    #print('df = ')
    #print(df)

    # handle tags
    if str('tags.csv') in str(fil_src):
        meas_src = {}
        meas_src['tmins'] = df.columns[0]
        meas_src['tunix'] = df.columns[0]
        return(meas_src)

    begin_unix = df.columns[0]
    freq = df[begin_unix][0]
    inc = 1/freq
    meas_found = list(df[begin_unix][1:])
    begin_unix = int(float(begin_unix))

    #print('begin_unix  = ' + str(begin_unix ))

    meas, tmins, tunixs = [], [], []
    for mea in meas_found:

        i = len(tmins)
        tmin = i*inc/60
        tunix = i*inc + begin_unix

        if tmin > 50: break

        tmins.append(tmin)
        tunixs.append(tunix)
        meas.append(mea)

    #print('begin_unix = ' + str(begin_unix))
    #print('max(tunixs) = ')
    #print(max(tunixs))
    assert begin_unix <= max(tunixs)

    meas_src = {}
    meas_src['begin_unix'] = begin_unix
    meas_src['end_unix'] = max(tunixs)
    meas_src['dur'] = max(tmins)
    meas_src['freq'] = freq
    meas_src['inc'] = inc
    meas_src['tmins'] = tmins
    meas_src['tunix'] = tunixs
    meas_src['meas'] = meas

    #meas_src['max'] = max(meas)
    #meas_src['min'] = min(meas)
    #meas_src['avg'] = sum(meas)/len(meas)
    return(meas_src)


def included_records():
    """
    save a dictionary/json file of included records
    must be longer than 8 minutes
    check if there is a pair
    """

    # for each study
    for study_type in retrieve_ref('study_types'):

        # create empty lists
        matched_fol = []
        records = []
        i = 0
        dur = 0

        # establish study json
        #print('study_type = ' + study_type)
        study_json = {}
        study_json['record_count'] = 0
        study_json['record_duration'] = dur
        study_json['records'] = records

        # list the folders found in the study_type folder
        rec_src = os.path.join(retrieve_path('src_csv'), study_type)
        for fol in os.listdir(rec_src):

            if fol in matched_fol: continue

            fol_names = [fol]
            fol_srcs = [os.path.join(rec_src, fol)]
            matched_fol.append(fol)

            fol_match = fol_matched(rec_src, fol)
            if fol_match != False and study_type != 'HI':
                fol_names.append(fol_match)
                fol_srcs.append(os.path.join(rec_src, fol_match))
                matched_fol.append(fol_match)

            # check that the record is at least 8 minutes
            # before including in compiled
            record_unix = find_record_unix(fol_srcs)
            if record_unix['duration'] < 8: continue

            record = {}
            i = i + 1
            record['name'] = str(study_type) + '_' + str(i).zfill(3)
            fol_src = os.path.join(rec_src, fol)
            record['fol_names'] = fol_names
            record['fol_srcs'] = fol_srcs

            record['record_begin'] = record_unix['unix_begin']
            record['record_end'] = record_unix['unix_end']
            record['record_duration'] = record_unix['duration']
            record['sensor'] = {}

            # add empty list for each file
            for fil in os.listdir(os.path.join(rec_src, fol)):

                sensor = fil.split('.')[0]

                if sensor == '': continue
                if sensor == 'ACC': continue
                if sensor == 'BVP': continue
                if sensor == 'IBI': continue
                if sensor == 'tags': continue
                if sensor == 'info': continue

                wearables = []
                for  fol_src in  fol_srcs:

                    wearable = {}
                    wearable['wearable_name'] = str((fol_src.split('/')[-1])).split('_')[-1]
                    wearable['wearable_begin'] = str((fol_src.split('/')[-1])).split('_')[0]
                    wearable['fil_src'] = os.path.join(fol_src, fil)
                    wearables.append(wearable)

                record['sensor'][sensor] = wearables

            for fil in os.listdir(fol_src):

                fil_src = os.path.join(fol_src, fil)
                #print('fil_src = ' + fil_src)

            records.append(record)
            dur = dur + (record['record_duration'])/60

        study_json['record_count'] = len(records)
        study_json['record_duration'] = dur
        study_json['records'] = records

        # save the dictionary as json
        fil_dst = os.path.join(retrieve_path('dst_json'), study_type + '_rough' + '.json')
        #print('fil_dst = ' + str(fil_dst))
        with open(fil_dst, "w") as fp:
            json.dump(study_json, fp, indent = 5)


def find_record_unix(fol_srcs):
    """
    return the initial and final unix timestamps
    and duration in minutes
    """


    begins, ends = [], []

    for fol in fol_srcs:

        fil_src = os.path.join(fol, 'TEMP.csv')
        meas_src = format_src_data(fil_src)

        begins.append(meas_src['begin_unix'])
        ends.append(meas_src['end_unix'])

        # check for a temp drop
        ends.append(check_temp_drop(meas_src))


    begin = int(max(begins) + 1)
    end = int(min(ends) - 5)

    assert begin > 0
    assert begin < end
    assert end < 1667947758*2

    record_unix = {}
    record_unix['unix_begin'] = begin
    record_unix['unix_end'] = end
    record_unix['duration'] = (end-begin)/60

    return(record_unix)


def check_temp_drop(meas_src):
    """
    check for a temp drop
    """

    meas = meas_src['meas']

    for i in range(len(meas)):

        if i + 22 > len(meas): continue

        # check for temp drop
        if meas[i] > meas[i+3] + 1:
            if meas[i] > meas[i+10] + 2:
                if meas[i] > meas[i+20] + 5:
                    time_end = float(meas_src['tunix'][i])
                    print('time_end found: ' + str(time_end))
                    return(time_end)

    return(1667947758*2)


def fol_matched(rec_src, fol_src):
    """
    check if the record has a match
    if so, return the fol_src of the match
    """

    begin_found = int(fol_src.split('_')[0])

    for fol in os.listdir(rec_src):

        if fol == fol_src: continue
        begin_ref = int(fol.split('_')[0])

        if abs(begin_found - begin_ref) > 250: continue

        return(fol)

    return(False)

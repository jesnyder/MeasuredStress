import csv
import codecs
import datetime
from datetime import datetime
import json
import math
import matplotlib
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import os
from random import random
import pandas as pd
import plotly
from plotly.tools import FigureFactory as ff
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


def build_scatter_record():
    """
    build a scatter plot for each record
    """

    print("begin build_scatter_record")

    tasks = [1, 2, 3]
    if 1 in tasks: write_scatter_js()
    if 2 in tasks: write_scatter_js_comparison()
    if 2 in tasks: write_scatter_html()

    print("completed build_scatter_record")


def write_scatter_html():
    """
    write html to run scatters
    """


    print("begin write_scatter_html")

    for study in retrieve_ref('study_types'):

        fil_dst = os.path.join(os.path.join('docs', 'data', study, 'html_temp' + '.html'))

        with open(fil_dst, "w") as f:

            study_src = os.path.join('docs', 'data', study, 'js')
            for fol in os.listdir(study_src):

                if '.js' in fol: continue

                fol_src = os.path.join('docs', 'data', study, 'js', fol)
                for fil in os.listdir(fol_src):

                    fil_src = os.path.join('js', fol, fil)

                    plot_name = fil.split('.')[0]

                    f.write('<br>' + '\n')
                    f.write('<div id="' + str(plot_name) + '"')
                    f.write('style="text-align:center; width:80%; margin-left: 10%; max-width:800px;">' + '\n')
                    f.write('<script src="' + fil_src + '"></script>' + '\n')
                    f.write('</div>' + '\n')
                    f.write('\n')

        f.close()

    print("completed write_scatter_html")


def write_scatter_js():
    """
    write js for each record for each sensor
    """
    # for each study type, either PMR or HI
    for study_type in retrieve_ref('study_types'):

        #print('study_type = ' + str(study_type))

        src_path = retrieve_path('json_compiled')
        for fil in os.listdir(src_path):

            if 'data' not in str(fil): continue

            if str(study_type) not in str(fil): continue

            json_src = retrieve_json(os.path.join(src_path, fil))

            for record in json_src['records'][:10]:

                print(str(study_type) + ' ' + str(list(json_src['records']).index(record)) + ' file of ' +  str(len(list(json_src['records']))))

                bubble_data = []

                for key in record['sensor'].keys():

                    sensor = key

                    for wearable in record['sensor'][key]:

                        build_color_info = {}
                        build_color_info['wearable_num'] = list(record['sensor'][key]).index(wearable)+1
                        build_color_info['wearable_count'] = len(list(record['sensor'][key]))
                        build_color_info['sensor'] = sensor


                        wearable_name = wearable['wearable_name']

                        if 'tmins' not in wearable.keys(): continue
                        if 'meas' not in wearable.keys(): continue

                        #print(wearable.keys())

                        trace = {}
                        data_src = str(wearable['tmins'])
                        #print('data_src = ')
                        #print(data_src)
                        trace['x'] = list(retrieve_df(data_src)['tmins'])
                        trace['y'] = list(retrieve_df(data_src)['meas'])
                        trace['name'] = sensor + ' ' +  str(wearable_name)
                        #trace['text'] = []
                        if 'HR' in str(sensor): trace['yaxis'] = 'y2'
                        if 'TEMP' in str(sensor): trace['yaxis'] = 'y3'
                        #if 'TEMP' in str(sensor): trace['yaxis'] = 'y4'
                        trace['mode'] = 'markers'
                        trace['marker'] = build_markers(trace, build_color_info)
                        bubble_data.append(trace)


                # write bubble chart layout
                # https://plotly.com/javascript/bubble-charts/
                desc_title = study_type + ' ' + record['name'] + ' ' +  sensor + '_' + str(wearable_name)
                desc_plotname = desc_title.replace(' ', '_')

                bubble_layout = {}
                bubble_layout['title'] = desc_title
                bubble_layout['showlegend'] = True
                bubble_layout['yaxis'] = { 'title': 'EDA (microsiemens)', 'titlefont': {'color': 'rgb(255, 70, 30)'}, 'tickfont': {'color': 'rgb(255, 70, 30)'} , 'showgrid': False, 'side': 'left', 'position': 0}

                bubble_layout['yaxis2'] =  {'title': 'HR (Hz)', 'showgrid': False, 'titlefont': {'color': 'rgb(30, 255, 70)'}, 'tickfont': {'color': 'rgb(30, 255, 70)'}, 'anchor': 'free', 'overlaying': 'y', 'side': 'right', 'position': 0.85}
                bubble_layout['yaxis3'] =  {'title': 'TEMP (°C)', 'range': [30, 39], 'showgrid': False, 'titlefont': {'color': 'rgb(70, 30, 255)'}, 'tickfont': {'color': 'rgb(70, 30, 255)'}, 'anchor': 'free', 'overlaying': 'y', 'side': 'right', 'position': 0.95}

                #bubble_layout['yaxis4'] =  {'title': 'yaxis4 title', 'titlefont': {'color': 'rgb(148, 103, 189)'}, 'tickfont': {'color': 'rgb(148, 103, 189)'}, 'anchor': 'free', 'overlaying': 'y', 'side': 'left', 'position': -0.3 }

                bubble_layout['xaxis'] = { 'title': 'Time (mins)', 'domain': [0, 0.85]}
                bubble_layout['height'] = 700
                bubble_layout['width'] = 1000

                fol_dst = os.path.join('docs', 'data', study_type)
                if os.path.exists(fol_dst) == False: os.mkdir(fol_dst)
                fol_dst = os.path.join('docs', 'data', study_type, 'js')
                if os.path.exists(fol_dst) == False: os.mkdir(fol_dst)
                fol_dst = os.path.join('docs', 'data', study_type, 'js', record['name'])
                if os.path.exists(fol_dst) == False: os.mkdir(fol_dst)

                fil_dst = os.path.join(fol_dst, desc_plotname + '.js' )
                with open(fil_dst, "w") as f:
                    f.write('Plotly.newPlot( "' + desc_plotname + '" , '+ '\n')
                    json.dump(bubble_data, f, indent = 4)
                    f.write(', ' + '\n')
                    json.dump(bubble_layout, f, indent = 4)
                    f.write(');')
                f.close()


def write_scatter_js_comparison():
    """
    write js for each record for each sensor
    """
    # for each study type, either PMR or HI
    for study_type in retrieve_ref('study_types'):

        #print('study_type = ' + str(study_type))

        src_path = retrieve_path('json_compiled')
        for fil in os.listdir(src_path):

            if 'data' not in str(fil): continue

            if str(study_type) not in str(fil): continue

            json_src = retrieve_json(os.path.join(src_path, fil))

            for record in json_src['records'][:10]:

                print(str(study_type) + ' ' + str(list(json_src['records']).index(record)) + ' file of ' +  str(len(list(json_src['records']))))

                for key in record['sensor']:

                    sensor1 = key
                    i1 = list(record['sensor']).index(key)

                    for key2 in record['sensor']:

                        sensor2 = key2
                        i2 = list(record['sensor']).index(key2)

                        if sensor1 == sensor2: continue
                        if i2 <= i1: continue

                        bubble_data = []
                        record_1 = record['sensor'][sensor1]
                        record_2 = record['sensor'][sensor2 ]

                        for i in range(len(record['sensor'][sensor1])):

                            trace = {}

                            wearable = record['sensor'][sensor1][i]
                            wearable_name = wearable['wearable_name']
                            data_src = str(wearable['tmins'])
                            trace['x'] = list(retrieve_df(data_src)['meas'])
                            wearable = record['sensor'][sensor2][i]
                            data_src = str(wearable['tmins'])
                            trace['y'] = list(retrieve_df(data_src)['meas'])
                            trace['name'] = sensor1 + ' vs ' + sensor2 + ' ' + str(wearable_name)


                            build_color_info_compare = {}
                            build_color_info_compare['sensor1'] = sensor1
                            build_color_info_compare['sensor2'] = sensor2
                            build_color_info_compare['x'] = trace['x']
                            build_color_info_compare['y'] = trace['y']
                            trace['mode'] = 'markers'
                            trace['marker'] = build_markers_compare(trace, build_color_info_compare)

                            bubble_data.append(trace)

                        # write bubble chart layout
                        # https://plotly.com/javascript/bubble-charts/
                        desc_title = study_type + ' ' + record['name'] + ' ' +  sensor1 + ' vs' + sensor2
                        desc_plotname = desc_title.replace(' ', '_')

                        bubble_layout = {}
                        bubble_layout['title'] = desc_title
                        bubble_layout['showlegend'] = True
                        bubble_layout['yaxis'] = { 'title': sensor2, 'titlefont': {'color': 'rgb(0, 0, 0)'}, 'tickfont': {'color': 'rgb(0, 0, 0)'} , 'showgrid': True, 'side': 'left', 'position': 0}

                        bubble_layout['xaxis'] = { 'title': sensor1, 'domain': [0, 1], 'showgrid': True}
                        bubble_layout['height'] = 600
                        bubble_layout['width'] = 900

                        fol_dst = os.path.join('docs', 'data', study_type)
                        if os.path.exists(fol_dst) == False: os.mkdir(fol_dst)
                        fol_dst = os.path.join('docs', 'data', study_type, 'js')
                        if os.path.exists(fol_dst) == False: os.mkdir(fol_dst)
                        fol_dst = os.path.join('docs', 'data', study_type, 'js', record['name'])
                        if os.path.exists(fol_dst) == False: os.mkdir(fol_dst)

                        fil_dst = os.path.join(fol_dst, desc_plotname + '.js' )
                        with open(fil_dst, "w") as f:
                            f.write('Plotly.newPlot( "' + desc_plotname + '" , '+ '\n')
                            json.dump(bubble_data, f, indent = 4)
                            f.write(', ' + '\n')
                            json.dump(bubble_layout, f, indent = 4)
                            f.write(');')
                            f.write(', ' + '\n')
                            f.write(', ' + '\n')
                            f.write('Plotly.moveTraces("' + desc_plotname + '", [0, 1, 2],[2, 0, 1]);')
                            f.write(', ' + '\n')
                            f.write(', ' + '\n')
                        f.close()


def build_markers_compare(trace, build_color_info):
    """
    return marker json
    """

    print('build_color_info.keys() = ')
    print(build_color_info.keys())

    colors, opacities, sizes = [], [], []
    for i in range(len(build_color_info['y'])):

        color = scatter_plotly_color_compare(build_color_info, i)
        colors.append(color)
        opacities.append(0.8)

        size = 30
        sizes.append(size)

    marker = {}
    marker['color'] = colors
    #marker['opacity'] =opacities
    marker['size'] = sizes
    marker['sizemode'] = 'area'
    marker['line'] = {'color': 'rgb(231, 99, 250)', 'width': 0}

    # https://plotly.com/javascript/bubble-charts/
    # ['circle', 'square', 'diamond', 'cross']
    marker['symbol'] = ['circle']*len(sizes)

    """
    if build_color_info['wearable_num'] == 2:
        if build_color_info['wearable_count'] == 2:
            marker['symbol'] = ['diamond']*len(sizes)
    """

    return(marker)


def build_markers(ref, build_color_info):
    """
    return json describing markers
    formatted for plotly
    ref:
    https://plotly.com/javascript/bubble-charts/
    """

    colors, opacities, sizes = [], [], []
    for i in range(len(ref['x'])):

        color = scatter_plotly_color(ref['y'][i], ref['y'], build_color_info)
        colors.append(color)
        opacities.append(0.8)

        size = 30
        sizes.append(size)

    marker = {}
    marker['color'] = colors
    #marker['opacity'] =opacities
    marker['size'] = sizes
    marker['sizemode'] = 'area'
    marker['line'] = {'color': 'rgb(231, 99, 250)', 'width': 0}

    # https://plotly.com/javascript/bubble-charts/
    # ['circle', 'square', 'diamond', 'cross']
    marker['symbol'] = ['circle']*len(sizes)

    """
    if build_color_info['wearable_num'] == 2:
        if build_color_info['wearable_count'] == 2:
            marker['symbol'] = ['diamond']*len(sizes)
    """
    return(marker)


def scatter_plotly_color_compare(build_color_info, i):
    """
    assign a color based on slope
    """

    values = list(build_color_info['x'])

    #print('build_color_info[\'sensor\'] = ')
    #print(build_color_info['sensor'])
    #print('build_color_info.keys() = ')
    #print(build_color_info.keys())
    #i = i -1
    #print('i = ' + str(i))
    #print('len(build_color_info[\'x\']) = ')
    #print(len(build_color_info['x']))



    values = build_color_info['y']
    value = values[i]
    value_max = max(values)
    value_min = min(values)
    value_avg = sum(values)/len(values)
    inc2 = (value_max - value)/(value_max - value_min)
    if inc2 > 1: inc2 = 1
    if inc2 < 0: inc2 = 0
    inc2 = 255*inc2


    inc1 = (len(build_color_info['y']) - i)/(len(build_color_info['y']))
    if inc1 > 1: inc1 = 1
    if inc1 < 0: inc1 = 0
    inc1 = 255*inc1

    #print('build_color_info = ')
    #print(build_color_info)
    mods = [1, 0.5, 0.8]
    r = int(255 - inc1*mods[0])
    g = int(inc1*mods[1])
    b = int(inc1*mods[2])

    #print('sensor1 =' + str(build_color_info['sensor1']))
    #print('sensor2 =' + str(build_color_info['sensor2']))

    if str('EDA') in str(build_color_info['sensor1']):
        if str('HR') in str(build_color_info['sensor2']):
            mods = [1, 0, 1]
            r = int(255 - inc1*mods[0])
            g = int(50)
            b = int(inc2*mods[2])

    elif str('EDA') in str(build_color_info['sensor1']):
        if str('TEMP') in str(build_color_info['sensor2']):
            mods = [0, 1, 1]
            r = int(50)
            g = int(inc1*mods[1])
            b = int(255 - inc1*mods[0])


    elif str('HR') in str(build_color_info['sensor1']):
        if str('TEMP') in str(build_color_info['sensor2']):
            mods = [1, 1, 1]
            r = int(inc1*mods[0])
            g = int(255 - inc2*mods[0])
            b = int(50)


    color_str = str('rgb( ' + str(r) + ' , ' +  str(g) + ' , ' + str(b) + ' )')
    #print('color_str = ' + str(color_str))
    return(color_str)


def scatter_plotly_color(value, values, build_color_info):
    """
    assign a color based on slope
    """

    #print('build_color_info[\'sensor\'] = ')
    #print(build_color_info['sensor'])

    value_max = max(values)
    value_min = min(values)
    value_avg = sum(values)/len(values)

    inc = (value_max - value)/(value_max - value_min)
    if inc > 1: inc = 1
    if inc < 0: inc = 0

    inc = 255*inc

    mods = [0.5, 1, 0.5]
    r = int(0   + inc*mods[0])
    g = int(255 - inc*mods[1])
    b = int(255 - inc*mods[2])

    if  str('EDA') in str(build_color_info['sensor']):
        #print('EDA found')
        mods = [0, 0.95, 0.5]
        r = int(255 - inc*mods[0])
        g = int(0   + inc*mods[1])
        b = int(0   + inc*mods[2])

        if build_color_info['wearable_num'] > 1:
            if build_color_info['wearable_count'] > 1:
                mods = [0, 0.8, 0.8]
                r = int(255 - inc*mods[0])
                g = int(0   + inc*mods[1])
                b = int(0   + inc*mods[2])

    elif  str('HR') in str(build_color_info['sensor']):
        #print('HR found')
        mods = [0.5, 0, 0.95]
        r = int(0   + inc*mods[0])
        g = int(255 - inc*mods[1])
        b = int(0   + inc*mods[2])

        if build_color_info['wearable_num'] > 1:
            if build_color_info['wearable_count'] > 1:
                mods = [0.8, 0, 0.8]
                r = int(255 - inc*mods[0])
                g = int(0   + inc*mods[1])
                b = int(0   + inc*mods[2])


    elif str('TEMP') in str(build_color_info['sensor']):
        #print('TEMP found')
        mods = [0.95, 0.5, 0]
        r = int(0   + inc*mods[0])
        g = int(0   + inc*mods[1])
        b = int(255 - inc*mods[2])

        if build_color_info['wearable_num'] > 1:
            if build_color_info['wearable_count'] > 1:
                mods = [0.8, 0.8, 0]
                r = int(255 - inc*mods[0])
                g = int(0   + inc*mods[1])
                b = int(0   + inc*mods[2])

    else:
        #print('else found')
        mods = [0.75, 0.75, 0.75]
        r = int(255 - inc*mods[0])
        g = int(255 - inc*mods[1])
        b = int(255 - inc*mods[2])

    """
    if build_color_info['wearable_num'] > 1:
        if build_color_info['wearable_count'] > 1:
            mods = [1, 0.25, 0.25]
            r = int(255 - inc*mods[0])
            g = int(0   + inc*mods[1])
            b = int(0   + inc*mods[2])
    """

    color_str = str('rgb( ' + str(r) + ' , ' +  str(g) + ' , ' + str(b) + ' )')
    #print('color_str = ' + str(color_str))
    return(color_str)

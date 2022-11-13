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


def build_plotly():
    """
    build a scatter plot for each record
    """

    print("begin plotly")

    tasks = [1, 2, 3]
    if 1 in tasks: each_record_each_sensor_scatter()


    print("completed build_plotly")



def each_record_each_sensor_scatter():
    """
    save a .js file to build a scatter plot using plotly
    save a separate file for each sensor of each record
    """

    for fol in os.listdir(retrieve_path('dst_json')):

        if 'data' not in str(fol): continue
        study = fol.split('_')[0]

        records_json = retrieve_json(os.path.join(retrieve_path('dst_json'), fol))
        for record in records_json['records']:

            for key in record['sensor'].keys():

                sensor = record['sensor'][key]

                layout_type = 'scatter'
                figure_name = 'test_' + layout_type + '_' + study + '_' + record['name'] + '_' + key

                temps = []
                for wearable in sensor:


                    plot_name = figure_name + '_' + wearable['wearable_name']

                    temp = wearable
                    temp['sensor'] = key
                    temp['file_name'] = figure_name
                    temp['figure_name'] = figure_name
                    temp['plot_type'] = 'each_record_each_sensor_scatter'
                    temp['study'] = study
                    temp['plot_name'] = plot_name
                    temp['plot_title'] = str(figure_name).replace('_', ' ')
                    temp['layout_mode'] = 'markers'
                    temp['layout_type'] = 'scatter'
                    temp['name'] = record['name']
                    temp['x_label'] = 'Time (minutes)'
                    temp['y_label'] = key
                    temp['x'] = list(retrieve_df(str(wearable['tmins']))['tmins'])
                    temp['y'] = list(retrieve_df(str(wearable['meas']))['meas'])

                    # assign colors
                    if 'EDA' in key: temp['color_type'] = 'reds'
                    if 'HR' in key: temp['color_type'] = 'greens'
                    if 'TEMP' in key: temp['color_type'] = 'blues'

                    temps.append(temp)

                ref_json = temps
                data = write_data(ref_json)
                layout = write_layout(ref_json)

                save_json = {}
                save_json['study'] = study
                save_json['data'] = data
                save_json['layout'] = layout
                save_json['record_name'] = record['name']
                save_json['figure_name'] = figure_name
                save_plotly_js(save_json)


def save_plotly_js(save_json):
    """
    save plotly js
    """

    fol_dst = os.path.join('docs', 'data', save_json['study'])
    if os.path.exists(fol_dst) == False: os.mkdir(fol_dst)
    fol_dst = os.path.join('docs', 'data', save_json['study'], 'js')
    if os.path.exists(fol_dst) == False: os.mkdir(fol_dst)
    fol_dst = os.path.join('docs', 'data', save_json['study'], 'js', save_json['record_name'])
    if os.path.exists(fol_dst) == False: os.mkdir(fol_dst)

    fil_dst = os.path.join(fol_dst, save_json['figure_name'] + '.js' )
    with open(fil_dst, "w") as f:
        f.write('Plotly.newPlot( "' + save_json['figure_name'] + '" , '+ '\n')
        json.dump(save_json['data'], f, indent = 4)
        f.write(', ' + '\n')
        json.dump(save_json['layout'], f, indent = 4)
        f.write(');')
        f.close()

    print(fil_dst)


def make_marker(marker_json):
    """
    return json describin marker
    """

    markers = {}
    markers['color'] = make_color(marker_json)
    markers['size'] = 12
    markers['size_mode'] = 'area'
    markers['line'] = {"color": "rgb(231, 99, 250)", "width": 0}
    markers['symbol'] = 'circle'
    return(markers)


def make_color(marker_json):
    """
    return a list of colors formatted as rgb
    according to the color type and scaled
    """

    values = marker_json['x']
    color_strs = []
    for i in range(len(values)):

        value = values[i]
        value_min = min(values)
        value_max = max(values)

        norm = 255*(value_max - value)/(value_max - value_min)

        if marker_json['color_type'] == 'blues':
            mods = [0.1, 0.9, 0.1]
            r = int(0   + norm*mods[0])
            g = int(255 - norm*mods[1])
            b = int(255 - norm*mods[1])

        if marker_json['color_type'] == 'greens':
            mods = [0.1, 0.1, 0.9]
            r = int(0   + norm*mods[0])
            g = int(255 - norm*mods[1])
            b = int(255 - norm*mods[1])

        if marker_json['color_type'] == 'reds':
            mods = [0.1, 0.1, 0.9]
            r = int(255 -  norm*mods[0])
            g = int(0   + norm*mods[1])
            b = int(0   + norm*mods[1])

        else:
            mods = [0.95, 0.3, 0.8]
            r = int(0   + norm*mods[0])
            g = int(255 - norm*mods[1])
            b = int(255 - norm*mods[1])

        color_str = str('rgb( ' + str(r) + ' , ' +  str(g) + ' , ' + str(b) + ' )')
        color_strs.append(color_str)

    return(color_strs)


def write_data(ref_json):
    """
    write data
    """

    # data is a list traces
    data = []

    for wearable in ref_json:

        trace = {}
        trace['x'] = wearable['x']
        trace['y'] = list(wearable['y'])
        trace['name'] = 'name'
        trace['mode'] = wearable['layout_mode']
        trace['type'] = wearable['layout_type']

        marker_json = {}
        marker_json['x'] = trace['x']
        marker_json['y'] = trace['y']
        marker_json['x_title'] = wearable['x_label']
        marker_json['y_title'] = wearable['y_label']
        marker_json['color_type'] = wearable['color_type']
        trace['marker'] = make_marker(marker_json)
        data.append(trace)

    return(data)


def write_layout(ref_json):
    """
    write the config
    """
    layout = {}
    layout['title'] = ref_json[0]['plot_title']
    layout['showlegend'] = True
    layout['height'] = 600
    layout['width'] = 800

    xaxis = {}
    xaxis['title'] = ref_json[0]['x_label']
    xaxis['showgrid'] = True
    xaxis['titlefont'] = {"color": "rgb(0, 0, 0)"}
    xaxis['tickfont'] = {"color": "rgb(0, 0, 0)"}
    if 'TEMP' in  ref_json[0]['x_label']: xaxis['range'] = [30, 39]
    layout['xaxis'] = xaxis

    yaxis = {}
    yaxis['title'] = ref_json[0]['y_label']
    yaxis['showgrid'] = True
    yaxis['titlefont'] = {"color": "rgb(255, 70, 30)"}
    yaxis['tickfont'] = {"color": "rgb(255, 70, 30)"}
    if 'TEMP' in  ref_json[0]['y_label']: yaxis['range'] = [30, 39]
    layout['yaxis'] = yaxis

    return(layout)

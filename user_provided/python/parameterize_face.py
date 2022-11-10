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
import random
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


def parameterize_face():
    """
    build a scatter plot for each record
    """

    print("begin parameterize_face")

    tasks = [1, 2]
    if 1 in tasks: find_parameters()
    if 2 in tasks: build_face()

    print("completed parameterize_face")


def build_face():
    """
    turn parameters into face parameters
    """

    js_faces = {}
    faces = []
    for record in retrieve_json('face_json')['faces']:

        i = list(retrieve_json('face_json')['faces']).index(record)

        ref_json = {'i': i, 'canvas_width': 300, 'canvas_height': 300}

        face = {}
        face['face_diameter'] = find_face_diameter(i)
        face['face_color'] = find_colors(i)['face_color']
        face['outline_color'] = find_colors(i)['outline_color']
        face['nose'] = build_nose(i)
        face['face'] = make_face(ref_json)
        face['eyes'] = make_eyes(ref_json)
        faces.append(face)


    js_faces['face_count'] = len(faces)
    js_faces['faces'] = faces

    js_var_name = 'faces'
    with open(retrieve_path('face_js'), "w") as f:
        f.write('var ' + js_var_name + ' = ')
        json.dump(js_faces, f, indent = 4)
        f.write( ';' + '\n')
        f.close()



def make_eyes(ref_json):
    """
    return json for eyes
    """

    canvas_width = ref_json['canvas_width']
    canvas_height = ref_json['canvas_height']
    i = ref_json['i']

    value1 = scaled(normalized(list_values('slope_HR'), i), 20, 70)
    value2 = scaled(normalized(list_values('slope_TEMP'), i), 3, 20)
    delta = scaled(normalized(list_values('slope_EDA'), i), 0.5, 1)

    eyes = {}

    eyes['d1'] = value2
    eyes['x1'] = canvas_width/2 + value1
    eyes['y1'] = canvas_height/3
    eyes['x2'] = canvas_width/2 - value1
    eyes['y2'] = canvas_height/3
    eyes['d2'] = value2*2
    eyes['d3'] = value2*2.5
    eyes['sweep'] = delta
    eyes['outline_color'] = calculate_color('eye_outline', i, list_values('slope_HR'))
    return(eyes)


def make_face(ref_json):
    """
    return json to build face
    including fill color and outline
    """

    canvas_width = ref_json['canvas_width']
    canvas_height = ref_json['canvas_height']
    i = ref_json['i']

    value1 = scaled(normalized(list_values('slope_HR'), i), 50, 100)
    value2 = scaled(normalized(list_values('slope_TEMP'), i), 50, 100)
    delta = scaled(normalized(list_values('slope_EDA'), i), 20, 50)

    face = {}
    face['x1'] = canvas_width/2
    face['y1'] = canvas_height/2 + delta
    face['d1'] = value1
    face['x2'] = canvas_width/2
    face['y2'] = canvas_height/2 - delta
    face['d2'] = value2

    face['fillColor'] = calculate_color('face_fill', i, list_values('slope_HR'))
    face['outlineColor'] = calculate_color('face_outline', i, list_values('slope_HR'))
    return(face)


def build_nose(i):
    """
    return json describing nose as the points of a triangle,
    fill color, and outline color
    """

    canvas_width = 300
    canvas_height = 300

    value1 = scaled(normalized(list_values('slope_HR'), i), 10, 80)
    value2 = scaled(normalized(list_values('slope_TEMP'), i), 50, 100)
    delta = scaled(normalized(list_values('slope_EDA'), i), 20, 50)

    value = scaled(normalized(list_values('slope_HR'), i), 10, 80)
    value = round(value,4)

    height = value2
    width = value

    nose = {}
    nose['x1'] = (canvas_width - width)*0.5 + width
    nose['y1'] = (canvas_height - height)*0.5 + height
    nose['x2'] = (canvas_width - width)*0.5 + 0.5*width
    nose['y2'] = (canvas_height - height)*0.5
    nose['x3'] = (canvas_width - width)*0.5
    nose['y3'] = (canvas_height - height)*0.5 + height
    nose['fillColor'] = calculate_color('nose_fill', i, list_values('slope_HR'))
    nose['outlineColor'] = calculate_color('nose_outline', i, list_values('slope_HR'))

    return(nose)


def calculate_color(type, i, values):
    """
    return color
    """

    val= scaled(normalized(values, i), 0, 255)

    if type == 'face_color':
        mods = [1, 0.1, 1]
        r = int(val*mods[0])
        g = int(255 - val*mods[1])
        b = int(255 - val*mods[2])

    elif type == 'outline_color':
        # default
        mods = [1, 1, 1]
        r = int(255 - val*mods[0])
        g = int(255 - val*mods[1])
        b = int(255 - val*mods[2])

    elif type == 'nose_outline':
        # default
        mods = [1, 0.1, 0.6]
        r = int(255 - val*mods[0])
        g = int(255 - val*mods[1])
        b = int(255 - val*mods[2])

    elif type == 'nose_fill':
        # default
        mods = [1, 1, 1]
        r = int(255 - val*mods[0])
        g = int(255 - val*mods[1])
        b = int(255 - val*mods[2])

    elif type == 'eye_outline' or type == 'eye_fill':
        # default
        mods = [1, 1, 1]
        r = int(0   + val*mods[0])
        g = int(255 - val*mods[1])
        b = int(255 - val*mods[2])

    else:
        num1 = random.random()
        num2 = random.random()
        num3 = random.random()

        # default
        mods = [num1, num2, num2]
        r = int(255 - val*mods[0])
        g = int(255 - val*mods[1])
        b = int(255 - val*mods[2])


    color_str = str('rgb( ' + str(r) + ' , ' +  str(g) + ' , ' + str(b) + ' )')
    return(color_str)



def find_colors(i):
    """
    return json of the colors
    """

    colors_json = {}
    term = 'face_color'
    colors_json[term] = calculate_color(term, i, list_values('slope_TEMP'))
    term = 'outline_color'
    colors_json[term] = calculate_color(term, i, list_values('slope_HR'))

    return(colors_json)



def list_values(key):
    """
    return a list of all values in a key
    """

    faces_json = retrieve_json('face_json')['faces']

    values = []
    for face in faces_json:
        value = face[key]
        values.append(value)
    return(values)


def find_face_diameter(i):
    """
    return face diameter
    """

    values = list_values('slope_TEMP')
    value = scaled(normalized(values, i), 10, 80)
    value = round(value,4)
    face_diameter = value
    return(face_diameter)


def scaled(value, value_min, value_max):
    """
    return a value between the min and max
    """

    scaling = value_max - value_min
    scaled = scaling*value + value_min

    assert scaled <= value_max
    assert scaled >= value_min
    return(scaled)


def normalized(values, i):
    """
    reset the value to be between 0 and 1
    """

    value_max = max(values)
    value_min = min(values)
    value = values[i]
    norm = (value_max - value) / (value_max - value_min)

    assert norm <= 1
    assert norm >= 0
    return(norm)


def find_parameters():
    """
    build json saved as a js variable
    in the docs folder
    """

    json_faces = {}
    faces = []

    for study in os.listdir(retrieve_path('json_compiled')):

        if 'data' not in str(study): continue

        fil_src = os.path.join(retrieve_path('json_compiled'), study)
        for record in retrieve_json(fil_src)['records']:

            #print(record['name'])
            i = list(retrieve_json(fil_src)['records']).index(record)

            face = {}
            face['slope_EDA'] = record['polyfit']['EDA'][2][0]
            face['slope_HR'] = record['polyfit']['HR'][2][0]
            face['slope_TEMP'] = record['polyfit']['TEMP'][2][0]
            faces.append(face)

            json_faces['face_count'] = len(faces)
            json_faces['faces'] = faces


    js_var_name = 'faces'
    with open(retrieve_path('face_json'), "w") as f:
        #f.write('var ' + js_var_name + ' = ')
        json.dump(json_faces, f, indent = 4)
        #f.write( ';' + '\n')
        f.close()

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


def write_html():
    """
    build a scatter plot for each record
    """

    print("begin write_html")

    tasks = [1, 2]
    if 1 in tasks: write_canvas()
    if 2 in tasks: write_record_html()


    print("completed write_html")




def write_record_html():
    """
    make an index.html for each record
    """


    study_src = os.path.join('docs', 'data')
    for study in os.listdir(study_src):

        if '.html' in study: continue

        fol_src = os.path.join(study_src, study, 'js')
        for fol in os.listdir(fol_src):

            if '.html' in fol: continue

            print('fol = ' + str(fol))

            insert_text = []
            for fil in os.listdir(os.path.join(fol_src, fol)):

                    insert_text = '\n'
                    line.append(text)
                    insert_text = '<br>' + '\n'
                    line.append(text)
                    insert_text = '<div id="' + str(fil.split('.')[0])
                    line.append(text)
                    insert_text = '" style="text-align:center; width:80%; margin-left: 10%; max-width:800px;">'
                    line.append(text)
                    insert_text = '<script src="js/' + str(os.path.join(fol, fil)) + '"></script>'  + '\n'
                    line.append(text)
                    insert_text = '</div>'
                    insert_text = '<br>' + '\n'
                    line.append(text)
                    insert_text = '\n'
                    line.append(text)


            temp_dst = os.path.join('docs', 'data', study, 'index_temp' + '.html')
            fil_dst = os.path.join('docs', 'data', study, fol + '.html')
            """
            shutil.copy(temp_dst, fil_dst)
            f = open(fil_dst,"r")
            lines = f.readlines()
            f.close()
            """

            idenifier = '<!-- Insert chart info -->'
            with open(temp_dst) as f_old, open(fil_dst, "w") as f_new:
                for line in f_old:
                    f_new.write(line)
                    if 'identifier' in line:
                        for text in insert_text:
                            f_new.write(text)
            f_old.close()
            f_new.close()


def write_canvas():
    """
    write canvas elements with links
    """

    lines = []

    for study in os.listdir(retrieve_path('json_compiled')):

        if 'data' not in str(study): continue

        fil_src = os.path.join(retrieve_path('json_compiled'), study)
        for record in retrieve_json(fil_src)['records']:

            #print(record['name'])
            i = list(retrieve_json(fil_src)['records']).index(record)

            study = record['name'].split('_')[0]
            href_dst = os.path.join('data', study, record['name'] + '.html')

            line = str('<a href="' + str(href_dst) + '"><canvas width="300" height="300"></canvas></a> ')
            lines.append(line)

    with open(retrieve_path('canvas_html'), "w") as f:
        for line in lines:
            f.write(line + '\n')
        f.close()

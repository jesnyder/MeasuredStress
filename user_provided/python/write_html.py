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
import re
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
        if '.js' in study: continue

        fol_src = os.path.join(study_src, study, 'js')
        for fol in os.listdir(fol_src):

            if '.html' in fol: continue

            print('fol = ' + str(fol))

            insert_lines = []
            for fil in os.listdir(os.path.join(fol_src, fol)):

                if '.html' in fil: continue

                text = '\n'
                insert_lines.append(text)
                text = '<br>' + '\n'
                insert_lines.append(text)
                text = '<div id="' + str(fil.split('.')[0])
                insert_lines.append(text)
                text = '" style="text-align:center; width:80%; margin-left: 10%; max-width:800px;">'
                insert_lines.append(text)
                text = '\n'
                insert_lines.append(text)
                text = '<script src="' + str(os.path.join(fil)) + '"></script>'  + '\n'
                insert_lines.append(text)
                text = '</div>'
                insert_lines.append(text)
                text = '<br>' + '\n'
                insert_lines.append(text)
                text = '\n'
                insert_lines.append(text)


            temp_dst = os.path.join('docs', 'data', study, 'index_temp' + '.html')
            fil_dst = os.path.join('docs', 'data', study, 'js', fol, fol + '.html')

            """
            shutil.copy(temp_dst, fil_dst)
            f = open(fil_dst,"r")
            lines = f.readlines()
            f.close()
            """

            identifier = '<!-- Insert chart info -->'
            with open(temp_dst) as f_old, open(fil_dst, "w+") as f_new:

                for line in f_old:

                    if 'LASTRECORD' in line:

                        fol_num = float(fol.split('_')[-1])
                        fol_num_last = fol_num - 1

                        if fol_num_last > 1:

                            fol_last = fol.split('_')[0] + '_' + str(int(fol_num_last)).zfill(3)
                            fil_dst_last = os.path.join('../' , fol_last, fol_last + '.html')
                            line = str(line)
                            print(line)
                            print(fil_dst_last)
                            line = re.sub('LASTRECORD', str('"' + fil_dst_last + '"'), line)
                            f_new.write(line)

                    elif 'NEXTRECORD' in line:

                        fol_num_next = float(fol.split('_')[-1]) + 1
                        fol_next = fol.split('_')[0] + '_' + str(int(fol_num_next)).zfill(3)
                        fil_dst_next = os.path.join('../' , fol_next)

                        if os.path.exists(fil_dst_next) == True:
                            line = str(line)
                            line = re.sub('NEXTRECORD',  str('"' + fil_dst_next + '"'), line)
                            f_new.write(line)

                    elif identifier in line:
                        f_new.write(line)
                        for insert_line in insert_lines:
                            f_new.write(insert_line)

                    else:
                        f_new.write(line)


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
            href_dst = os.path.join('data', study, 'js', record['name'], record['name'] + '.html')

            line = str('<a href="' + str(href_dst) + '"><canvas width="300" height="300"></canvas></a> ')
            lines.append(line)

    with open(retrieve_path('canvas_html'), "w") as f:
        for line in lines:
            f.write(line + '\n')
        f.close()

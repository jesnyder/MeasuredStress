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

from build_json import build_json
from build_scatter_record import build_scatter_record
from parameterize_face import parameterize_face
from write_html import write_html

def main():
    """
    analyze data
    """

    print("running main")

    tasks = [4]
    if 1 in tasks: build_json()
    if 2 in tasks: build_scatter_record()
    if 3 in tasks: write_html()
    if 4 in tasks: parameterize_face()

    print("completed main")


if __name__ == "__main__":
    main()

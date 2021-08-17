from c0101_retrieve_ref import retrieve_ref

from c8001_modeling_test import modeling_test
from c8002_modeling_mean import modeling_mean



from datetime import date
from datetime import datetime
import math
import os
import pandas as pd
from pytz import reference
from shutil import copyfile


def openscad_modeling():
    """
    Write code for openscad to model parameters of the analysis
    """

    print("openSCAD modeling begin")

    modeling_test()
    modeling_mean()

    print("openSCAD modeling complete")

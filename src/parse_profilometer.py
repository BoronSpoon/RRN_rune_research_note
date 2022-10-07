# profilometer
import numpy as np
import pandas as pd
from misc import *

def read_files(input_path, output_path):
    with open(input_path, "r") as f:
        lines = f.readlines()

    data = pd_read_csv( 
        filename=input_path, encoding="utf-8", sep=", ", header_count=0, 
        names_old=["position (mm)", "height (μm)"], names_new=["position (μm)", "height (nm)"], unit_conversion_coefficients=[1000, 1],
    )
    data.to_csv(output_path, index=False)
    

def main(**kwargs):
    read_files(kwargs["input_path"], kwargs["output_path"])

# profilometer
import numpy as np
import pandas as pd
from pandasgui import show

def pd_read_csv(filename, encoding, sep, header_count, names_old, names_new, unit_conversion_coefficients, use_index=False, name_index=0, index_coefficient=0):
    data_old = pd.read_csv(filename, header=header_count, names=names_old, sep=sep, encoding=encoding)
    data_new = pd.DataFrame()
    if use_index:
        data_new[name_index] = np.arange(data_old.shape[0])*index_coefficient
    for name_old, name_new, unit_conversion_coefficient in zip(names_old, names_new, unit_conversion_coefficients):
        if "erase" not in name_new: # erase unnecessary columns
            data_new[name_new] = data_old[name_old]*unit_conversion_coefficient
    return data_new

def read_files(input_path, output_path):
    with open(input_path, "r") as f:
        lines = f.readlines()

    data = pd_read_csv( 
        filename=input_path, encoding="utf-8", sep=",", header_count=16, 
        names_old=["erase1", "Voltage (V)", "erase2"], names_new=["erase1", "Voltage (V)", "erase2"], unit_conversion_coefficients=[1, 1, 1], 
        use_index=True, name_index="time (ns)", index_coefficient=4E-013*1e9
    )
    data.to_csv(output_path, index=False)

    gui = show(data)

def main(**kwargs):
    read_files(kwargs["input_path"], kwargs["output_path"])

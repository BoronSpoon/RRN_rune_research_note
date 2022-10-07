import numpy as np
import pandas as pd

def pd_read_csv(filename, encoding, sep, header_count, names_old, names_new, unit_conversion_coefficients, use_index=False, name_index=0, index_coefficient=0):
    data_old = pd.read_csv(filename, header=header_count, names=names_old, sep=sep, encoding=encoding)
    data_new = pd.DataFrame()
    if use_index:
        data_new[name_index] = np.arange(data_old.shape[0])*index_coefficient
    for name_old, name_new, unit_conversion_coefficient in zip(names_old, names_new, unit_conversion_coefficients):
        if "erase" not in name_new: # erase unnecessary columns
            data_new[name_new] = data_old[name_old]*unit_conversion_coefficient
    return data_new
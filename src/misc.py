import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def pd_read_csv(filename, encoding, sep, header_count, names_old, names_new, unit_conversion_coefficients, use_index=False, name_index=0, index_coefficient=0):
    df_old = pd.read_csv(filename, header=header_count, names=names_old, sep=sep, encoding=encoding, engine="python")
    df_new = pd.DataFrame()
    if use_index:
        df_new[name_index] = np.arange(df_old.shape[0])*index_coefficient
    for name_old, name_new, unit_conversion_coefficient in zip(names_old, names_new, unit_conversion_coefficients):
        if "erase" not in name_new: # erase unnecessary columns
            df_new[name_new] = df_old[name_old]*unit_conversion_coefficient
    return df_new

def plot(df, plot_path):
    ax = plt.gca()
    keys = df.keys()
    plot_params = {
        "axes.labelsize": 16,
        "axes.titlesize": 16,    
        "lines.linestyle": "solid",
        "lines.linewidth": 2,
        "lines.markersize": 5,
        "xtick.major.size": 3.5,
        "xtick.minor.size": 2,
        "xtick.labelsize": 13,
        "ytick.major.size": 3.5,
        "ytick.minor.size": 2,
        "ytick.labelsize": 13,
    }
    plt.rcParams.update(plot_params)
    if len(keys) == 2: # dont need legend for two axis
        df.plot(kind="line", x=keys[0], y=keys[1], legend=None).set(ylabel=keys[1])
    else:
        df.plot(kind="line", x=keys[0], y=keys[1])

    plt.savefig(plot_path, bbox_inches="tight")

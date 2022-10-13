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

def set_min_0(df): # set minimum value of column to 0
    keys = df.keys()
    df[keys[1]] -= min(df[keys[1]])
    return df

def set_rcparams():
    plot_params = {
        "axes.labelsize": 16,
        "axes.titlesize": 16,    
        "lines.linestyle": "solid",
        "lines.linewidth": 1,
        "lines.marker": "o",
        "lines.markersize": 3,
        "xtick.major.size": 3.5,
        "xtick.minor.size": 2,
        "xtick.labelsize": 13,
        "ytick.major.size": 3.5,
        "ytick.minor.size": 2,
        "ytick.labelsize": 13,
    }
    plt.rcParams.update(plot_params)

def plot(df, plot_path, show=False):
    set_rcparams()
    ax = plt.gca()
    keys = df.keys()
    if len(keys) == 2: # dont need legend for two axis
        df.plot(kind="line", x=keys[0], y=keys[1], legend=None, ax=ax)
        ax.set(ylabel=keys[1])
    else:
        df.plot(kind="line", x=keys[0], y=keys[1], ax=ax)

    plt.savefig(plot_path, bbox_inches="tight")
    if show: plt.show()
    plt.cla()

def hist(df, hist_path, show=False):
    set_rcparams()
    ax = plt.gca()
    keys = df.keys()
    if len(keys) == 2: # dont need legend for two axis
        df.plot.hist(column=keys[1], bins=100, alpha=0.5, legend=None, ax=ax)
        ax.set(xlabel=keys[1])
    else:
        df.plot.hist(column=keys[1:], bins=100, alpha=1, ax=ax)

    annotate_top_n(df, ax, top_n=5)
    plt.savefig(hist_path, bbox_inches="tight")
    if show: plt.show()
    plt.cla()

# https://stackoverflow.com/questions/43374920/how-to-automatically-annotate-maximum-value-in-pyplot
def annotate_top_n(df, ax, top_n=1):
    keys = df.keys()
    for key in keys[1:]:
        hist, bins = np.histogram(df[key], bins=100)
        top_n_indices = np.argpartition(hist, -1*top_n)[-1*top_n:]
        for i in range(top_n):
            index_ = top_n_indices[i]
            x_max = bins[index_]
            y_max = hist[index_]
            text = f"{x_max:.3f}"
            bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
            arrow_props = dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=60")
            kw = dict(xycoords='data', textcoords="offset points", arrowprops=arrow_props, bbox=bbox_props, ha="left", va="top")
            ax.annotate(text, xy=(x_max, y_max), xytext=(max(bins)/20, max(hist)/20), **kw)
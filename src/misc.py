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

class Plot():
    def __init__(self, df, interactive=False):
        self.df = df
        self.interactive = interactive

    def plot_(self, plot_path):
        set_rcparams()
        self.ax = plt.gca()
        keys = self.df.keys()
        if len(keys) == 2: # dont need legend for two axis
            self.df.plot(kind="line", x=keys[0], y=keys[1], legend=None, ax=self.ax)
            self.ax.set(ylabel=keys[1])
        else:
            self.df.plot(kind="line", x=keys[0], y=keys[1], ax=self.ax)
        plt.savefig(plot_path, bbox_inches="tight")
 
    def on_xlims_change(self, event_ax):
        self.xlim = event_ax.get_xlim()
    def on_ylims_change(self, event_ax):
        self.ylim = event_ax.get_ylim()

    def crop_data(self):
        keys = self.df.keys()
        self.df = self.df[(self.df[keys[0]] > self.xlim[0]) & (self.df[keys[0]] < self.xlim[1]) & (self.df[keys[1]] > self.ylim[0]) & (self.df[keys[1]] < self.ylim[1])]

    def plot(self, plot_path):
        self.plot_(plot_path)
        if self.interactive:
            self.xlim=None
            self.ylim=None
            self.ax.callbacks.connect("xlim_changed", self.on_xlims_change)
            self.ax.callbacks.connect("ylim_changed", self.on_ylims_change)
            plt.show()
            if self.xlim is not None and self.ylim is not None:
                self.crop_data()
            self.plot_(plot_path)
            plt.cla()

    def hist(self, hist_path):
        set_rcparams()
        ax = plt.gca()
        keys = self.df.keys()
        if len(keys) == 2: # dont need legend for two axis
            self.df.plot.hist(column=keys[1], bins=100, alpha=0.5, legend=None, ax=ax)
            ax.set(xlabel=keys[1])
        else:
            self.df.plot.hist(column=keys[1:], bins=100, alpha=1, ax=ax)

        annotate_top_n(self.df, ax, top_n=5)
        plt.savefig(hist_path, bbox_inches="tight")
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
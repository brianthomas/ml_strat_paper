import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy

import sys
sys.path.append("../src")
from fitting_util import *

def plot_data_errs (x, y, y_err, xlabel="", ylabel="", title="Title", ax=None, color='red'):
    if ax == None:
        fig, ax = plt.subplots()

    #plt.style.use('fivethirtyeight')

    ax.plot(x, y, marker='o', markerfacecolor=color, linestyle=' ')
    plt.errorbar(x, y, fmt='ko', yerr=y_err)

    ax.set_title(title)
    ax.set(xlabel=xlabel, ylabel=ylabel)

    return ax

def plot_report(df:pd.DataFrame, title:str="", which_cagr:str="CAGR", offset:str="FILLINOFFSET", spearman:bool=False, 
        cagr_err:float=0.009, ri_err:float=20., tcs_lit_err:float=5.5):

    fig, axs = plt.subplots(3, figsize=(6,12))

    fig.suptitle(f"Report\n{title}")

    plot_cagr_scatter(df, title, which_cagr=which_cagr, ax=axs[0], spearman=spearman, yerr_est=cagr_err)
    #axs[0].set(xlabel="", ylabel=f"{which_cagr}")

    plot_tcs_scatter(df, title, ax=axs[1], spearman=spearman, yerr_est=tcs_lit_err)
    #axs[1].set(ylabel='Counts (per topic)')

    plot_ri_scatter(df, title, ax=axs[2], spearman=spearman, yerr_est=cagr_err)
    axs[2].set(xlabel="Topic Document Content (%)", ylabel=f"RI$_{1998-2010}$ (O=={offset})")


def plot_cagr_scatter(df:pd.DataFrame, title:str="", which_cagr:str="CAGR", ax=None, spearman:bool=False, yerr_est:float=0.009):
    x=np.array(df['doc_tcs'])
    y=np.array(df['cagr'])
    y_err = [yerr_est for i in range(0,len(y))] 

    plot_scatter(x, y, y_err, title, "Document TCS (%)", f"TCS_CAGR$_{1998-2010}$ {which_cagr}", ax, spearman)

def plot_ri_scatter(df:pd.DataFrame, title:str="", ax=None, spearman:bool=False, yerr_est:float=20.):
    x=np.array(df['doc_tcs'])
    y=np.array(df['ri'])
    y_err = [yerr_est for i in range(0,len(y))] 
    plot_scatter(x, y, y_err, title, "Document TCS (%)", f"RI$_{1998-2010}$", ax, spearman)

def plot_tcs_scatter(df:pd.DataFrame, title:str="", ax=None, spearman:bool=False, yerr_est:float=1.):
    x=np.array(df['doc_tcs'])
    y=np.array(df['tcs'])
    y_err = [yerr_est for i in range(0,len(y))] 
    plot_scatter(x, y, y_err, title, "Document TCS (%)", f"TCS$_{1998-2010}$", ax, spearman)

def plot_scatter(x, y, y_err, title:str="", xlabel:str="", ylabel:str="", ax=None, spearman:bool=False):

    if spearman:
        coeff, p = scipy.stats.spearmanr(x, y)
    else:
        coeff, p = scipy.stats.pearsonr(x, y)

    pfit, perr, redchisq = fit_leastsq([0.,1.], x, y, functions['line']['func'], y_err)

    single = False
    if ax == None:
        single = True

    if single:
        plotdata (plt, f"{title}\n r:%5.3f p:%6.4f\n {pfit} {perr}" % (coeff,p), x, y, [], pfit, perr, redchisq, functions['line']['func'])
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.errorbar(x,y,y_err,fmt='o')
        plt.show()
    else:
        ax.plot(x, y, 'ko')
        ax.text(3*(np.amax(x)/4), 9*(np.amax(y)/10), f"r:%5.3f p:%6.4f" % (coeff, p))
        ax.errorbar(x,y,y_err,fmt='o')


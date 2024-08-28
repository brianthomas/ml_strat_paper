''' Module of plotting utility functions '''
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy

sys.path.append("../src")
from fitting_util import *

def plot_data (xdata, ydata, xlabel="", ylabel="", title="Decadal Analysis", ax=None, color='red'):
    ''' utility plot data method '''

    if ax is None:
        fig, ax = plt.subplots()

    #ax.style.use('fivethirtyeight')

    ax.plot(xdata, ydata, marker='o', markerfacecolor=color, linestyle=' ')

    ax.set_title(title)
    ax.set(xlabel=xlabel, ylabel=ylabel)

    return ax

def plot_data_errs (x, y, y_err, xlabel="", ylabel="", title="Title", ax=None, color='red'):
    ''' utility plot data with y errors method '''
    if ax is None:
        fig, ax = plt.subplots()

    ax.plot(x, y, marker='o', markerfacecolor=color, linestyle=' ')
    ax.errorbar(x, y, fmt='ko', yerr=y_err)

    ax.set_title(title)
    ax.set(xlabel=xlabel, ylabel=ylabel)

    return ax

def plotdata_with_errors (ax, x, y, y_err ):
    ''' alternative utility plot data with y errors method '''

    #plot data and errors
    ax.plot(x, y, "ko", label='Topic')
    ax.errorbar(x, y, fmt='ko', yerr=y_err)

def plotdata_with_errors_and_func (ax, x, y, y_err, p, fitfunc):
    ''' utility plot data with y errors and a fitting function method '''

    plotdata_with_errors(ax, x, y, y_err )
    ax.plot(x, fitfunc(p, x), 'r-', label='Fitted Fnct')


def plotdata_and_residuals(ax, center, x, y, y_err, pfit, redchisq, fitfunc, ylabel:str="", xlabel:str="", ylim:list=None):
    ''' utility plot data with y errors and a fitting function with residuals from fit method '''

    fitfunc_cnst = lambda p, x: np.array([p[0] for dx in x])

    fig = ax.figure(1)
    fig.add_axes((.1,.3,.8,.6))
    plotdata_with_errors_and_func(ax, x, y, y_err, pfit, fitfunc )
    ax.title(f" {center}")
    ax.ylabel(ylabel)
    if ylim != None:
        ax.ylim(ylim)

    #ax.grid()

    # fit and plot residuals w/ a constant
    difference = fitfunc(pfit, x) - y

    # try to fit with constant line
    pfit_cnst, perr_cnst, redchisq_cnst = fit_leastsq([0], x, difference, fitfunc_cnst, y_err)

    fig.add_axes((.1,.1,.8,.2))
    plotdata_with_errors(ax, x, difference, y_err)
    ax.ylabel("Residuals")

    ax.plot(x, fitfunc_cnst(pfit_cnst, x), 'r-', label='Fitted Const')
    #ax.title(f" Fitted value {pfit_cnst[0]} +/- {perr_cnst[0]}\n redchi:{redchisq_cnst}")
    #ax.ylim(-125.,125.)
    ax.xlabel(xlabel)

def plot_report(df:pd.DataFrame, title:str="", which_cagr:str="CAGR", offset:str="FILLINOFFSET", spearman:bool=False,
        cagr_err:float=0.009, ri_err:float=20., tcs_lit_err:float=5.5):
    ''' utility plot report of 3 scatter plots (x-axis is doc TCS) ''' 

    fig, axs = plt.subplots(3, figsize=(6,12))

    fig.suptitle(f"Report\n{title}\n")

    plot_cagr_scatter(df, which_cagr=which_cagr, ax=axs[0], spearman=spearman, yerr_est=cagr_err)

    plot_tcs_scatter(df, ax=axs[1], spearman=spearman, yerr_est=tcs_lit_err)

    plot_ri_scatter(df, ax=axs[2], offset=offset, spearman=spearman, yerr_est=ri_err)
    # axs[2].set(xlabel="Topic Document Content (%)", ylabel=f"RI$_{1998-2010}$ (O=={offset})")


def plot_cagr_scatter(df:pd.DataFrame, which_cagr:str="CAGR", ax=None, spearman:bool=False, yerr_est:float=0.009):
    ''' Make TCS CAGR vs Document TCS scatter plot '''
    x=np.array(df['doc_tcs'])
    y=np.array(df['cagr'])
    y_err = [yerr_est for i in range(0,len(y))]

    y_label = 'TCS_CAGR$_{1998-2010}$\n' + f"({which_cagr})"
    plot_scatter(x, y, y_err, "Document TCS (%)", y_label, ax, spearman)

def plot_ri_scatter(df:pd.DataFrame, ax=None, offset:str="0", spearman:bool=False, yerr_est:float=20.):
    ''' Make RI vs Document TCS scatter plot '''
    x=np.array(df['doc_tcs'])
    y=np.array(df['ri'])
    y_err = [yerr_est for i in range(0,len(y))]
    y_label = "RI$_{1998-2010}$" + f"\n(O = {offset})"
    plot_scatter(x, y, y_err, "Document TCS (%)", y_label, ax, spearman)

def plot_tcs_scatter(df:pd.DataFrame, ax=None, spearman:bool=False, yerr_est:float=1.):
    ''' Make Lit TCS vs Document TCS scatter plot '''
    x=np.array(df['doc_tcs'])
    y=np.array(df['tcs'])
    y_err = [yerr_est for i in range(0,len(y))]
    plot_scatter(x, y, y_err, "Document TCS (%)", "TCS$_{1998-2010}$", ax, spearman)

def plot_scatter(x, y, y_err, xlabel:str="", ylabel:str="", ax=None, spearman:bool=False):
    ''' make a scatter plot '''

    if spearman:
        coeff, p = scipy.stats.spearmanr(x, y)
    else:
        coeff, p = scipy.stats.pearsonr(x, y)

    pfit, perr, redchisq = fit_leastsq([0.,1.], x, y, functions['line']['func'], y_err)

    ax.plot(x, y, 'ko')
    redchi_label = f"r:%5.3f p:%6.4f" % (coeff, p)
    ax.text(3*(np.amax(x)/4), 9*(np.amax(y)/10), redchi_label)
    ax.errorbar(x,y,y_err,fmt='o')

    if xlabel != "":
        ax.set_xlabel(xlabel)
    if ylabel != "":
        ax.set_ylabel(ylabel)

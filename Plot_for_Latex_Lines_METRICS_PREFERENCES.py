#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 22:33:38 2018

@author: eduardo
"""
#https://stackoverflow.com/questions/14279344/how-can-i-add-textures-to-my-bars-and-wedges
#https://stackoverflow.com/questions/22833404/how-do-i-plot-hatched-bars-using-pandas

from matplotlib.ticker import FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib
from math import sqrt
SPINE_COLOR = 'gray'
matplotlib.style.use('ggplot')

def latexify(fig_width=None, fig_height=None, columns=1):
    """Set up matplotlib's RC params for LaTeX plotting.
    Call this before plotting a figure.

    Parameters
    ----------
    fig_width : float, optional, inches
    fig_height : float,  optional, inches
    columns : {1, 2}
    """

    # code adapted from http://www.scipy.org/Cookbook/Matplotlib/LaTeX_Examples

    # Width and max height in inches for IEEE journals taken from
    # computer.org/cms/Computer.org/Journal%20templates/transactions_art_guide.pdf

    assert(columns in [1,2])

    if fig_width is None:
        fig_width = 3.39 if columns==1 else 6.9 # width in inches

    if fig_height is None:
        golden_mean = (sqrt(5)-1.0)/2.0    # Aesthetic ratio
        fig_height = fig_width*golden_mean # height in inches

    MAX_HEIGHT_INCHES = 8.0
    if fig_height > MAX_HEIGHT_INCHES:
        print("WARNING: fig_height too large:" + fig_height + 
              "so will reduce to" + MAX_HEIGHT_INCHES + "inches.")
        fig_height = MAX_HEIGHT_INCHES

    params = {'backend': 'ps',
              'text.latex.preamble': ['\usepackage{gensymb}'],
              'axes.labelsize': 20, # fontsize for x and y labels (was 10)
              'axes.titlesize': 18,
              'font.size': 18, # was 10
              'legend.fontsize': 16, # was 10
              'xtick.labelsize': 20, #was 20
              'ytick.labelsize': 18, # was 20
              'text.usetex': True,
              'figure.figsize': [fig_width,fig_height],
              'font.family': 'serif' # was serif
    }

    matplotlib.rcParams.update(params)


def format_axes(ax):

    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)

    for spine in ['left', 'bottom']:
        ax.spines[spine].set_color(SPINE_COLOR)
        ax.spines[spine].set_linewidth(0.5)

    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_tick_params(direction='out', color=SPINE_COLOR)

    return ax

    

###############################################################
if __name__ == "__main__":
    print("Prepare for LaTEX")

    
    '''
        Data
    '''
    df = pd.read_csv('metrics_consensus_data_lines.txt')
    #df = df[['e_method1','e_method2','e_fairness','e_average']]
    #df.columns = ['2','3','4','5','6']
    df.index = [2,3,4,5,6]
    #df = df.drop('id',axis=1)
    df.columns = ['M1', 'M2', 'Fairness', 'Average', 'GR']
    #lines = df.plot.line()
    print df
    
    '''
        Type of plot
    '''
    latexify(columns=2)
    styles=['bs-', 'ro-', 'g^-', 'kx-', 'yv-']
    ax = df.plot(kind='line', rot=0, legend=False, style=styles)
    
    bars = ax.patches
    #patterns =('-', '+', 'x','/','//','O','o','\\','\\\\')
    #patterns =('///','xx','-','\\\\')
    
    hatches = [p for p in styles for i in range(len(df))]
    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)
    
    ##ax.legend(loc='best')
    ax.set_xticks(df.index)
    
    ticks = ax.get_yticks()
    #ax.set_yticklabels(ticks)
    print ticks
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.5f'))
    
    ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=3, mode="expand", borderaxespad=0.)
    

    '''
        Labels and Title
    '''
    label_x = 'Group size'
    lab = label_x.replace(" ","")
    label_y = 'Consensus'
    title = ''
    tit = title.replace(" ","")
    
    ax.set_xlabel(label_x)
    ax.set_ylabel(label_y)
    ax.set_title(title)
    plt.tight_layout()
    format_axes(ax)
    
    '''
        Output
    '''
    file_title = 'consensus YahooMovies with GR (3 categories)'
    tit = file_title.replace(" ","")
    #outputfilename = tit + '_' + 'comparison_image.pdf'
    outputfilename = tit + '_' + lab + '_' + 'comparison_image.pdf'
    print outputfilename    

    plt.savefig(outputfilename, bbox_inches='tight')
    

        
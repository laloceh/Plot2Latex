#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 22:33:38 2018

@author: eduardo
"""
#https://stackoverflow.com/questions/14279344/how-can-i-add-textures-to-my-bars-and-wedges
#https://stackoverflow.com/questions/22833404/how-do-i-plot-hatched-bars-using-pandas

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
              'xtick.labelsize': 20, # was 10
              'ytick.labelsize': 20, # was 10
              'text.usetex': True,
              'figure.figsize': [fig_width,fig_height],
              'font.family': 'serif'
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
    df = pd.read_csv('random_data.txt')
    alpha = df['alpha']
    alpha = alpha.loc[2]
    alpha = round(alpha,2)
    df = df[['e_method1','e_method2','e_fairness','e_average','e_GRmodel']]
    df.columns = ['M1','M2','Fairness','Average','GR']
    df.index = [0.4, 0.5, 0.6, 0.7, 0.8]

    '''
        Type of plot
    '''
    latexify(columns=2)
    
    ax = df.plot(kind='bar', rot=0, legend=False)
    
    bars = ax.patches
    #patterns =('-', '+', 'x','/','//','O','o','\\','\\\\')
    patterns =('///','xx','-','\\\\', '||')
    hatches = [p for p in patterns for i in range(len(df))]
    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)
    
    #ax.set_ylim(0,1)
    #ax.legend(loc='upper right')

    #ax.legend(loc='best', ncol=4, mode="expand", shadow=True, fancybox=False)
    #ax.legend.get_frame().set_alpha(0.5)
    
    ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=3, mode="expand", borderaxespad=0.)
    
    '''
        Labels and Title
    '''
    label_x = '$\\alpha$ value'  #$\\alpha$ value
    lab = label_x.replace(" ","")
    label_y = 'Balance error (lower is better)'
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
    file_title = 'Yahoo!Movies_GR (2 categories)'
    tit = file_title.replace(" ","")
    outputfilename = tit + '_' + str(alpha).replace('.','') + '_' + lab + '_' + 'comparison_image.pdf'
    print outputfilename    

    plt.savefig(outputfilename, bbox_inches='tight')
    

        
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 22 11:27:43 2018

@author: eduardo
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 22:33:38 2018

@author: eduardo
"""

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
              'axes.labelsize': 16, # fontsize for x and y labels (was 10)
              'axes.titlesize': 8,
              'font.size': 8, # was 10
              'legend.fontsize': 10, # was 10
              'xtick.labelsize': 10,
              'ytick.labelsize': 10,
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
    df = df[['method1_2c','method2_2c','method1_3c','method2_3c']]
    df.columns = ['M1 2C','M2 2C','M1 3C','M2 3C']
    df.index = [2,3,4,5,6]

    '''
        Type of plot
    '''
    
    
    latexify(columns=2)
    ax = df.plot(kind='bar', rot=0, legend=False)
    
    bars = ax.patches
    #patterns =('-', '+', 'x','/','//','O','o','\\','\\\\')
    patterns =('///','xx','-','\\\\')
    hatches = [p for p in patterns for i in range(len(df))]
    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)
    
    ax.legend(loc='best')
    
    
    '''
        Labels and Title
    '''
    label_x = 'Group size'
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
    file_title = 'Yahoo! Movies (2 and 3 categories)'
    tit = file_title.replace(" ","")
    outputfilename = tit + '_' + str(alpha).replace('.','') + '_' + lab + '_' + 'comparison_image.pdf'
    print outputfilename      

    plt.savefig(outputfilename)
    

        
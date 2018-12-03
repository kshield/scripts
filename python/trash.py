#!/c/Users/Public/python
# -*- coding: utf-8 -*-
#"""
#Created on Tue May  8 13:40:20 2018
#@author: Kathy Shield
#"""

import os
import time
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import datetime
import plotly as py
import plotly.graph_objs as go
from sklearn import linear_model
from numpy import arange, array, ones
from sklearn.metrics import mean_squared_error, r2_score
from scipy import stats
py.tools.set_credentials_file(username = 'kshield', api_key = 'H9UX6nYroLdbt1W1pjgj')


xi = arange (0,9)
A = array([ xi, ones(9)])

y = [19, 20, 20.5, 21.5, 22, 23, 25,24,26]

slope, intercept, r_value, p_value, std_err = stats.linregress(xi,y)
line = slope*xi+intercept

trace1 = go.Scatter(x=xi,
y=line,
mode = 'lines')

layout = go.Layout(
    title = 'Distribution Ratios',
    xaxis = dict(
        type = 'log',
        autorange = True,
        #domain = [0,1],
        #range = [-4,-2],
        title = 'Ligand Concentration (mM)',
        showgrid = True,
        showline = True,
        exponentformat = 'e',
        #nticks = 5
        tick0 = -4,
        dtick = 1
    ),
    yaxis = dict(
        type = 'log',
        autorange = True,
    #    domain = [0,1],
    #    range = [0,1.1],
        title = 'D (distribution ratio)',
        showgrid = True,
        showline = True
    ))
fig = go.Figure(data=trace1, layout=layout)
plot = py.offline.plot(fig, image = 'png')

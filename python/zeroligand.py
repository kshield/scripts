#!/c/Users/Public/python

# First go into the pandas dataframe and determine what lines we're looking at

#import the necessary packages
import os
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import csv
import plotly as py
import plotly.graph_objs as go
py.tools.set_credentials_file(username = 'kshield', api_key = 'H9UX6nYroLdbt1W1pjgj')

datan = pd.read_csv(os.path.join('c:\\Users\\Kathy Shield\\Desktop\\Berkeley\\AbergelGroup\\Research\\Extractions\\Results\\ProcessedDataFiles','allthedata.csv'))

isotopelist = ['Ac227','Gd153','Lu177']
yvalues = []
yerror = []
text = []

from math import log10, floor
def round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(abs(x))))-1)


for isotope in isotopelist:
    datatable = datan[(datan['Ligand'] == 'none') & (datan['Isotope'] == isotope ) & (datan['Initial pH'] == 6)]
    value = datatable['Extraction %'].mean()
    standard_deviation = datatable['Extraction %'].std()
    yvalues.append(value)
    yerror.append(standard_deviation)
    value = round_sig(value,4)*100
    stdev = round_sig(standard_deviation,4)*100
    stdev = round_sig(stdev,4)
    text.append(str(value)+'±'+str(stdev)+'%')

trace1 = go.Bar(
    x = isotopelist,
    y = yvalues,
    text = text,
    textposition = 'outside',
    marker = dict(
        color=['rgba(170,255,195,1)', 'rgba(128,0,0,0.7)', 'rgba(0,130,200,0.7)']
    ),
    width = [.6,.6,.6],
    error_y = dict(
        type = 'data',
        array = yerror,
        visible = True
    )
)

#data = [go.Bar(
#    x = isotopelist,
#    y = yvalues,
#    error_y = yerror
#)]

data = [trace1]
layout = go.Layout(
    title = 'Extraction into HDEHP with No Competing Ligand'
)

fig = go.Figure(data = data, layout = layout)
plot = py.offline.plot(fig, image = 'png')

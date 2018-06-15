#!/c/Users/Public/python





## PLAYING WITH plotly

#import the necessary packages
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import csv
import plotly as py
import plotly.graph_objs as go
py.tools.set_credentials_file(username = 'kshield', api_key = 'H9UX6nYroLdbt1W1pjgj')

# import a file for practice
path = '~/Desktop/Berkeley/AbergelGroup/Research/Extractions/'
data1 = pd.read_csv(path+'20180521Gd153_CDTA_HDEHP.csv')
yvalues1 = data1['Extraction %'].tolist()
xvalues1 = data1['Ligand Concentration (mM)'].tolist()
trace1 = go.Scatter(x=xvalues1, y=yvalues1, name = 'CDTA', mode='markers')

data2 = pd.read_csv(path+'20180521Gd153_DTPA_HDEHP.csv')
yvalues2 = data2['Extraction %'].tolist()
xvalues2 = data2['Ligand Concentration (mM)'].tolist()
trace2 = go.Scatter(x=xvalues2, y = yvalues2, name = 'DTPA', mode = 'markers')


data3 = pd.read_csv(path+'20180521Gd153_EDTA_HDEHP.csv')
yvalues3 = data3['Extraction %'].tolist()
xvalues3 = data3['Ligand Concentration (mM)'].tolist()
trace3 = go.Scatter(x=xvalues3, y = yvalues3, name = 'EDTA', mode = 'markers')


data4 = pd.read_csv(path+'20180521Gd153_PDTA_HDEHP.csv')
yvalues4 = data4['Extraction %'].tolist()
xvalues4 = data4['Ligand Concentration (mM)'].tolist()
trace4 = go.Scatter(x=xvalues4, y = yvalues4, name = 'PDTA', mode = 'markers')



data = [trace1, trace2, trace3, trace4]
layout = go.Layout(
    xaxis = dict(
        type = 'log',
        autorange = True,
        domain = [0,1],
        range = [-4,-2],
        title = 'Ligand Concentration (mM)',
        showgrid = True,
        showline = True,
        exponentformat = 'none',
        #nticks = 5
        tick0 = -4,
        dtick = 1
    ),
    yaxis = dict(
        type = 'linear',
        autorange = False,
        domain = [0,1],
        range = [0,1],
        title = 'Extraction Percent',
        showgrid = True,
        showline = True
    ),
    title='Gd153 Extraction into HDEHP with Carboxylic Acid Competitors'
)

fig = go.Figure(data=data, layout=layout)

py.offline.iplot(fig)

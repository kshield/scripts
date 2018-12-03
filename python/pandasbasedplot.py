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

# import a file for practice
datan = pd.read_csv(os.path.join('c:\\Users\\Kathy Shield\\Desktop\\Berkeley\\AbergelGroup\\Research\\Extractions\\Results\\ProcessedDataFiles','allthedata.csv'))
print ('done')
rowsofinterest = input ('What rows are being graphed today?: ')
rowsofinterest = [float(x) for x in rowsofinterest.split(',')]

yvalues = datan['Extraction %'].tolist()
xvalues = datan[dependentvariable].tolist()
trace = go.Scatter(x = xvalues, y = yvalues, mode = 'markers')
allthedata.append(trace)

layout = go.Layout(
xaxis = dict(
    type = 'log',
    autorange = True,
    domain = [0,1],
    range = [-4,-2],
    title = dependentvariable,
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
title='Gd153 Extraction into HDEHP with Varying Buffer Concentrations',
showlegend = True
)

fig = go.Figure(data=allthedata, layout=layout)

py.offline.iplot(fig)


howmanyfiles = input('How many files are there? ')
allthedata = []
varies = input('What varies? PICK ONE: aql, aqconc, ph, orgl, orgconc, isotope, buffer, bufferconc  > ')

def plotthething():
    for value in range(int(howmanyfiles)):
        # Filenames are in this format when they come out of splitLSC.sh
        datafile = str(value+1)+'.ExperTable.csv'
        filename = input('What is the filename? (YYYYMMDDisotope_ligand_extractant.csv): ')
        if varies == 'aql':
            dependentvariable = 'Ligand'
        elif varies == 'aqconc':
            dependentvariable = 'Ligand Concentration (mM)'
        elif varies == 'ph':
            dependentvariable = 'Initial pH'
        elif varies == 'orgl':
            dependentvariable = 'Extractant'
        elif varies == 'orgconc':
            dependentvariable = 'Extractant Concentration (M)'
        elif varies == 'isotope':
            dependentvariable = 'Isotope'
        elif varies == 'buffer':
            dependentvariable = 'Buffer'
        elif varies == 'bufferconc':
            dependentvariable = 'Buffer Concentration (mM)'

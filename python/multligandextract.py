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

### pH 6 DATA

relevantdata = datan[(datan['Isotope'] == 'Gd153') &
(datan['Date'] != '6/20/2018') &
(datan['Initial pH'] == 6) &
(datan['Extractant Concentration (M)'] == 0.0025)]


CDTA6data = relevantdata[relevantdata['Ligand'] == 'CDTA']
CDTA6data = CDTA6data.sort_values('Ligand Concentration (mM)')
DTPA6data = relevantdata[relevantdata['Ligand'] == 'DTPA']
DTPA6data = DTPA6data.sort_values('Ligand Concentration (mM)')
EDTA6data = relevantdata[relevantdata['Ligand'] == 'EDTA']
EDTA6data = EDTA6data.sort_values('Ligand Concentration (mM)')
PDTA6data = relevantdata[relevantdata['Ligand'] == 'PDTA']
PDTA6data = PDTA6data.sort_values('Ligand Concentration (mM)')
CAM6data = relevantdata[relevantdata['Ligand'] == 'CAM']
CAM6data = CAM6data.sort_values('Ligand Concentration (mM)')
CHHC6data = relevantdata[relevantdata['Ligand'] == 'CHHC']
CHHC6data = CHHC6data.sort_values('Ligand Concentration (mM)')
HCCH6data = relevantdata[relevantdata['Ligand'] == 'HCCH']
HCCH6data = HCCH6data.sort_values('Ligand Concentration (mM)')
HOPO6data = relevantdata[relevantdata['Ligand'] == 'HOPO']
HOPO6data = HOPO6data.sort_values('Ligand Concentration (mM)')

CDTA6plot = go.Scatter(
    x = CDTA6data['Ligand Concentration (mM)'],
    y = CDTA6data['Extraction %'],
    mode = 'lines+markers',
    name = 'CDTA, pH 6',
    line = dict(color = "rgba(240,0,0,1)")
)

DTPA6plot = go.Scatter(
    x = DTPA6data['Ligand Concentration (mM)'],
    y = DTPA6data['Extraction %'],
    mode = 'lines+markers',
    name = 'DTPA, pH 6',
    line = dict(color = 'rgba(56,6,156,1)')
)

EDTA6plot = go.Scatter(
    x = EDTA6data['Ligand Concentration (mM)'],
    y = EDTA6data['Extraction %'],
    mode = 'lines+markers',
    name = 'EDTA, pH 6',
    line = dict(color = 'rgba(124,3,83,1)')
)

PDTA6plot = go.Scatter(
    x = PDTA6data['Ligand Concentration (mM)'],
    y = PDTA6data['Extraction %'],
    mode = 'lines+markers',
    name = 'PDTA, pH 6',
    line = dict(color = 'rgba(250,100,30,1)')
)

CAM6plot = go.Scatter(
    x = CAM6data['Ligand Concentration (mM)'],
    y = CAM6data['Extraction %'],
    mode = 'lines+markers',
    name = 'CAM, pH 6',
    line = dict(color = 'rgba(76,178,76,1)')
)

CHHC6plot = go.Scatter(
    x = CHHC6data['Ligand Concentration (mM)'],
    y = CHHC6data['Extraction %'],
    mode = 'lines+markers',
    name = 'CHHC, pH 6',
    line = dict(color = 'rgba(16,136,102,1)')
)

HCCH6plot = go.Scatter(
    x = HCCH6data['Ligand Concentration (mM)'],
    y = HCCH6data['Extraction %'],
    mode = 'lines+markers',
    name = 'HCCH, pH 6',
    line = dict(color = 'rgba(105,178,231,1)')
)

HOPO6plot = go.Scatter(
    x = HOPO6data['Ligand Concentration (mM)'],
    y = HOPO6data['Extraction %'],
    mode = 'lines+markers',
    name = 'HOPO, pH 6',
    line = dict(color = 'rgba(16,54,207,1)')
)

#### pH 7 DATA #####
relevantdata7 = datan[(datan['Isotope'] == 'Gd153') & #(datan['Date'] != '6/20/2018') &
(datan['Initial pH'] == 7.2) & (datan['Extractant Concentration (M)'] == 0.0025)]

CDTA7data = relevantdata7[relevantdata7['Ligand'] == 'CDTA']
CDTA7data = CDTA7data.sort_values('Ligand Concentration (mM)')
DTPA7data = relevantdata7[relevantdata7['Ligand'] == 'DTPA']
DTPA7data = DTPA7data.sort_values('Ligand Concentration (mM)')
EDTA7data = relevantdata7[relevantdata7['Ligand'] == 'EDTA']
EDTA7data = EDTA7data.sort_values('Ligand Concentration (mM)')
PDTA7data = relevantdata7[relevantdata7['Ligand'] == 'PDTA']
PDTA7data = PDTA7data.sort_values('Ligand Concentration (mM)')

#print (DTPAdata)

CDTA7plot = go.Scatter(
    x = CDTA7data['Ligand Concentration (mM)'],
    y = CDTA7data['Extraction %'],
    mode = 'lines+markers',
    name = 'CDTA, pH 7',
    marker = dict(symbol = "square"),
    line = dict(color = "rgba(240,0,0,.75)")
)

DTPA7plot = go.Scatter(
    x = DTPA7data['Ligand Concentration (mM)'],
    y = DTPA7data['Extraction %'],
    mode = 'lines+markers',
    name = 'DTPA, pH 7',
    marker = dict(symbol = "square"),
    line = dict(color = 'rgba(56,6,156,.75)')
)

EDTA7plot = go.Scatter(
    x = EDTA7data['Ligand Concentration (mM)'],
    y = EDTA7data['Extraction %'],
    mode = 'lines+markers',
    name = 'EDTA, pH 7',
    marker = dict(symbol = "square"),
    line = dict(color = 'rgba(124,3,83,.75)', dash = "dash")
)

PDTA7plot = go.Scatter(
    x = PDTA7data['Ligand Concentration (mM)'],
    y = PDTA7data['Extraction %'],
    mode = 'lines+markers',
    name = 'PDTA, pH 7',
    marker = dict(symbol = "square"),
    line = dict(color = 'rgba(250,100,30,.75)')
)

data = [CDTA6plot,DTPA6plot,EDTA6plot,PDTA6plot,
CDTA7plot, DTPA7plot, EDTA7plot, PDTA7plot,
CAM6plot,CHHC6plot,HCCH6plot,HOPO6plot
]

layout = go.Layout(
xaxis = dict(
    type = 'log',
    autorange = True,
    #domain = [0,1],
    #range = [-4,-2],
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
title='Gd153 Extraction into HDEHP with Varying Buffer Concentrations',
showlegend = True
)


fig = go.Figure(data=data, layout=layout)
#
py.offline.plot(fig)
# yvalues = rowsofinterest['Extraction %'].tolist()
# xvalues = datan[dependentvariable].tolist()
# trace = go.Scatter(x = xvalues, y = yvalues, mode = 'markers')
# allthedata.append(trace)
#

#

#
#
# howmanyfiles = input('How many files are there? ')
# allthedata = []
# varies = input('What varies? PICK ONE: aql, aqconc, ph, orgl, orgconc, isotope, buffer, bufferconc  > ')
#
# def plotthething():
#     for value in range(int(howmanyfiles)):
#         # Filenames are in this format when they come out of splitLSC.sh
#         datafile = str(value+1)+'.ExperTable.csv'
#         filename = input('What is the filename? (YYYYMMDDisotope_ligand_extractant.csv): ')
#         if varies == 'aql':
#             dependentvariable = 'Ligand'
#         elif varies == 'aqconc':
#             dependentvariable = 'Ligand Concentration (mM)'
#         elif varies == 'ph':
#             dependentvariable = 'Initial pH'
#         elif varies == 'orgl':
#             dependentvariable = 'Extractant'
#         elif varies == 'orgconc':
#             dependentvariable = 'Extractant Concentration (M)'
#         elif varies == 'isotope':
#             dependentvariable = 'Isotope'
#         elif varies == 'buffer':
#             dependentvariable = 'Buffer'
#         elif varies == 'bufferconc':
#             dependentvariable = 'Buffer Concentration (mM)'

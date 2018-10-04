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
datan = pd.read_csv(os.path.join('c:\\Users\\Kathy Shield\\Desktop\\Berkeley\\AbergelGroup\\Research\\Extractions\\Results\\ProcessedDataFiles','data2.csv'))

### pH 6 DATA

relevantdata = datan[(datan['Isotope'] == 'Gd153') &
#(datan['Date'] >= '7/25/2018') &
(datan['Initial pH'] == 6) &
(datan['Extractant Concentration (M)'] == 0.0025)]


CDTA6data = relevantdata[relevantdata['Ligand'] == 'CDTA']
#CDTA6data = CDTA6data.sort_values('Ligand Concentration (mM)')
DTPA6data = relevantdata[relevantdata['Ligand'] == 'DTPA']
#DTPA6data = DTPA6data.sort_values('Ligand Concentration (mM)')
EDTA6data = relevantdata[relevantdata['Ligand'] == 'EDTA']
#EDTA6data = EDTA6data.sort_values('Ligand Concentration (mM)')
DTPMP6data = relevantdata[relevantdata['Ligand'] == 'DTPMP']
#DTPMP6data = DTPMP6data.sort_values('Ligand Concentration (mM)')
EDTPA6data = relevantdata[relevantdata['Ligand'] == 'EDTPA']
#EDTPA6data = EDTPA6data.sort_values('Ligand Concentration (mM)')
PDTA6data = relevantdata[relevantdata['Ligand'] == 'PDTA']
#PDTA6data = PDTA6data.sort_values('Ligand Concentration (mM)')
TTHA6data = relevantdata[relevantdata['Ligand'] == 'TTHA']
#TTHA6data = TTHA6data.sort_values('Ligand Concentration (mM)')


CAM6data = relevantdata[relevantdata['Ligand'] == 'CAM']
#CAM6data = CAM6data.sort_values('Ligand Concentration (mM)')
CHHC6data = relevantdata[relevantdata['Ligand'] == 'CHHC']
#CHHC6data = CHHC6data.sort_values('Ligand Concentration (mM)')
HCCH6data = relevantdata[relevantdata['Ligand'] == 'HCCH']
#HCCH6data = HCCH6data.sort_values('Ligand Concentration (mM)')
HOPO6data = relevantdata[relevantdata['Ligand'] == 'HOPO']
#HOPO6data = HOPO6data.sort_values('Ligand Concentration (mM)')

# number_of_points:  number of samples in one run
# length of the total number of samples; divide by 3; make into an integer
number_of_points = int(len(CDTA6data['Ligand Concentration (mM)'])/3)
# make a list of values of ligand concentration (because the table format isn't nice to us)
xvalues = CDTA6data['Ligand Concentration (mM)'].tolist()
# shorten list of values to only have each value once -- remove the triplicate-ness
# define "xvalues" because these are the x values to plot
xvalues = xvalues[0:number_of_points]
# define an empty list for the y values and the y errors -- we fill them next
yvalues = []
yerror = []
# fill the yvalue and yerror lists
# loop through each entry in xvalues - each ligand concentration
for point in range(0,number_of_points):
    # define "yvalue" as the mean of the triplicate data
    value = CDTA6data.loc[(CDTA6data['Ligand Concentration (mM)'] == xvalues[point]), 'Extraction %'].mean()
    # define yerror as the standard deviation of the triplicate data
    standard_deviation = CDTA6data.loc[(CDTA6data['Ligand Concentration (mM)'] == xvalues[point]), 'Extraction %'].std()
    # add the point and the error into the lists
    yvalues.append(value)
    yerror.append(standard_deviation)
    #this repeats for every value in xvalues
CDTA6plot = go.Scatter(
    x = xvalues,
    y = yvalues,
    mode = 'markers+lines',
    name = 'CDTA, pH 6',
    line = dict(color = "rgba(240,0,0,1)"),
    error_y = dict(
        type = 'data',
        array = yerror,
        visible = 'True',
        color = "rgba(240,0,0,.5)"
        )
)

number_of_points = int(len(DTPA6data['Ligand Concentration (mM)'])/3)
xvalues = DTPA6data['Ligand Concentration (mM)'].tolist()
xvalues = xvalues[0:number_of_points]
yvalues = []
yerror = []

for point in range(0,number_of_points):
    value = DTPA6data.loc[(DTPA6data['Ligand Concentration (mM)'] == xvalues[point]), 'Extraction %'].mean()
    standard_deviation = DTPA6data.loc[(DTPA6data['Ligand Concentration (mM)'] == xvalues[point]), 'Extraction %'].std()
    yvalues.append(value)
    yerror.append(standard_deviation)
DTPA6plot = go.Scatter(
    x = xvalues,
    y = yvalues,
    mode = 'markers+lines',
    name = 'DTPA, pH 6',
    line = dict(color = 'rgba(56,6,156,1)'),
    error_y = dict(
        type = 'data',
        array = yerror,
        visible = 'True',
        color = 'rgba(56,6,156,.5)'
        )
)

number_of_points = int(len(DTPMP6data['Ligand Concentration (mM)']))
xvalues = DTPMP6data['Ligand Concentration (mM)'].tolist()
xvalues = xvalues[0:number_of_points]
yvalues = []
yerror = []

for point in range(0,number_of_points):
    value = DTPMP6data.loc[(DTPMP6data['Ligand Concentration (mM)'] == xvalues[point]), 'Extraction %'].mean()
    standard_deviation = DTPMP6data.loc[(DTPMP6data['Ligand Concentration (mM)'] == xvalues[point]), 'Extraction %'].std()
    yvalues.append(value)
    yerror.append(standard_deviation)
DTPMP6plot = go.Scatter(
    x = xvalues,
    y = yvalues,
    mode = 'markers+lines',
    name = 'DTPMP, pH 6',
    line = dict(color = 'rgba(65,6,165,1)'),
    error_y = dict(
        type = 'data',
        array = yerror,
        visible = 'True',
        color = 'rgba(65,6,165,.5)'
        )
)

number_of_points = int(len(EDTA6data['Ligand Concentration (mM)'])/3)
xvalues = EDTA6data['Ligand Concentration (mM)'].tolist()
xvalues = xvalues[0:number_of_points]
yvalues = []
yerror = []
for point in range(0,number_of_points):
    value = EDTA6data.loc[(EDTA6data['Ligand Concentration (mM)'] == xvalues[point]), 'Extraction %'].mean()
    standard_deviation = EDTA6data.loc[(EDTA6data['Ligand Concentration (mM)'] == xvalues[point]), 'Extraction %'].std()
    yvalues.append(value)
    yerror.append(standard_deviation)
EDTA6plot = go.Scatter(
    x = xvalues,
    y = yvalues,
    mode = 'markers+lines',
    name = 'EDTA, pH 6',
    line = dict(color = 'rgba(124,3,83,1)'),
    error_y = dict(
        type = 'data',
        array = yerror,
        visible = 'True',
        color = 'rgba(124,3,83,.5)'
        )
)

number_of_points = int(len(EDTPA6data['Ligand Concentration (mM)']))
xvalues = EDTPA6data['Ligand Concentration (mM)'].tolist()
xvalues = xvalues[0:number_of_points]
yvalues = []
yerror = []
for point in range(0,number_of_points):
    value = EDTPA6data.loc[(EDTPA6data['Ligand Concentration (mM)'] == xvalues[point]), 'Extraction %'].mean()
    standard_deviation = EDTPA6data.loc[(EDTPA6data['Ligand Concentration (mM)'] == xvalues[point]), 'Extraction %'].std()
    yvalues.append(value)
    yerror.append(standard_deviation)
EDTPA6plot = go.Scatter(
    x = xvalues,
    y = yvalues,
    mode = 'markers+lines',
    name = 'EDTPA, pH 6',
    line = dict(color = 'rgba(142,3,83,1)'),
    error_y = dict(
        type = 'data',
        array = yerror,
        visible = 'True',
        color = 'rgba(142,3,83,.5)'
        )
)

PDTA6plot = go.Scatter(
    x = PDTA6data['Ligand Concentration (mM)'],
    y = PDTA6data['Extraction %'],
    mode = 'markers',
    name = 'PDTA, pH 6',
    line = dict(color = 'rgba(250,100,30,1)'),
    error_y = dict(
        type = 'data',
        array = yerror,
        visible = 'True'
        )
)
number_of_points = int(len(TTHA6data['Ligand Concentration (mM)'])/3)
xvalues = TTHA6data['Ligand Concentration (mM)'].tolist()
xvalues = xvalues[0:number_of_points]
yvalues = []
yerror = []
for point in range(0,number_of_points):
    value = TTHA6data.loc[(TTHA6data['Ligand Concentration (mM)'] == xvalues[point]), 'Extraction %'].mean()
    standard_deviation = TTHA6data.loc[(TTHA6data['Ligand Concentration (mM)'] == xvalues[point]), 'Extraction %'].std()
    yvalues.append(value)
    yerror.append(standard_deviation)
TTHA6plot = go.Scatter(
    x = xvalues,
    y = yvalues,
    mode = 'markers+lines',
    name = 'TTHA, pH 6',
    line = dict(color = 'rgba(71,51,30,1)'),
    error_y = dict(
        type = 'data',
        array = yerror,
        visible = 'True',
        color = 'rgba(71,51,30,.5)'
        )
)

CAM6plot = go.Scatter(
    x = CAM6data['Ligand Concentration (mM)'],
    y = CAM6data['Extraction %'],
    mode = 'markers',
    name = 'CAM, pH 6',
    line = dict(color = 'rgba(76,178,76,1)'),
    error_y = dict(
        type = 'data',
        array = yerror,
        visible = 'True'
        )
)
number_of_points = int(len(CHHC6data['Ligand Concentration (mM)'])/3)
xvalues = CHHC6data['Ligand Concentration (mM)'].tolist()
xvalues = xvalues[0:number_of_points]
yvalues = []
yerror = []
for point in range(0,number_of_points):
    value = CHHC6data.loc[(CHHC6data['Ligand Concentration (mM)'] == xvalues[point]), 'Extraction %'].mean()
    standard_deviation = CHHC6data.loc[(CHHC6data['Ligand Concentration (mM)'] == xvalues[point]), 'Extraction %'].std()
    yvalues.append(value)
    yerror.append(standard_deviation)
CHHC6plot = go.Scatter(
    x = xvalues,
    y = yvalues,
    mode = 'markers+lines',
    name = 'CHHC, pH 6',
    line = dict(color = 'rgba(16,136,102,1)'),
    error_y = dict(
        type = 'data',
        array = yerror,
        visible = 'True',
        color = 'rgba(16,136,102,.5)'
        )
)
number_of_points = int(len(HCCH6data['Ligand Concentration (mM)'])/3)
xvalues = HCCH6data['Ligand Concentration (mM)'].tolist()
xvalues = xvalues[0:number_of_points]
yvalues = []
yerror = []
for point in range(0,number_of_points):
    value = HCCH6data.loc[(HCCH6data['Ligand Concentration (mM)'] == xvalues[point]), 'Extraction %'].mean()
    standard_deviation = HCCH6data.loc[(HCCH6data['Ligand Concentration (mM)'] == xvalues[point]), 'Extraction %'].std()
    yvalues.append(value)
    yerror.append(standard_deviation)
HCCH6plot = go.Scatter(
    x = xvalues,
    y = yvalues,
    mode = 'markers+lines',
    name = 'HCCH, pH 6',
    line = dict(color = 'rgba(105,178,231,1)'),
    error_y = dict(
        type = 'data',
        array = yerror,
        visible = 'True',
        color = 'rgba(105,178,231,.5)'
        )
)

number_of_points = int(len(HOPO6data['Ligand Concentration (mM)'])/2)
xvalues = HOPO6data['Ligand Concentration (mM)'].tolist()
xvalues = xvalues[0:number_of_points]
yvalues = []
yerror = []
for point in range(0,number_of_points):
    value = HOPO6data.loc[(HOPO6data['Ligand Concentration (mM)'] == xvalues[point]), 'Extraction %'].mean()
    standard_deviation = HOPO6data.loc[(HOPO6data['Ligand Concentration (mM)'] == xvalues[point]), 'Extraction %'].std()
    yvalues.append(value)
    yerror.append(standard_deviation)
HOPO6plot = go.Scatter(
    x = xvalues,
    y = yvalues,
    mode = 'markers+lines',
    name = 'HOPO, pH 6',
    line = dict(color = 'rgba(16,54,207,1)'),
    error_y = dict(
        type = 'data',
        array = yerror,
        visible = 'True',
        color = 'rgba(16,54,207,.5)'
        )
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

data = [CDTA6plot,DTPA6plot,EDTA6plot,PDTA6plot,TTHA6plot,DTPMP6plot,EDTPA6plot,
#CDTA7plot, DTPA7plot, EDTA7plot, PDTA7plot,
CAM6plot,CHHC6plot,HCCH6plot,HOPO6plot
]

layout = go.Layout(
xaxis = dict(
    type = 'log',
    autorange = True,
    rangemode ="tozero",
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
title='Extractions',
showlegend = True
)


fig = go.Figure(data=data, layout=layout)
#
#py.offline.plot(fig)
plot = py.offline.plot(fig, image = 'png')
programfilename = os.path.join('C:/Users/Kathy Shield/Desktop','plot_image.png').replace('\\','/')
print (programfilename)
newfilename = os.path.join('C:/Users/Kathy Shield/Desktop/Berkeley/AbergelGroup/Research/Extractions/Results/Images','Gd153TriplicateData2'+'.png').replace('\\','/')
print (newfilename)
os.rename(programfilename, newfilename)
if os.path.exists(programfilename):
    os.remove(programfilename)
print ('file removed')

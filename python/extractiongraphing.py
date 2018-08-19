#!/c/Users/Public/python

# For making graphs with multiple inputs

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


# Which ligands are we graphing today?
potential_ligands = ['CDTA', 'DTPA', 'EDTA', 'PDTA', 'TTHA', 'DTPMP', 'EDTPA', 'CAM', 'CHHC', 'HCCH', 'HOPO']
allligands = input ('Do you want to graph all possible ligands? (y/n): ')
if allligands == 'y':
    graphed_ligands = potential_ligands
    ligand_colors = ['rgba(240,0,0,', 'rgba(56,6,156,', 'rgba(124,3,83,', 'rgba(250,100,30,', 'rgba(71,51,30,', 'rgba(164,125,242,', 'rgba(242,116,199,', 'rgba(76,178,76,', 'rgba(16,136,102,', 'rgba(105,178,231,', 'rgba(16,54,207,']
else:
    graphed_ligands = []
    ligand_colors = []
    for ligand in potential_ligands:
        ligand_yes = input ('Do you want to graph ' + ligand + '? (y/n): ')
        if ligand_yes == 'y':
            graphed_ligands.append(ligand)
            if ligand == 'CDTA':
                ligand_colors.append('rgba(240,0,0,')
            elif ligand == 'DTPA':
                ligand_colors.append('rgba(56,6,156,')
            elif ligand == 'EDTA':
                ligand_colors.append('rgba(124,3,83,')
            elif ligand == 'PDTA':
                ligand_colors.append('rgba(250,100,30,')
            elif ligand == 'TTHA':
                ligand_colors.append('rgba(71,51,30,')
            elif ligand == 'DTPMP':
                ligand_colors.append('rgba(164,125,242,')
            elif ligand == 'EDTPA':
                ligand_colors.append('rgba(242,116,199,')
            elif ligand == 'HOPO':
                ligand_colors.append('rgba(16,54,207,')
            elif ligand == 'CHHC':
                ligand_colors.append('rgba(16,136,102,')
            elif ligand == 'HCCH':
                ligand_colors.append('rgba(105,178,231,')
            elif ligand == 'CAM':
                ligand_colors.append('rgba(76,178,76,')


# Which isotopes are we graphing today?

# Warning about data
print ('This script only incorporates pH 6 data; if you want other pH values, go elsewhere.')

# Actually plotting the thing
graphdata = []
for ligand in graphed_ligands:
    indexnumber = graphed_ligands.index(ligand)
    linecolor = ligand_colors[indexnumber]
    liganddata = datan[(datan['Ligand'] == ligand) & (datan['Initial pH'] == 6) & (datan['Extractant Concentration (M)'] == 0.0025) & (datan['Exclude Me'] != 'y')]
    liganddata.sort_values('Ligand Concentration (mM)', inplace = True)
    xvalues_all = liganddata['Ligand Concentration (mM)'].unique().tolist()
    xvalues = []
    yvalues = []
    yerror = []
    # figuring out how many data points are in triplicate
    numberofentries = liganddata.groupby('Ligand Concentration (mM)').size().tolist()
    triplicatedataexists = []
    for point in range(0,len(xvalues_all)):
    #if the data is in triplicate or more:
        if numberofentries[point] >= 3:
            value = liganddata.loc[(liganddata['Ligand Concentration (mM)'] == xvalues_all[point]), 'Extraction %'].mean()
            standard_deviation = liganddata.loc[(liganddata['Ligand Concentration (mM)'] == xvalues_all[point]), 'Extraction %'].std()
            xvalues.append(xvalues_all[point])
            yvalues.append(value)
            yerror.append(standard_deviation)
            triplicatedataexists.append(point)
    if len(triplicatedataexists) >= 1:
        trace = go.Scatter(
            x = xvalues,
            y = yvalues,
            mode = 'markers+lines',
            name = ligand,
            line = dict(color = linecolor+'1)'),
            error_y = dict(
                type = 'data',
                array = yerror,
                visible = 'True',
                color = linecolor+'.5)'
                )
            )
        graphdata.append(trace)
    else:
        xvalues = xvalues_all
        yvalues = liganddata['Extraction %']
        trace = go.Scatter(
            x = xvalues,
            y = yvalues,
            mode = 'markers+lines',
            name = ligand+ '*',
            line = dict(color = linecolor+'1)')
            )
        graphdata.append(trace)


    # if no data exists in triplicate, plot the single data that exists with no error bars

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
            range = [0,1.1],
            title = 'Extraction Percent',
            showgrid = True,
            showline = True
        ),
        title = 'Extraction into HDEHP with varying Ligands'
    )
    fig = go.Figure(data=graphdata, layout=layout)
plot = py.offline.plot(fig, image = 'png')

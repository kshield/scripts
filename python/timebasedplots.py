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
potential_ligands = ['CDTA', 'DTPA', 'EDTA', 'PDTA', 'TTHA', 'EDTPA']
# Ligand colors list
CDTAcolor = 'rgba(245,130,48,'
DTPAcolor = 'rgba(128,0,0,'
EDTAcolor = 'rgba(0,130,200,'
PDTAcolor = 'rgba(240,50,230,'
TTHAcolor = 'rgba(230,25,75,'
DTPMPcolor = 'rgba(0,128,128,'
EDTPAcolor = 'rgba(0,0,128,'
CAMcolor = 'rgba(250,190,190,'
CHHCcolor = 'rgba(70,240,240,'
HCCHcolor = 'rgba(145,30,180,'
HOPOcolor = 'rgba(60,180,75,'
allligands = input ('Do you want to graph all possible ligands? (y/n): ')
triplicateorno = input ('For n>=3 data, show average and error bars or individual points? (average/individual): ')
if allligands == 'y':
    graphed_ligands = potential_ligands
    ligand_colors = [CDTAcolor, DTPAcolor, EDTAcolor, PDTAcolor, TTHAcolor, DTPMPcolor, EDTPAcolor, CAMcolor, CHHCcolor, HCCHcolor, HOPOcolor]
else:
    graphed_ligands = []
    ligand_colors = []
    for ligand in potential_ligands:
        ligand_yes = input ('Do you want to graph ' + ligand + '? (y/n): ')
        if ligand_yes == 'y':
            graphed_ligands.append(ligand)
            #ligand_colors.append(ligand+'color')
            if ligand == 'CDTA':
                ligand_colors.append('rgba(245,130,48,')
            elif ligand == 'DTPA':
                ligand_colors.append('rgba(128,0,0,')
            elif ligand == 'EDTA':
                ligand_colors.append('rgba(0,130,200,')
            elif ligand == 'PDTA':
                ligand_colors.append('rgba(240,50,230,')
            elif ligand == 'TTHA':
                ligand_colors.append('rgba(230,25,75,')
            elif ligand == 'DTPMP':
                ligand_colors.append('rgba(0,128,128,')
            elif ligand == 'EDTPA':
                ligand_colors.append('rgba(0,0,128,')
            elif ligand == 'CAM':
                ligand_colors.append('rgba(250,190,190,')
            elif ligand == 'CHHC':
                ligand_colors.append('rgba(70,240,240,')
            elif ligand == 'HCCH':
                ligand_colors.append('rgba(145,30,180,')
            elif ligand == 'HOPO':
                ligand_colors.append('rgba(60,180,75,')


# Which isotopes are we graphing today?

# Warning about data
print ('This script only incorporates pH 6 data; if you want other pH values, go elsewhere.')

# Actually plotting the thing
graphdata = []
for ligand in graphed_ligands:
    #original data
    indexnumber = graphed_ligands.index(ligand)
    linecolor = ligand_colors[indexnumber]
    liganddata = datan[(datan['Ligand'] == ligand) &
    (datan['Isotope'] == 'Gd153') &
    (datan['Initial pH'] == 6) &
    (datan['Extractant Concentration (M)'] == 0.0025) &
    (datan['Exclude Me'] != 'y')]
    liganddata.sort_values('Ligand Concentration (mM)', inplace = True)
    xvalues_all = liganddata['Ligand Concentration (mM)'].unique().tolist()
    xvalues = []
    yvalues = []
    yerror = []
    # figuring out how many data points are in triplicate
    numberofentries = liganddata.groupby('Ligand Concentration (mM)').size().tolist()
    if triplicateorno == 'average':
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
    #24 hour data
    indexnumber = graphed_ligands.index(ligand)
    linecolor = ligand_colors[indexnumber]
    liganddata = datan[(datan['Ligand'] == ligand+'-') &
    (datan['Isotope'] == 'Gd153') &
    (datan['Initial pH'] == 6) &
    (datan['Extractant Concentration (M)'] == 0.0025) &
    (datan['Exclude Me'] != 'y')]
    liganddata.sort_values('Ligand Concentration (mM)', inplace = True)
    xvalues_all = liganddata['Ligand Concentration (mM)'].unique().tolist()
    xvalues = []
    yvalues = []
    yerror = []
    # figuring out how many data points are in triplicate
    numberofentries = liganddata.groupby('Ligand Concentration (mM)').size().tolist()
    if triplicateorno == 'average':
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
                mode = 'markers',
                name = ligand+' 24 hr',
                line = dict(color = linecolor+'1)'),
                marker = dict(
                    color = linecolor+'1)',
                    size = 10,
                    line = dict(
                        color = 'rgb(250,190,190)',
                        width = 2
                        )
                    ),
                error_y = dict(
                    type = 'data',
                    array = yerror,
                    visible = 'True',
                    color = linecolor+'.5)'
                    )
                )
            graphdata.append(trace)
    #45 min data
    indexnumber = graphed_ligands.index(ligand)
    linecolor = ligand_colors[indexnumber]
    liganddata = datan[(datan['Ligand'] == ligand+'--') &
    (datan['Isotope'] == 'Gd153') &
    (datan['Initial pH'] == 6) &
    (datan['Extractant Concentration (M)'] == 0.0025) &
    (datan['Exclude Me'] != 'y')]
    liganddata.sort_values('Ligand Concentration (mM)', inplace = True)
    xvalues_all = liganddata['Ligand Concentration (mM)'].unique().tolist()
    xvalues = []
    yvalues = []
    yerror = []
    # figuring out how many data points are in triplicate
    numberofentries = liganddata.groupby('Ligand Concentration (mM)').size().tolist()
    if triplicateorno == 'average':
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
                mode = 'markers',
                name = ligand+' 45 min',
                line = dict(color = linecolor+'1)'),
                marker = dict(
                    color = linecolor+'1)',
                    size = 10,
                    line = dict(
                        color = 'rgb(70,240,240)',
                        width = 2
                        )
                    ),
                error_y = dict(
                    type = 'data',
                    array = yerror,
                    visible = 'True',
                    color = linecolor+'.5)'
                    )
                )
            graphdata.append(trace)
    #15 min data
    indexnumber = graphed_ligands.index(ligand)
    linecolor = ligand_colors[indexnumber]
    liganddata = datan[(datan['Ligand'] == ligand+'---') &
    (datan['Isotope'] == 'Gd153') &
    (datan['Initial pH'] == 6) &
    (datan['Extractant Concentration (M)'] == 0.0025) &
    (datan['Exclude Me'] != 'y')]
    liganddata.sort_values('Ligand Concentration (mM)', inplace = True)
    xvalues_all = liganddata['Ligand Concentration (mM)'].unique().tolist()
    xvalues = []
    yvalues = []
    yerror = []
    # figuring out how many data points are in triplicate
    numberofentries = liganddata.groupby('Ligand Concentration (mM)').size().tolist()
    if triplicateorno == 'average':
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
                mode = 'markers',
                name = ligand+' 15 min',
                line = dict(color = linecolor+'1)'),
                marker = dict(
                    color = linecolor+'1)',
                    size = 10,
                    line = dict(
                        color = 'rgb(231, 99, 250)',
                        width = 2
                        )
                    ),
                error_y = dict(
                    type = 'data',
                    array = yerror,
                    visible = 'True',
                    color = linecolor+'.5)'
                    )
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
        legend = dict(
            font = dict(
                size = 18
            )
        ),
        title = 'Extraction into HDEHP with varying Ligands'
    )
    fig = go.Figure(data=graphdata, layout=layout)
plot = py.offline.plot(fig, image = 'png')

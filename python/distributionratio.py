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
from sklearn.metrics import mean_squared_error, r2_score
from scipy import stats
py.tools.set_credentials_file(username = 'kshield', api_key = 'H9UX6nYroLdbt1W1pjgj')

# Open the data table
datan = pd.read_csv(os.path.join('c:\\Users\\Kathy Shield\\Desktop\\Berkeley\\AbergelGroup\\Research\\Extractions\\Results\\ProcessedDataFiles','allthedata.csv'))

# Define the isotopes being used #
isotope = 'Gd153' # Only using Gd153 for now; copy code from extractionanalysis to use multiple ligands
graphed_isotopes = [isotope]

# Define the ligands being used  #
potential_ligands = ['CDTA', 'DTPA', 'EDTA', 'PDTA', 'TTHA', #'DTPMP',
'EDTPA', #'CAM',
'CHHC', 'HCCH', 'HOPO']
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
if allligands == 'y':
    graphed_ligands = potential_ligands
    ligand_colors = [CDTAcolor, DTPAcolor, EDTAcolor, PDTAcolor, TTHAcolor, #DTPMPcolor,
    EDTPAcolor, #CAMcolor,
    CHHCcolor, HCCHcolor, HOPOcolor]
else:
    graphed_ligands = []
    ligand_colors = []
    for ligand in potential_ligands:
        ligand_yes = input ('Do you want to graph ' + ligand + '? (y/n): ')
        if ligand_yes == 'y':
            graphed_ligands.append(ligand)
            #ligand_colors.append(string(ligand)+'color')
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

datan['Date'] = datan.Date
date = datetime.datetime.strptime(datan.loc[0,'Date'],'%m/%d/%Y').strftime('%Y%m%d')

graphdata = []
for ligand in graphed_ligands:
    ligandindex = graphed_ligands.index(ligand)
    linecolor = ligand_colors[ligandindex]
    liganddata = datan[(datan['Ligand'] == ligand) &
    (datan['Isotope'] == isotope) &
    (datan['Initial pH'] == 6) &
    (datan['Extractant Concentration (M)'] == 0.0025) &
    #(datan['Date'] >= '10/10/2018') & (datan['Date'] <= '10/11/2018') &
    (datan['Exclude Me'] != 'y')]
    liganddata.sort_values('Ligand Concentration (mM)', inplace = True)
    xvalues_all = liganddata['Ligand Concentration (mM)'].unique().tolist()
    xvalues = []
    yvalues = []
    yerror = []
    numberofentries = liganddata.groupby('Ligand Concentration (mM)').size().tolist()
    for point in range(0,len(xvalues_all)):
        if numberofentries[point] >= 3:
            distribution_ratios = []

            ## EXTRACT THE CPM VALUES & TAKE lOG_10 ##
            ## (THE LOG VALUES MUST BE PLOTTED BECAUSE STRAIGHT LINES CANNOT BE PLOTTED ON A
            ## LOG/LOG SCALE; USING LIN/LIN SCALES INSTEAD REQUIRES PRE-LOGGING THE VALUES TO PLOT)
            aqueousCPM = liganddata.loc[(liganddata['Ligand Concentration (mM)'] == xvalues_all[point]), 'AqCPM']
            aqueousCPM = np.log10(aqueousCPM)
            organicCPM = liganddata.loc[(liganddata['Ligand Concentration (mM)'] == xvalues_all[point]), 'OrgCPM']
            organicCPM = np.log10(organicCPM)

            ## DETERMINE THE DISTRIBUTION RATIOS ##
            distribution_ratio = organicCPM/aqueousCPM
            #if distribution_ratio = -inf or inf
            distribution_ratios.append(distribution_ratio)
            distribution_ratios = np.array(distribution_ratios)

            ## REMOVE DATA POINTS EQUAL TO +/- INFINITY ##

            ## TAKE THE AVERAGE & STANDARD DEVIATION OF DISTRIBUTION RATIOS ##
            value = np.mean(distribution_ratios)
            standard_deviation = distribution_ratios.std()

            ## TAKE THE LOG_10 OF EACH CONCENTRATION ##
            logx = np.log10(xvalues_all[point])
            xvalues.append(logx)
            yvalues.append(value)
            yerror.append(standard_deviation)
    print(xvalues, yvalues)

    ##### MAKE THE PLOT OF POINTS & ERRORS #####
    trace = go.Scatter(
        x = xvalues,
        y = yvalues,
        name = ligand,
        mode = 'markers',
        marker = dict(
            color = linecolor+'1)'
        ),
        hoverinfo = 'distribution_ratio',
        error_y = dict(
            type = 'data',
            array = yerror,
            visible = 'True',
            color = linecolor+'.5)'
            )
    )
    graphdata.append(trace)


    ###### CALCULATE THE LINEAR REGRESSION #####
    slope, intercept, r_value, p_value, std_err = stats.linregress(xvalues, yvalues)
    xvalues = np.array(xvalues)

    ### DEFINE BEGINNING AND END POINTS FOR THE LINEAR REGRESSION PLOT ###
    x1 = (-10)*np.amax(xvalues)
    x2 = 10*np.amax(xvalues)
    y1 = slope*x1 + intercept
    y2 = slope*x2 + intercept
    line_x = [x1, x2]
    line_y = [y1, y2]

    ### PLOT THE LINEAR REGRESSION ###
    regline = go.Scatter(
        x = line_x,
        y = line_y,
        mode = 'lines',
        line = dict(
            color = linecolor+'1)'
        ),
        name = 'y ='+str(slope)+'x +'+str(intercept)
    )
    graphdata.append(regline)

##### DESIGN AND PRINT THE PLOT ####
layout = go.Layout(
    title = 'Distribution Ratios',
    xaxis = dict(
        type = 'lin',
        autorange = False,
        #domain = [0,1],
        range = [-5,2.5],
        title = 'log([Ligand (mM)])',
        showgrid = True,
        showline = True,
        exponentformat = 'e',
        #nticks = 5
        tick0 = -4,
        dtick = 1
    ),
    yaxis = dict(
        type = 'lin',
        autorange = False,
    #    domain = [0,1],
        range = [-0.5,5.5],
        title = 'log(D)',
        showgrid = True,
        showline = True
    ))
fig = go.Figure(data=graphdata, layout=layout)
plot = py.offline.plot(fig, image = 'png')

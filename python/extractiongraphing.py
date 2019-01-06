#!/c/Users/Public/python

# For making graphs with multiple inputs

import os
import pandas as pd
import numpy as np
import datetime
import warnings
warnings.filterwarnings("ignore")
import csv
import plotly as py
import plotly.graph_objs as go
py.tools.set_credentials_file(username = 'kshield', api_key = 'H9UX6nYroLdbt1W1pjgj')

datan = pd.read_csv(os.path.join('c:\\Users\\Kathy Shield\\Desktop\\Berkeley\\AbergelGroup\\Research\\Extractions\\Results\\ProcessedDataFiles','allthedata.csv'))

# Are we plotting triplicate data or individual points?
triplicateorno = input ('For n>=3 data, show average and error bars (normalized) or individual points (true extraction data)? (average/individual): ')

# ---------------------------- SELECTING THE DATA TO PLOT  ------------------------------


# --------------------- LIGANDS -----------------------

potential_ligands = ['CDTA', 'DTPA', 'EDTA', 'PDTA', 'TTHA', 'DTPMP', 'EDTPA', 'CAM', 'CHHC', 'HCCH', 'HOPO', 'bacillibactin']
# Ligand colors list
CDTAcolor = 'rgba(245,130,48,'
DTPAcolor = 'rgba(128,0,0,'
EDTAcolor = 'rgba(0,130,200,'
PDTAcolor = 'rgba(240,50,230,'
TTHAcolor = 'rgba(230,25,75,'
DTPMPcolor = 'rgba(241,73,35,'
EDTPAcolor = 'rgba(0,0,128,'
CAMcolor = 'rgba(250,190,190,'
CHHCcolor = 'rgba(70,240,240,'
HCCHcolor = 'rgba(145,30,180,'
HOPOcolor = 'rgba(60,180,75,'
bbactincolor = HCCHcolor
allligands = input ('Do you want to graph all possible ligands? (y/n): ')
if allligands == 'y':
    graphed_ligands = potential_ligands
    ligand_colors = [CDTAcolor, DTPAcolor, EDTAcolor, PDTAcolor, TTHAcolor, DTPMPcolor, EDTPAcolor, CAMcolor, CHHCcolor, HCCHcolor, HOPOcolor, bbactincolor]
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
                ligand_colors.append('rgba(241,73,35,')
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
            elif ligand == 'bacillibactin':
                ligand_colors.append('rgba(145,30,180,')

# --------------------- ISOTOPES --------------------------
potential_isotopes = ['Ac227','Ce134','Gd153','Lu177','Ac227 Daughters','La134']
# Isotope line format list
Ac227line = 'dot'
Gd153line = ''
Lu177line = 'dash'
Ce134line = 'longdash'
allisotopes = input ('Do you want to graph all possible isotopes? (y/n): ')
if allisotopes == 'y':
    includedaughters = input ('Graph daughters too? (y/n): ')
    if includedaughters == 'y':
        graphed_isotopes = potential_isotopes
        isotope_lines = [Ac227line, Gd153line, Lu177line, Ac227line, Gd153line]
        isotope_markers = ['circle','square','diamond','triangle','x','star']
    elif includedaughters =='n':
        graphed_isotopes = potential_isotopes
        isotope_lines = [Ac227line, Gd153line, Lu177line]
        isotope_markers = ['circle','square','diamond','triangle']
else:
    graphed_isotopes = []
    isotope_lines = []
    isotope_markers = []
    for isotope in potential_isotopes:
        isotope_yes = input ('Do you want to graph '+isotope+'? (y/n): ')
        if isotope_yes == 'y':
            graphed_isotopes.append(isotope)
            if isotope == 'Ac227':
                isotope_lines.append('dot')
                isotope_markers.append('circle')
            elif isotope == 'Gd153':
                isotope_lines.append('')
                isotope_markers.append('square')
            elif isotope == 'Lu177':
                isotope_lines.append('dash')
                isotope_markers.append('diamond')
            elif isotope == 'Ce134':
                isotope_lines.append('longdash')
                isotope_markers.append('triangle')
            elif isotope == 'Ac227 Daughters':
                isotope_lines.append('dot')
                isotope_markers.append('x')
            elif isotope == 'Ce134 Daughters':
                isotope_lines.append('longdash')
                isotope_markers.append('star')

# ------------------------------ pH VALUES ------------------------
potential_pH = ['6','7','7.4']
pH6marker = 'circle'
pH7marker = 'square'
pH7_4marker = 'diamond'
desiredpH = input ('Do you want to graph all possible pH values? (y/n): ')
if desiredpH == 'y':
    graphed_pH = float(potential_pH)
    pH_markers = [pH6marker, pH7marker, pH7_4marker]
else:
    graphed_pH = []
    pH_markers = []
    for pHstring in potential_pH:
        pH_yes = input ('Do you want to graph '+pHstring+'? (y/n): ')
        pH = float(pHstring)
        if pH_yes == 'y':
            graphed_pH.append(pH)
            if pH == 6:
                pH_markers.append('circle')
            elif pH == 7:
                pH_markers.append('square')
            elif pH == 7.4:
                pH_markers.append('diamond')

# --------------------------------- EXTRACTING THE DATA ---------------------------------

datan['Date'] = datan.Date
date = datetime.datetime.strptime(datan.loc[0,'Date'],'%m/%d/%Y').strftime('%Y%m%d')
graphtitle = input ('Please Input the Desired title: ')
# Actually plotting the thing
graphdata = []
linetype = []
for isotope in graphed_isotopes:
    isotopeindex = graphed_isotopes.index(isotope)
    linetype = isotope_lines[isotopeindex]
    markershape = isotope_markers[isotopeindex]
    for ligand in graphed_ligands:
        ligandindex = graphed_ligands.index(ligand)
        linecolor = ligand_colors[ligandindex]
        for pH in graphed_pH:
            liganddata = datan[(datan['Ligand'] == ligand) &
            (datan['Isotope'] == isotope) &
            (datan['Initial pH'] == pH) &
            (datan['Extractant Concentration (M)'] == 0.0025) &
            #(datan['Date'] >= '10/10/2018') & (datan['Date'] <= '10/11/2018') &
            (datan['Exclude Me'] != 'y')]
            liganddata.sort_values('Ligand Concentration (mM)', inplace = True)
            xvalues_all = liganddata['Ligand Concentration (mM)'].unique().tolist()
            xvalues = []
            yvalues = []
            yerror = []
            xvaluessingle = []
            yvaluessingle = []
            yerrorsingle = []
            pHname = str(pH)
            # figuring out how many data points are in triplicate
            numberofentries = liganddata.groupby('Ligand Concentration (mM)').size().tolist()
            if triplicateorno == 'average':
                triplicatedataexists = []
                for point in range(0,len(xvalues_all)):
                #if the data is in triplicate or more:
                    if numberofentries[point] >= 3:
                        maxvalue = liganddata.iloc[0]['Extraction %']
                        value = liganddata.loc[(liganddata['Ligand Concentration (mM)'] == xvalues_all[point]), 'Extraction %'].mean()
                        normalizedvalue = value/maxvalue
                        standard_deviation = liganddata.loc[(liganddata['Ligand Concentration (mM)'] == xvalues_all[point]), 'Extraction %'].std()
                        normalizedstandard_deviation = standard_deviation/maxvalue
                        xvalues.append(xvalues_all[point])
                        yvalues.append(normalizedvalue)
                        yerror.append(normalizedstandard_deviation)
                        triplicatedataexists.append(point)
                    elif numberofentries[point] <= 2:
                        liganddata = liganddata.sort_values(by=['Extraction %'], ascending=False)
                        maxvalue = liganddata.iloc[0]['Extraction %']
                        value = liganddata.loc[(liganddata['Ligand Concentration (mM)'] == xvalues_all[point]), 'Extraction %'].mean()
                        normalizedvalue = value/maxvalue
                        standard_deviation = liganddata.loc[(liganddata['Ligand Concentration (mM)'] == xvalues_all[point]), 'Extraction %'].std()
                        xvaluessingle.append(xvalues_all[point])
                        yvaluessingle.append(normalizedvalue)
                        yerrorsingle.append(standard_deviation)
                if len(triplicatedataexists) >= 1:
                    trace = go.Scatter(
                        x = xvalues,
                        y = yvalues,
                        mode = 'markers+lines',
                        name = ligand+'-'+isotope,
                        line = dict(color = linecolor+'1)', dash = linetype),
                        marker = dict(color = linecolor+'1)', symbol = markershape, size = 10),
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
                        x = xvaluessingle,
                        y = yvaluessingle,
                        error_y = dict(
                            type = 'data',
                            array = yerrorsingle,
                            visible = 'True',
                            color = linecolor+'.5)'
                            ),
                        mode = 'markers+lines',
                        name = ligand+'-'+isotope,
                        line = dict(color = linecolor+'1)', dash = linetype),
                        marker = dict(color = linecolor+'1)', symbol = markershape, size = 10),
                        )
                    graphdata.append(trace)
            if triplicateorno == 'individual':
                datecolors = input ('Should individual dates of'+ligand+' + '+isotope+' + '+pHname+' get different colors? (y/n): ')
                if datecolors == 'n':
                    xvalues = liganddata['Ligand Concentration (mM)'].tolist()
                    yvalues = liganddata['Extraction %'].tolist()
                    trace = go.Scatter(
                        x = xvalues,
                        y = yvalues,
                        mode = 'markers+lines',
                        name = ligand+'-'+isotope,
                        line = dict(color = linecolor+'1)', dash = linetype),
                        marker = dict(color = linecolor+'1)', symbol = markershape, size = 10),
                        )
                    graphdata.append(trace)
                elif datecolors == 'y':
                    dates_all = liganddata['Date'].unique().tolist()
                    #print (dates_all)
                    for date in dates_all:
                        datespecificdata = liganddata[(liganddata['Date'] == date)]
                        xvalues = datespecificdata['Ligand Concentration (mM)'].tolist()
                        yvalues = datespecificdata['Extraction %'].tolist()
                        trace = go.Scatter(
                            x = xvalues,
                            y = yvalues,
                            mode = 'markers+lines',
                            name = ligand+'-'+isotope+', '+pHname+': '+ date,
                            line = dict(dash = linetype),
                            marker = dict(symbol = markershape, size = 10)
                            )
                        graphdata.append(trace)
            # if no data exists in triplicate, plot the single data that exists with no error bars

# ------------------------------------- DESIGNING THE PLOT --------------------------------

            layout = go.Layout(
                title = graphtitle,
                    titlefont = dict(
                        family = 'Georgia',
                        size = 30
                    ),
                xaxis = dict(
                    type = 'log',
                    #autorange = True,
                    domain = [0,1],
                    range = [-5.2,3],
                    title = 'Ligand Concentration (mM)',
                    titlefont = dict(
                        family = 'Georgia',
                        size = 22
                    ),
                    tickfont = dict(
                        family = 'Georgia',
                        size = 22
                    ),
                    showgrid = True,
                    showline = True,
                    exponentformat = 'e',
                    tick0 = -4,
                    dtick = 1),
                yaxis = dict(
                    type = 'linear',
                    autorange = False,
                    domain = [0,1],
                    range = [0,1.1],
                    title = 'Relative Extraction',
                    titlefont = dict(
                        family = 'Georgia',
                        size = 22
                    ),
                    tickfont = dict(
                        family = 'Georgia',
                        size = 22
                    ),
                    showgrid = True,
                    showline = True),
                legend = dict(
                    font = dict(
                        family = 'Georgia',
                        size = 14
                    ),
                    orientation = 'h',
                    xanchor = 'center',
                    x = 0.5,
                    y = 1.05
                )
            )
    fig = go.Figure(data=graphdata, layout=layout)
plot = py.offline.plot(fig, image = 'png')

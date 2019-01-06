#!/c/Users/Public/python

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

# functions needed
# Step 1
def pH_select():
    potential_pH = ['6','7','7.4']
    pH6marker = 'circle'
    pH7marker = 'square'
    pH7_4marker = 'diamond'
    desiredpH = input ('Are you looking at just pH 6 data? (y/n): ')
    if desiredpH == 'y':
        graphed_pH = [6]
        pH_markers = [pH6marker]
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
    print ('pH_select')
    return (graphed_pH, pH_markers)
# Step 2
def isotope_select():
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
            isotope_lines = [Ac227line, Ce134line, Gd153line, Lu177line, Ac227line, Gd153line]
            isotope_markers = ['circle','square','diamond','triangle','x','star']
        elif includedaughters =='n':
            graphed_isotopes = potential_isotopes[0:3]
            isotope_lines = [Ac227line, Ce134line, Gd153line, Lu177line]
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
    print ('ran isotope_select')
    return (isotope_markers, isotope_lines, graphed_isotopes)
# Step 3
def ligand_select():
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
    print ('ran ligand_select')
    return (graphed_ligands, ligand_colors)
# Step 4
def extractdata(graphed_isotopes, graphed_ligands, graphed_pH):
    liganddata = datan[(datan['Initial pH'] == pH) &
    (datan['Ligand'] == ligand) &
    (datan['Isotope'] == isotope) &
    (datan['Exclude Me'] != 'y') &
    (datan['Extractant Concentration (M)'] == 0.0025)]
            #liganddata = datan[(datan['Ligand'] == ligand) & (datan['Isotope'] == isotope) & (datan['Initial pH'] == pH) & (datan['Extractant Concentration (M)'] == 0.0025)&(datan['Exclude Me'] != 'y')]
            #(datan['Date'] >= '10/10/2018') & (datan['Date'] <= '10/11/2018') &
    liganddata.sort_values('Ligand Concentration (mM)', inplace = True)
#                xvalues_all = liganddata['Ligand Concentration (mM)'].unique().tolist()
    if isotope in ['Ac227 Daughters','La134']:
        plotdata = liganddata[['Ligand Concentration (mM)','Daughter Extraction %']]
        plotdata = plotdata.rename(index = str, columns={"Daughter Extraction %":"Extraction %"})
    elif isotope in ['Ac227','Ce134','Lu177','Gd153']:
        plotdata = liganddata[['Ligand Concentration (mM)','Extraction %']]
            #    print (liganddata)
    else:
        print ("Error - I don't know what to do with this isotope")
        print ('ran extractdata')
    print(pH, ligand, isotope)
    return (plotdata, linecolor, markershape, linetype, pHname, ligand, isotope)
# Step 6
def average(triplicateorno, plotdata):
    xvalues = []
    yvalues = []
    yerror = []
    if triplicateorno == 'average':
        uniquexentries = plotdata['Ligand Concentration (mM)'].unique().tolist()
        numberofentries = plotdata.groupby('Ligand Concentration (mM)').size().tolist()
        for point in range(0,len(uniquexentries)):
            xvalues.append(uniquexentries[point])
            value = plotdata.loc[(plotdata['Ligand Concentration (mM)'] == uniquexentries[point]),'Extraction %'].mean()
            error = plotdata.loc[(plotdata['Ligand Concentration (mM)'] == uniquexentries[point]),'Extraction %'].std()
            yvalues.append(value)
            yerror.append(error)
    elif triplicateorno == 'individual':

        #Missing the ability to give different dates different colors

        xvalues = plotdata['Ligand Concentration (mM)'].tolist()
        yvalues = plotdata['Extraction %'].tolist()
        yerror = [0] * len(xvalues)
    return (xvalues, yvalues, yerror)
# Step 7
def normalization(normalizedorno, triplicateorno, xvalues, yvalues, yerror):
    if normalizedorno == 'y':
        sortedyvalues = sorted(yvalues, reverse = True) # sorts smallest to largest
        maxyvalue = sortedyvalues[0] # sets max value as first (largest) value in the list
        yvalues[:] = [x/maxyvalue for x in yvalues] # defines new list as the normalized values;
                                        # keeps the original ordering to match the x values ordering
# WRONG ???? (ASK SOMEONE BETTER AT STATISTICS...)
        if triplicateorno == 'y':
            sortedyerror = sorted(yerror, reverse = True)
            maxyerror = sortedyerror[0]
            yerror[:] = [x/maxyerror for x in yerror]
    return (xvalues, yvalues, yerror)
# Step 8
def plots(xvalues, yvalues, yerror, ligand, isotope, linecolor, linetype, markershape):
    # individual plots without lines - except do we want 
    if triplicateorno == 'individual':
        modetype = 'markers'
    elif triplicateorno == 'average':
        modetype = 'markers+lines'
    trace = go.Scatter(
                x = xvalues,
                y = yvalues,
                mode = modetype,
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
    print ('ran plots')
    return (graphdata)

# code
graphed_pH, pH_markers = pH_select()
isotope_markers, isotope_lines, graphed_isotopes = isotope_select()
graphed_ligands, ligand_colors = ligand_select()

# I don't want to have to answer this question a bunch of times...this should come as an input
# after the pH, isotope, ligand inputs but before the code starts actually running
normalizedorno = input ('Do you want the normalized data? (y = normalized; n = raw) (y/n): ')
triplicateorno = input ('Do you want the average or individual data? (average/individual): ')
graphtitle = input ('Please input the desired graph title: ')

datan = pd.read_csv(os.path.join('c:\\Users\\Kathy Shield\\Desktop\\Berkeley\\AbergelGroup\\Research\\Extractions\\Results\\ProcessedDataFiles','allthedata.csv'))
graphdata = []
for isotope in graphed_isotopes:
    #print (graphed_isotopes)
    isotopeindex = graphed_isotopes.index(isotope)
    linetype = isotope_lines[isotopeindex]
    markershape = isotope_markers[isotopeindex]
    for ligand in graphed_ligands:
        #print (graphed_ligands)
        ligandindex = graphed_ligands.index(ligand)
        linecolor = ligand_colors[ligandindex]
        for pH in graphed_pH:
            pHname = str(pH)
            plotdata, linecolor, markershape, linetype, pHname, ligand, isotope = extractdata(graphed_isotopes, graphed_ligands, graphed_pH)
            if not plotdata.empty:
            #if data is extracted, run the rest. if not; move on
                xvalues, yvalues, yerror = average(triplicateorno, plotdata)
                xvalues, yvalues, yerror = normalization(normalizedorno, triplicateorno, xvalues, yvalues, yerror)
                graphdata = plots(xvalues, yvalues, yerror, ligand, isotope, linecolor, linetype, markershape)
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
plot = py.offline.plot(fig, image = 'svg')

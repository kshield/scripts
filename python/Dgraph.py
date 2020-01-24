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
import math
#py.tools.set_credentials_file(username = 'kshield', api_key = 'H9UX6nYroLdbt1W1pjgj')

# functions needed
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
def isotope_select():
    potential_isotopes = ['Ac227','Ce134','Gd153','Lu177','Ac227 Daughters','La134']
    # Isotope line format list
    Ac227line = 'dot'
    Gd153line = 'solid'
    Lu177line = 'dash'
    Ce134line = 'longdash'
    allisotopes = input ('Do you want to graph all possible isotopes? (y/n): ')
    if allisotopes == 'y':
        includedaughters = input ('Graph daughters too? (y/n): ')
        if includedaughters == 'y':
            graphed_isotopes = potential_isotopes
            isotope_lines = [Ac227line, Ce134line, Gd153line, Lu177line, Gd153line, Ac227line]
            isotope_markers = ['circle','square','triangle-up','diamond','x','star']
            isotope_data = ['Ac227','Ce134','Gd153','Lu177','Ac227','Ce134']
        elif includedaughters =='n':
            graphed_isotopes = potential_isotopes[0:3]
            isotope_lines = [Ac227line, Ce134line, Gd153line, Lu177line]
            isotope_markers = ['circle','square','triangle-up','diamond']
            isotope_data = ['Ac227','Ce134','Gd153','Lu177']
    else:
        graphed_isotopes = []
        isotope_data = []
        isotope_lines = []
        isotope_markers = []
        for isotope in potential_isotopes:
            isotope_yes = input ('Do you want to graph '+isotope+'? (y/n): ')
            if isotope_yes == 'y':
                graphed_isotopes.append(isotope)
                if isotope == 'Ac227':
                    isotope_lines.append(Ac227line)
                    isotope_markers.append('circle')
                    isotope_data.append('Ac227')
                elif isotope == 'Gd153':
                    isotope_lines.append(Gd153line)
                    isotope_markers.append('square')
                    isotope_data.append('Gd153')
                elif isotope == 'Lu177':
                    isotope_lines.append(Lu177line)
                    isotope_markers.append('triangle-up')
                    isotope_data.append('Lu177')
                elif isotope == 'Ce134':
                    isotope_lines.append(Ce134line)
                    isotope_markers.append('diamond')
                    isotope_data.append('Ce134')
                elif isotope == 'Ac227 Daughters':
                    isotope_lines.append(Gd153line)
                    isotope_markers.append('x')
                    isotope_data.append('Ac227')
                elif isotope == 'La134':
                    isotope_lines.append(Lu177line)
                    isotope_markers.append('star')
                    isotope_data.append('Ce134')
    print ('ran isotope_select')
    return (isotope_markers, isotope_lines, graphed_isotopes, isotope_data)
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
# plot: D/D0
# need to extract D0 values
# need to define D values (probably easiest to just put these values in by hand once instead of writing code for it)
# normalization? I don't think so...
# start without any by date data analysis


def extractdata(graphed_isotopes, graphed_ligands, graphed_pH):
    liganddata = datan[(datan['Initial pH'] == pH) &
    (datan['Ligand'] == ligand) &
    (datan['Isotope'] == parentname) &
    (datan['Exclude Me'] != 'y') &
    (datan['Extractant Concentration (M)'] == 0.0025)]
            #liganddata = datan[(datan['Ligand'] == ligand) & (datan['Isotope'] == isotope) & (datan['Initial pH'] == pH) & (datan['Extractant Concentration (M)'] == 0.0025)&(datan['Exclude Me'] != 'y')]
            #(datan['Date'] >= '10/10/2018') & (datan['Date'] <= '10/11/2018') &
    liganddata.sort_values('Ligand Concentration (mM)', inplace = True)
    #                xvalues_all = liganddata['Ligand Concentration (mM)'].unique().tolist()
    if isotope in ['Ac227 Daughters','La134']:
        plotdata = liganddata[['Date','Ligand Concentration (mM)','Daughter Distribution Value']]
        plotdata = plotdata.rename(index = str, columns={"Daughter Distribution Value":"Distribution Value"})
        #parentdata = liganddata[['Date','Ligand Concentration (mM)','Extraction %']]
    elif isotope in ['Ac227','Ce134','Lu177','Gd153']:
        plotdata = liganddata[['Date','Ligand Concentration (mM)','Distribution Value']]
        print (plotdata)
        #parentdata = []
    else:
        print ("Error - I don't know what to do with this isotope")
    print ('ran extractdata')
    print(pH, ligand, isotope)
    return (plotdata, #parentdata,
    linecolor, markershape, linetype, pHname, ligand, isotope)
def notbydate(plotdata, isotope):
    # define D0 values (taken from allthedata.csv zero ligand by hand)
    d0_Ac = 4.334488
    d0_Acerror = 0.988426
    d0_Gd = 5.283318
    d0_Gderror = 2.748455
    fullydeprotonated_DTPA = 6.14541E-8
    xvalues = []
    yvalues = []
    yerror = []
    uniquexentries = plotdata['Ligand Concentration (mM)'].unique().tolist()
    numberofentries = plotdata.groupby('Ligand Concentration (mM)').size().tolist()
    for point in range(0,len(uniquexentries)):
        xvalue = uniquexentries[point]#*fullydeprotonated_DTPA
        logxvalue = math.log10(xvalue)
        # if the D value = 0, the point needs to be discarded
        #if logxvalue > 0.000000000:
        xvalues.append(xvalue)
        #plotdata = plotdata.convert_objects(convert_numeric=True)
        value = plotdata.loc[(plotdata['Ligand Concentration (mM)'] == uniquexentries[point]),'Distribution Value']
        value = pd.to_numeric(value, errors='coerce').mean()
        error = plotdata.loc[(plotdata['Ligand Concentration (mM)'] == uniquexentries[point]),'Distribution Value']
        error = pd.to_numeric(error, errors='coerce').std()
        #value = d0_Gd/value
        print (xvalue, value, error)
        #logvalue = math.log10(value)
        #logerror = math.log10(error)
        #print (xvalue, logvalue, error, logerror)
        yvalues.append(value)
        yerror.append(error)
    return (xvalues, yvalues, yerror)
def distributionplots(xvalues, yvalues, yerror, ligand, isotope, linecolor, linetype, markershape, pHname):
    # individual plots without lines - except do we want
    linename = ligand+'-'+isotope#+', '+date#+', '+pHname
    modetype = 'markers+lines'
    markerdefine = dict(color = linecolor+'1)', symbol = markershape, size = 10)
    linedefine = dict(color = linecolor+'1)', dash = linetype)
    trace = go.Scatter(
                x = xvalues,
                y = yvalues,
                mode = modetype,
                name = linename,
                line = linedefine,
                marker = markerdefine,
                #error_y = dict(
                #    type = 'data',
                #    array = yerror,
                #    visible = 'True',
                #    color = linecolor+'.5)'
                #    )
                )
    graphdata.append(trace)
    print ('ran plots')
    return (graphdata)

graphed_pH, pH_markers = pH_select()
isotope_markers, isotope_lines, graphed_isotopes, isotope_data = isotope_select()
graphed_ligands, ligand_colors = ligand_select()

# I don't want to have to answer this question a bunch of times...this should come as an input
# after the pH, isotope, ligand inputs but before the code starts actually running

graphtitle = input ('Please input the desired graph title: ')

datan = pd.read_csv(os.path.join('c:\\Users\\Kathy Shield\\Desktop\\Berkeley\\AbergelGroup\\Research\\1-Extractions\\Extractions\\Results\\ProcessedDataFiles','allthedata.csv'))
graphdata = []
for isotope in graphed_isotopes:
    #print (graphed_isotopes)
    isotopeindex = graphed_isotopes.index(isotope)
    linetype = isotope_lines[isotopeindex]
    markershape = isotope_markers[isotopeindex]
    parentname = isotope_data[isotopeindex]
    for ligand in graphed_ligands:
        #print (graphed_ligands)
        ligandindex = graphed_ligands.index(ligand)
        linecolor = ligand_colors[ligandindex]
        for pH in graphed_pH:
            pHname = str(pH)
            plotdata, linecolor, markershape, linetype, pHname, ligand, isotope = extractdata(graphed_isotopes, graphed_ligands, graphed_pH)
            xvalues, yvalues, yerror = notbydate(plotdata, isotope)
            graphdata = distributionplots(xvalues, yvalues, yerror, ligand, isotope, linecolor, linetype, markershape, pHname)

layout = go.Layout(
                      title = graphtitle,
                          titlefont = dict(
                              family = 'Georgia',
                              size = 30
                          ),
                      xaxis = dict(
                          type = 'linear',
                          autorange = True,
                          domain = [0,1],
                          range = [-5.2,1],
                          title = '[Ligand]',
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
                          autorange = True,
                          domain = [0,1],
                          range = [0,1.1],
                          title = 'D0/D',
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
                          y = 1.04
                      )
                  )
fig = go.Figure(data=graphdata, layout=layout)
plot = py.offline.plot(fig, image = 'png')

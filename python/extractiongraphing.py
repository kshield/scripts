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
    CDTAcolor = 'rgba(70,240,240,'
    DTPAcolor = 'rgba(128,0,0,'
    EDTAcolor = 'rgba(0,130,200,'
    PDTAcolor = 'rgba(240,50,230,'
    TTHAcolor = 'rgba(250,190,190,'
    DTPMPcolor = 'rgba(241,73,35,'
    EDTPAcolor = 'rgba(0,0,128,'
    CAMcolor = 'rgba(230,25,75,'
    CHHCcolor = 'rgba(245,130,48,'
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
                    ligand_colors.append('rgba(70,240,240,')
                elif ligand == 'DTPA':
                    ligand_colors.append('rgba(128,0,0,')
                elif ligand == 'EDTA':
                    ligand_colors.append('rgba(0,130,200,')
                elif ligand == 'PDTA':
                    ligand_colors.append('rgba(240,50,230,')
                elif ligand == 'TTHA':
                    ligand_colors.append('rgba(250,190,190,')
                elif ligand == 'DTPMP':
                    ligand_colors.append('rgba(241,73,35,')
                elif ligand == 'EDTPA':
                    ligand_colors.append('rgba(0,0,128,')
                elif ligand == 'CAM':
                    ligand_colors.append('rgba(230,25,75,')
                elif ligand == 'CHHC':
                    ligand_colors.append('rgba(245,130,48,')
                elif ligand == 'HCCH':
                    ligand_colors.append('rgba(145,30,180,')
                elif ligand == 'HOPO':
                    ligand_colors.append('rgba(60,180,75,')
                elif ligand == 'bacillibactin':
                    ligand_colors.append('rgba(145,30,180,')
    print ('ran ligand_select')
    return (graphed_ligands, ligand_colors)
def extractdata(graphed_isotopes, graphed_ligands, graphed_pH):
    liganddata = datan[(datan['Initial pH'] == pH) &
    (datan['Ligand'] == ligand) &
    (datan['Isotope'] == parentname) &
    (datan['Exclude Me'] != 'y') &
    (datan['Extractant Concentration (M)'] == 0.0025)] #&
            #liganddata = datan[(datan['Ligand'] == ligand) & (datan['Isotope'] == isotope) & (datan['Initial pH'] == pH) & (datan['Extractant Concentration (M)'] == 0.0025)&(datan['Exclude Me'] != 'y')]
    #(datan['Date'] >= '5/3/2019') & (datan['Date'] <= '5/5/2019')]
    liganddata.sort_values('Ligand Concentration (mM)', inplace = True)
#                xvalues_all = liganddata['Ligand Concentration (mM)'].unique().tolist()
    if isotope in ['Ac227 Daughters','La134']:
        plotdata = liganddata[['Date','Ligand Concentration (mM)','Daughter Extraction %']]
        plotdata = plotdata.rename(index = str, columns={"Daughter Extraction %":"Extraction %"})
        parentdata = liganddata[['Date','Ligand Concentration (mM)','Extraction %']]
    elif isotope in ['Ac227','Ce134','Lu177','Gd153']:
        plotdata = liganddata[['Date','Ligand Concentration (mM)','Extraction %']]
        parentdata = []
        print (plotdata)
    else:
        print ("Error - I don't know what to do with this isotope")
        print ('ran extractdata')
    print(pH, ligand, isotope)
    return (plotdata, parentdata, linecolor, markershape, linetype, pHname, ligand, isotope)
def bydate(triplicateorno, plotdata, date):
    xvalues = []
    yvalues = []
    yerror = []
    parentyvalues = []
    parentyerror = []
    #parentdata['Date'] = datetime.datetime.strptime(parentdata['Date'],'%m/%d/%Y').strftime('%Y%m%d')
    #plotdata['Date'] = datetime.datetime.strptime(plotdata['Date'],'%m/%d/%Y').strftime('%Y%m%d')
    datespecificdata = plotdata.loc[plotdata['Date'] == date]
    #datespecificparentdata = parentdata.loc[parentdata['Date'] == date]
    if triplicateorno == 'average' and datecolors == 'y':
        uniquexentries = datespecificdata['Ligand Concentration (mM)'].unique().tolist()
        numberofentries = datespecificdata.groupby('Ligand Concentration (mM)').size().tolist()
        for point in range(0,len(uniquexentries)):
            xvalues.append(uniquexentries[point])
            value = datespecificdata.loc[(datespecificdata['Ligand Concentration (mM)'] == uniquexentries[point]),'Extraction %'].mean()
            error = datespecificdata.loc[(datespecificdata['Ligand Concentration (mM)'] == uniquexentries[point]),'Extraction %'].std()
            yvalues.append(value)
            yerror.append(error)
            if isotope in ['Ac227 Daughters','La134']:
                parentvalue = datespecificparentdata.loc[(datespecificparentdata['Ligand Concentration (mM)'] == uniquexentries[point]),'Extraction %'].mean()
                parenterror = datespecificparentdata.loc[(datespecificparentdata['Ligand Concentration (mM)'] == uniquexentries[point]),'Extraction %'].std()
                parentyvalues.append(parentvalue)
                parentyerror.append(parenterror)
    elif triplicateorno == 'individual' and datecolors == 'y':
        xvalues = datespecificdata['Ligand Concentration (mM)'].tolist()
        yvalues = datespecificdata['Extraction %'].tolist()
        yerror = [0] * len(xvalues)
        if isotope in ['Ac227 Daughters','La134']:
            parentyvalues = datespecificparentdata['Extraction %'].tolist()
            parentyerror = [0] * len(xvalues)
    return (xvalues, yvalues, yerror, parentyvalues, parentyerror)
def notbydate(triplicateorno, plotdata, parentdata):
    xvalues = []
    yvalues = []
    yerror = []
    parentyvalues = []
    parentyerror = []
    if triplicateorno == 'average':
        uniquexentries = plotdata['Ligand Concentration (mM)'].unique().tolist()
        numberofentries = plotdata.groupby('Ligand Concentration (mM)').size().tolist()
        for point in range(0,len(uniquexentries)):
            xvalues.append(uniquexentries[point])
            value = plotdata.loc[(plotdata['Ligand Concentration (mM)'] == uniquexentries[point]),'Extraction %'].mean()
            error = plotdata.loc[(plotdata['Ligand Concentration (mM)'] == uniquexentries[point]),'Extraction %'].std()
            yvalues.append(value)
            yerror.append(error)
            if isotope in ['Ac227 Daughters','La134']:
                parentvalue = parentdata.loc[(parentdata['Ligand Concentration (mM)'] == uniquexentries[point]),'Extraction %'].mean()
                parenterror = parentdata.loc[(parentdata['Ligand Concentration (mM)'] == uniquexentries[point]),'Extraction %'].std()
                parentyvalues.append(parentvalue)
                parentyerror.append(parenterror)
    elif triplicateorno == 'individual':
        xvalues = plotdata['Ligand Concentration (mM)'].tolist()
        yvalues = plotdata['Extraction %'].tolist()
        yerror = [0] * len(xvalues)
        if isotope in ['Ac227 Daughters','La134']:
            parentyvalues = datespecificparentdata['Extraction %'].tolist()
            parentyerror = [0] * len(xvalues)
    return (xvalues, yvalues, yerror, parentyvalues, parentyerror)
def normalization(normalizedorno, triplicateorno, xvalues, yvalues, yerror, parentyvalues, parentyerror):
    # PROBLEM: normalization code is normalizing the daughters independently of the parent, resulting in graphs
    # that indication 100% daughter extraction.
    # SOLUTION: normalization code needs to take into account the parent when it exists, and normalize to the
    # max. value of the parent, not the max. value of the daughter.
    if normalizedorno == 'y':
        if isotope in ['Ac227 Daughters','La134']: # if isotope has a parent
            sortedyvalues = sorted(parentyvalues, reverse = True) # sorts parent values largest to smallest
        else: #if isotope has no parent
            sortedyvalues = sorted(yvalues, reverse = True) # sorts largest to smallest
        maxyvalue = sortedyvalues[0] #defines first entry as the value to normalize by
        if maxyvalue == 0:
            maxyvalue = 1 # prevents division by 0
        yvalues[:] = [x/maxyvalue for x in yvalues] # defines new list as the normalized values;
                                        # keeps the original ordering to match the x values ordering
# WRONG ???? (ASK SOMEONE BETTER AT STATISTICS...)
        if triplicateorno == 'y':
            if isotope in ['Ac227 Daughters','La134']: # if isotope has a parent
                sortedyerror = sorted(parentyerror, reverse = True) # sorts parent values largest to smallest
            else: #if isotope has no parent
                sortedyerror = sorted(yerror, reverse = True) # sorts largest to smallest
            maxyerror = sortedyerror[0]
            yerror[:] = [x/maxyerror for x in yerror]
    return (xvalues, yvalues, yerror)
def extractionplots(xvalues, yvalues, yerror, ligand, isotope, linecolor, linetype, markershape, pHname, date):
    # individual plots without lines - except do we want
    linename = ligand+'-'+isotope#+', '+date#+', '+pHname
    if triplicateorno == 'individual':
        modetype = 'markers'
    elif triplicateorno == 'average':
        modetype = 'markers+lines'
    if datecolors == 'y':
        markerdefine = dict(symbol = markershape, size = 10)
        linedefine = dict(dash = linetype)
    elif datecolors == 'n':
        markerdefine = dict(color = linecolor+'1)', symbol = markershape, size = 10)
        linedefine = dict(color = linecolor+'1)', dash = linetype)
    trace = go.Scatter(
                x = xvalues,
                y = yvalues,
                mode = modetype,
                name = linename,
                line = linedefine,
                marker = markerdefine,
                error_y = dict(
                    type = 'data',
                    array = yerror,
                    visible = True,
                    color = linecolor+'.5)'
                    )
                )
    graphdata.append(trace)
    print ('ran plots')
    return (graphdata)

graphed_pH, pH_markers = pH_select()
isotope_markers, isotope_lines, graphed_isotopes, isotope_data = isotope_select()
graphed_ligands, ligand_colors = ligand_select()

# I don't want to have to answer this question a bunch of times...this should come as an input
# after the pH, isotope, ligand inputs but before the code starts actually running
normalizedorno = input ('Do you want the normalized data? (y = normalized; n = raw) (y/n): ')
triplicateorno = input ('Do you want the average or individual data? (average/individual): ')
datecolors = input ('Do you want different dates to have different colors? (y/n): ')
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
            plotdata, parentdata, linecolor, markershape, linetype, pHname, ligand, isotope = extractdata(graphed_isotopes, graphed_ligands, graphed_pH)
            #datecolors = input ('Should individual dates of '+ligand+' + '+isotope+' + '+pHname+' get different colors? (y/n): ')
            if datecolors == 'y':
                dates_all = plotdata['Date'].unique().tolist()
                for date in dates_all:
                    if not plotdata.empty:
                #if data is extracted, run the rest. if not; move on
                        xvalues, yvalues, yerror, parentyvalues, parentyerror = bydate(triplicateorno, plotdata, date)
                        xvalues, yvalues, yerror = normalization(normalizedorno, triplicateorno, xvalues, yvalues, yerror, parentyvalues, parentyerror)
                        graphdata = extractionplots(xvalues, yvalues, yerror, ligand, isotope, linecolor, linetype, markershape, pHname, date)
            elif datecolors == 'n':
                date = ''
                if not plotdata.empty:
            #if data is extracted, run the rest. if not; move on
                    xvalues, yvalues, yerror, parentyvalues, parentyerror = notbydate(triplicateorno, plotdata, parentdata)
                    xvalues, yvalues, yerror = normalization(normalizedorno, triplicateorno, xvalues, yvalues, yerror, parentyvalues, parentyerror)
                    graphdata = extractionplots(xvalues, yvalues, yerror, ligand, isotope, linecolor, linetype, markershape, pHname, date)

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
                          range = [-5.2,1.2],
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
                          y = 1.04
                      )
                  )
fig = go.Figure(data=graphdata, layout=layout)
#plot = py.plot(fig, auto_open = True)
plot = py.offline.plot(fig, image = 'png')

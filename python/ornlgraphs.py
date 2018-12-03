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

# Which ligands are we graphing today?
potential_ligands = ['CDTA', 'DTPA', 'EDTA', 'PDTA', 'TTHA',
'DTPMP', 'EDTPA', 'CAM', 'CHHC', 'HCCH', 'HOPO'
]
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
    ligand_colors = [CDTAcolor, DTPAcolor, EDTAcolor, PDTAcolor, TTHAcolor, DTPMPcolor, EDTPAcolor, CAMcolor, CHHCcolor, HCCHcolor, HOPOcolor]
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

# Which isotopes are we graphing today?
potential_isotopes = ['Ac227','Gd153'#,'Lu177'
]
# Isotope line format list
Ac227line = 'dot'
Gd153line = ''
Lu177line = 'dash'
allisotopes = input ('Do you want to graph all possible isotopes? (y/n): ')
if allisotopes == 'y':
    graphed_isotopes = potential_isotopes
    isotope_lines = [Ac227line, Gd153line, Lu177line]
else:
    graphed_isotopes = []
    isotope_lines = []
    for isotope in potential_isotopes:
        isotope_yes = input ('Do you want to graph '+isotope+'? (y/n): ')
        if isotope_yes == 'y':
            graphed_isotopes.append(isotope)
            if isotope == 'Ac227':
                isotope_lines.append('dot')
            elif isotope == 'Gd153':
                isotope_lines.append('')
            elif isotope == 'Lu177':
                isotope_lines.append('dash')

# Warning about data
print ('This script only incorporates pH 6 data; if you want other pH values, go elsewhere.')


datan['Date'] = datan.Date
date = datetime.datetime.strptime(datan.loc[0,'Date'],'%m/%d/%Y').strftime('%Y%m%d')

# Actually plotting the thing
graphdata = []
for isotope in graphed_isotopes:
    isotopeindex = graphed_isotopes.index(isotope)
    linetype = isotope_lines[isotopeindex]
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
        #normalize the data


        # figuring out how many data points are in triplicate
        numberofentries = liganddata.groupby('Ligand Concentration (mM)').size().tolist()
        triplicatedataexists = []
        xvalues = xvalues_all
        if isotope == 'Gd153':
            yvalues = liganddata['Extraction %']
            trace = go.Scatter(
                x = xvalues,
                y = yvalues,
                mode = 'markers+lines',
                name = ligand+'-'+isotope,
                line = dict(color = linecolor+'1)', dash = linetype)
                )
            graphdata.append(trace)
        elif isotope == 'Ac227':
            yvalues = liganddata['Extraction %']
            print(liganddata, yvalues)
            maxvalue = liganddata.iloc[0]['Extraction %']
            print (maxvalue)
            normalizedyvalues = []
            for entry in yvalues:
               normalizedvalue = entry/maxvalue
               normalizedyvalues.append(normalizedvalue)
            print (normalizedyvalues)
            trace = go.Scatter(
                x = xvalues,
                y = normalizedyvalues,
                mode = 'markers+lines',
                name = ligand+'-'+isotope,
                line = dict(color = linecolor+'1)', dash = linetype)
                )
            graphdata.append(trace)

        layout = go.Layout(
            xaxis = dict(
                type = 'log',
                autorange = True,
                domain = [0,1],
                range = [-4,-2],
                title = 'Ligand Concentration (mM)',
                showgrid = True,
                showline = True,
                exponentformat = 'e',
                tick0 = -4,
                dtick = 1,
            ),
            yaxis = dict(
                type = 'linear',
                autorange = False,
                domain = [0,1],
                range = [0,1.1],
                title = 'Relative Extraction',
                showgrid = True,
                showline = True
            ),
            legend = dict(
                #font = dict(
                #    size = 18
                #),
                orientation = 'h',
                xanchor = 'center',
                x = 0.5,
                y = -.2),
            title = 'Ac and Gd Extraction: Phosphonated Ligands'
        )
    fig = go.Figure(data=graphdata, layout=layout)
plot = py.offline.plot(fig, image = 'svg')

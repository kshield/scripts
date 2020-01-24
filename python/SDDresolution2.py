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

data = pd.read_csv(os.path.join('c:\\Users\\Kathy Shield\\Desktop\\Berkeley\\LANL SDD Paper\\energyresolution_graphdata.csv'))

xvalues = data['Energy (keV)']
yvalues = data['Resolution FWHM (keV)'] *1000
xerror = data['energy error']
yerror = data['resolution error'] *1000
labels = data['Isotope'].tolist()


data = []

graphdata = go.Scatter(
        x = xvalues,
        y = yvalues,
        mode = 'markers',
        marker = dict(color = 'black'),
        error_y = dict(
            type = 'data',
            array = yerror,
            visible = 'True',
            color = '#000000'
            ),
        error_x = dict(
            type = 'data',
            array = xerror,
            visible = 'True',
            color = '#000000'
            ),
        text = labels,
        showlegend = False
        )

xi = np.arange(0,22,.1)

line = 2.355*np.sqrt(1789.29 + 0.115*3630*xi)
#line = 1+np.sqrt(xi)

lineplot = go.Scatter(
    x = xi,
    y = line,
    mode = 'lines',
    name = '99.617 + 2.35SQRT(417.45*x)')

data.append(lineplot)
data.append(graphdata)


# SHOW LINE OF BEST FIT EQUATION
# REMOVE LEGEND

layout = go.Layout(
    title = 'Silicon Drift Detector Energy Resolution',
        titlefont = dict(
            family = 'Times',
            size = 30
        ),
    xaxis = dict(
       type = 'linear',
       autorange = True,
       #domain = [0,1],
       range = [0,15],
       title = 'Energy (keV)',
       titlefont = dict(
            family = 'Times',
            size = 22
        ),
       tickfont = dict(
            family = 'Times',
            size = 22
       ),
       showgrid = True,
       showline = True,
       # exponentformat = 'e',
       # tick0 = -4,
       # dtick = 1),
       ),
   yaxis = dict(
       type = 'linear',
       autorange = False,
       # domain = [0,1],
       range = [0,500],
       title = 'Resolution FWHM (eV)',
       titlefont = dict(
            family = 'Times',
            size = 22
        ),
       tickfont = dict(
            family = 'Times',
            size = 22
       ),
       showgrid = True,
       showline = True,
       ),
    legend = dict(
        font = dict(
            family = 'Times',
            size = 22
        ),
        x = .4,
        y = .87
    )
)

fig = go.Figure(data = data, layout=layout)
plot = py.offline.plot(fig, image = 'svg')

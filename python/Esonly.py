''' Present an interactive function explorer with slider widgets.
Scrub the sliders to change the properties of the ``sin`` curve, or
type into the title text box to update the title of the plot.
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve sliders.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/Esonly
in your browser.
'''
import numpy as np
import pandas as pd
import scipy as scipy
from scipy import optimize
import scipy.stats as stats

import datetime
import csv
import math

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.ticker as ticker
from matplotlib.ticker import AutoMinorLocator
from matplotlib import gridspec
import matplotlib.patches as mpatches

from bokeh.io import curdoc, show
from bokeh.layouts import column, row, widgetbox
from bokeh.models import ColumnDataSource, Slider, TextInput, Legend
from bokeh.plotting import figure

Bk_energies = [15.7, 889.956, 929.468, 989.125, 1028.654, 1031.852]
Bk_intensities = [21.4, 1.53, 1.23, 45.0, 4.91, 35.6]
Es_energies = [61.89, 107.2, 112.1]
Es_intensities = [2.17, 0.102, 0.167]
Cf_energies = [15.0, 104.59, 109.271, 252.82, 333.37, 388.17]
Cf_intensities = [14.5, 2.01, 3.15, 2.59, 15.0, 66.0]
energies = [Es_energies, Bk_energies, Cf_energies]
intensities = np.array([np.array(Es_intensities), np.array(Bk_intensities), np.array(Cf_intensities)])
choosecolor = ["blue", "coral", "green"]
elementlist = ['Es-254', 'Bk-250', 'Cf-249']

# all data in [Es-254, Bk-250, Cf-249, Cf-250] order
tonehalf = [275.7*24*3600, 3.212*3600, 351*365*24*3600, 13.08*365*24*3600] # half lives in seconds
lambdas = [0.69314718056/i for i in tonehalf] # seconds^-1
lambdashr = [3600*i for i in lambdas] # hours ^-1
lambdasd = [3600*24*i for i in lambdas] # days ^-1
N_A = 6.022*(10**23)
specact = [(1/254)*N_A*i for i in lambdas] # specific activities, Bq/g
mng = [233.8,0,119,0] #initial mass, nanograms
m0 = [i/1000/1000/1000 for i in mng] #initial mass, grams
ABq = [i*j for i, j in zip(specact, m0)] #initial activity (Bq)
A0 = [i/(3.7*(10**10)) for i in ABq] # initial activity (Ci)
A0mCi_init = [i*1000 for i in A0] # activity (mCi)
days = 150
time = 24

# Set up data
df = pd.DataFrame()
df["energies"] = Es_energies
df["intensities"] = Es_intensities
df["isotope"] = "Es-254"
df["color"] = "blue"
df["tops"] = 0

df1 = pd.DataFrame()
df1["energies"] = Bk_energies
df1["intensities"] = Bk_intensities
df1["isotope"] = "Bk-250"
df1["color"] = "coral"
df1["tops"] = 0

df2 = pd.DataFrame()
df2["energies"] = Cf_energies
df2["intensities"] = Cf_intensities
df2["isotope"] = "Cf-249"
df2["color"] = "green"
df2["tops"] = 0

def Esactivityd(A0mCi, x):
    l = lambdasd
    At = A0mCi[0]*np.exp(-l[0]*x)
    return At

def Bkactivityd(A0mCi, x):
    l = lambdasd
    At = A0mCi[0] * (l[1]/(l[1]-l[0])) * (np.exp(-l[0]*x) - np.exp(-l[1]*x)) + (A0[1] * np.exp(-l[1]*x))
    return At

def Cf249activityd(A0mCi, t):
    l = lambdasd
    At = A0mCi[2]*np.exp(-l[3]*t)
    return At

def Esactivityhr(A0mCi, x):
    l=lambdashr
    At = A0mCi[0]*np.exp(-l[0]*x)
    return At

def Bkactivityhr(A0mCi, x):
    l = lambdashr
    At = A0mCi[0] * (l[1]/(l[1]-l[0])) * (np.exp(-l[0]*x) - np.exp(-l[1]*x)) + (A0mCi[1] * np.exp(-l[1]*x))
    return At

def Cf249activityhr(A0mCi, t):
    l = lambdashr
    At = A0mCi[2]*np.exp(-l[3]*t)
    return At

def totalactivity(days):
    A0mCi = A0mCi_init
    df["activities"] = Esactivityd(A0mCi, days)
    df1["activities"] = Bkactivityd(A0mCi, days)
    df2["activities"] = Cf249activityd(A0mCi, days)
    return df,df1,df2

def purified(time):
    if time < 24:
        A0mCi = [df.loc[0,'activities'],0,0]
    else:
        A0mCi = [df.loc[0,'activities'],df1.loc[0,'activities'],df2.loc[0,'activities']]#,df1.loc[0,'activities'],df2.loc[0,'activities']]
    df["activities2"] = Esactivityhr(A0mCi, time)
    df1["activities2"] = Bkactivityhr(A0mCi, time)
    df2["activities2"] = Cf249activityhr(A0mCi,time)
    df["tops"] = df["activities2"]*df["intensities"]
    df1["tops"] = df1["activities2"]*df1["intensities"]
    df2["tops"] = df2["activities2"]*df2["intensities"]
    return df, df1, df2

df, df1, df2 = totalactivity(days)
df, df1, df2 = purified(time)
data = pd.concat([df,df1,df2])
data["comptony"] = data.iloc[5,4]
# x = df["energies"]
# x1= df1["energies"]
# x2= df2["energies"]
# y = df["tops"]
# y1=df1["tops"]
# y2 = df2["tops"]
# source = ColumnDataSource(data=dict(x=x,y=y))
# source1 = ColumnDataSource(data=dict(x=x1,y=y1))
# source2 = ColumnDataSource(data=dict(x=x2,y=y2))
source = ColumnDataSource(data=data)
plot = figure(title = "Predicted Gamma Spectrum", y_axis_type = "log")
plot.xaxis.axis_label = "Energy (keV)"
plot.yaxis.axis_label = "Intensity"
legend = Legend()
plot.add_layout(legend,'below')
# plot.vbar(x='x', top='y', width=1, source=source, color="blue", legend="Es-254")
# plot.vbar(x='x', top='y', width=1, source=source1, color="coral", legend="Bk-250")
# plot.vbar(x='x', top='y', width=1, source=source2, color="green", legend="Cf-249")

plot.vbar(x="energies",top="tops",bottom=0.0000001, color="color", width=1, source=source, legend = "isotope")

# compton line
plot.line(x="energies",y="comptony", line_width = 1, line_color = "coral", alpha=0.5, source=source, legend="approx. Bk compton shelf")

day_select = Slider(start=0, end=500, value=191, step=1, title="Days since Es purified at ORNL (May 1 = 191)")
time_select = Slider(start=0, end=25, value=2, step=0.2, title="Hours since column separation")

def update_data(attrname, old, new):
    # Get the current slider values
    days = day_select.value
    time = time_select.value
    # Generate the new curve
    df, df1, df2 = totalactivity(days)
    df, df1, df2 = purified(time)
    data= pd.concat([df,df1,df2])
    data["comptony"] = data.iloc[5,4]
    source.data = ColumnDataSource(data=data).data



for w in [day_select, time_select]:
    w.on_change('value', update_data)

inputs=widgetbox(day_select, time_select)
curdoc().add_root(column(plot,inputs))

# Esdata = {'x':Es_energies, 'y':df.tops.tolist()}
# Bkdata = {'x':Bk_energies, 'y':df1.tops.tolist()}
# Cfdata = {'x':Cf_energies, 'y':df2.tops.tolist()}
#
# #set up plot
# plot = figure(title="Simulated Gamma Spectrum")
# plot.vbar(source=Esdata,x='x',width=1,top='y', color = df.loc[0,"color"], legend = df.loc[0,"isotope"])
# plot.vbar(source=Bkdata,x='x',width=1,top='y', color = df1.loc[0,"color"], legend = df1.loc[0,"isotope"])
# plot.vbar(source=Cfdata,x='x',width=1,top='y', color = df2.loc[0,"color"], legend = df2.loc[0,"isotope"])
#
# def replot():
#     plot.vbar(source=Esdata,x='x',width=1,top='y', color = df.loc[0,"color"], legend = df.loc[0,"isotope"])
#     plot.vbar(source=Bkdata,x='x',width=1,top='y', color = df1.loc[0,"color"], legend = df1.loc[0,"isotope"])
#     plot.vbar(source=Cfdata,x='x',width=1,top='y', color = df2.loc[0,"color"], legend = df2.loc[0,"isotope"])
#
#
# # Set up widgets
#
#
#
# # Set up callbacks
#
#

#
# # Set up layouts and add to document
# inputs = column(day_select, time_select)
# curdoc().add_root(column(inputs, plot, width=800))
# curdoc().title = "Interim2"

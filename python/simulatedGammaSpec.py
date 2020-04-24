import os
import pandas as pd
import numpy as np
import datetime
import csv
import ggplot
from ggplot import *
import plotnine as p9
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import scipy as scipy
from scipy import optimize
from matplotlib.ticker import AutoMinorLocator
from matplotlib import gridspec
import matplotlib.ticker as ticker
import scipy.stats as stats
import math
import seaborn as sns
import matplotlib.patches as mpatches
import bokeh
from bokeh.plotting import figure, output_file, show

# ------------ DETERMINING RELATIVE INTENSITIES OF GAMMA LINES --------------

# ----------------------------------------
# BK-250
# ----------------------------------------
Bk_energies = [15.7, 889.956, 929.468, 989.125, 1028.654, 1031.852]
Bk_intensities = [21.4, 1.53, 1.23, 45.0, 4.91, 35.6]
Bk_gammas = []
for gamma in range(0,len(Bk_energies)):
    entry = np.random.normal(Bk_energies[gamma],1/Bk_intensities[gamma],10000)
    Bk_gammas.append(entry)

for gamma in Bk_gammas:
    sns.distplot(gamma,color='coral')

coral_patch = mpatches.Patch(color="coral",label = "Bk-250")
# ----------------------------------------
# ES-254
# ----------------------------------------
#Es_energies = [16.351, 21.479, 25.747, 104.351, 115.279, 121.058, 136.088, 584.316, 648.795, 688.667, 693.774]
#Es_intensities = [10.6, 13.2, 3.1, .179, .502, .77, .292, 2.89, 28.9, 12.4, 24.7]
# ^ these are for the wrong halflife
#Es_energies = [42.6, 65.0, 316.7]
#Ex_intensities = [0.15, 2.0, 0.15]
# ^ these are from nndc while the numbers below are from Ahmad, 2008 (10.1103/PhysRevC.77.054302)
Es_energies = [61.89, 107.2, 112.1]
Es_intensities = [2.17, 0.102, 0.167]
Es_gammas=[]
for gamma in range(0,len(Es_energies)):
    entry = np.random.normal(Es_energies[gamma],1/Es_intensities[gamma],1000)
    Es_gammas.append(entry)

for gamma in Es_gammas:
    sns.distplot(gamma,color='blue')

blue_patch = mpatches.Patch(color="blue",label = "Es-254")
# ----------------------------------------
# CF-249
# ----------------------------------------
Cf_energies = [15.0, 104.59, 109.271, 252.82, 333.37, 388.17]
Cf_intensities = [14.5, 2.01, 3.15, 2.59, 15.0, 66.0]
Cf_gammas = []
for gamma in range(0,len(Cf_energies)):
    entry = np.random.normal(Cf_energies[gamma],1/Cf_intensities[gamma],10000)
    Cf_gammas.append(entry)

for gamma in Cf_gammas:
    sns.distplot(gamma,color='green')

green_patch = mpatches.Patch(color="green",label = "Cf-249")

fig = plt.figure(figsize=(10,10))
gs = gridspec.GridSpec(1,1)
ax1 = fig.add_subplot(gs[0])
plt.legend(handles=[blue_patch,coral_patch,green_patch])
plt.show()

energies = [Es_energies, Bk_energies, Cf_energies]
intensities = [Es_intensities, Bk_intensities, Cf_intensities]
# -------------- DETERMINING RELATIVE ACTIVITY OF ISOTOPES ------------------
# initial activities (as of 01/07/2020):
#        Es-254: 175 ng
#        Cf-250: 182 ng
#        Cf-249: 112 ng

# initial activites (as of email from Kevin Felker, fwd from Rebecca 10/22/2019) <-- these are the numbers used
#        Es-254: 233.8 ng
#        Es-253: 3.4 ng
#        Cf-250: 0 ng
#        Cf-249: 119 ng
#        Cf-252: 0.04 ng

# relevant decay chain:
#     Es-254 ------(100%, alpha)---->
#           Bk-250 -------(100%, beta)----->
#                  Cf-250------(100%, alpha)----->
#                         Cm-246-----(t1/2 = 4706years, assume chain ends here)
# all data in [Es-254, Bk-250, Cf-250, Cf-249] order
tonehalf = [275.7*24*3600, 3.212*3600, 13.08*365*24*3600, 351*365*24*3600] # half lives in seconds
lambdas = [0.69314718056/tonehalf[0],0.69314718056/tonehalf[1],0.69314718056/tonehalf[2],0.69314718056/tonehalf[3]] # seconds^-1
lambdasd = [lambdas[0]*3600*24, lambdas[1]*3600*24, lambdas[2]*3600*24, lambdas[3]*3600*24]
N_A = 6.022*(10**23)
specact = [lambdas[0]*N_A/254,lambdas[1]*N_A/250,lambdas[2]*N_A/250,lambdas[3]*N_A/249] # specific activities, Bq/g
mng = [233.8,0,0,119] #initial mass, nanograms
m0 = [mng[0]/1000/1000/1000, mng[1]/1000/1000/1000, mng[2]/1000/1000/1000, mng[3]/1000/1000/1000] #initial mass, grams
ABq = [specact[0]*m0[0], specact[1]*m0[1], specact[2]*m0[2], specact[3]*m0[3]] #initial activity (Bq)
#A0 = [1000*ABq[0]/(3.7*(10**10)), 1000*ABq[1]/(3.7*(10**10)), 1000*ABq[2]/(3.7*(10**10)), 1000*ABq[3]/(3.7*(10**10))] # initial activity (mCi)
A0 = [ABq[0]/(3.7*(10**10)), ABq[1]/(3.7*(10**10)), ABq[2]/(3.7*(10**10)), ABq[3]/(3.7*(10**10))] # initial activity (mCi)
A0mCi = [A0[0]*1000,A0[1]*1000,A0[2]*1000,A0[3]*1000]


# Einsteinium decay equations --------------------------------------------------
def Esactivity(x):
    At = A0mCi[0]*np.exp(-lambdas[0]*x)
    return At

def Esmass(x):
    mt = At * 3.7*10**7 /specact[0]
    return mt

# Berkelium decay equations ----------------------------------------------------
def Bkactivity(x):
    At = A0mCi[0] * (lambdas[1]/(lambdas[1]-lambdas[0])) * (np.exp(-lambdas[0]*x) - np.exp(-lambdas[1]*x)) + (A0[1] * np.exp(-lambdas[1]*x))
    return At

def Bkmass(x):
    mt = At * 3.7*10**7 /specact[1]
    return mt

# Californium decay equations --------------------------------------------------
def Cf250activity(x):
    At = A0mCi[0] * (lambdas[1]*lambdas[2]) * ((np.exp(-lambdas[0]*x) / ((lambdas[1]-lambdas[0]) * (lambdas[2] - lambdas[0]))) +
    (np.exp(-lambdas[1] * x) / ((lambdas[0] - lambdas[1]) * (lambdas[2] - lambdas[1]))) +
    (np.exp(-lambdas[2] * x) / ((lambdas[1] - lambdas[2]) * (lambdas[0] - lambdas[2])))) + A0mCi[1] * lambdas[2] * (np.exp(-lambdas[1] * x) - ((np.exp(-lambdas[2] * x) / (lambdas[2] - lambdas[1])))) + A0mCi[2] * np.exp(-lambdas[2] * x)
    return At

def Cf250mass(x):
    mt = At * 3.7*10**7 /specact[2]
    return mt

# Califnorium-249 decay equations ----------------------------------------------
def Cf249activity(t):
    At = A0mCi[3]*np.exp(-lambdas[3]*t)
    return At

def Cf249mass(t):
    mt = At * 3.7*10**7 /specact[3]
    return mt

# ACTIVITIES PLOT -------------------------------------------------------------
x = np.linspace(0,500,5000)
yEsact = A0mCi[0]*np.exp(-lambdasd[0]*x)
yBkact = A0mCi[0] * (lambdasd[1]/(lambdasd[1]-lambdasd[0])) * (np.exp(-lambdasd[0]*x) - np.exp(-lambdasd[1]*x)) + (A0mCi[1] * np.exp(-lambdasd[1]*x))
yCf250act = A0mCi[0] * (lambdasd[1]*lambdasd[2]) * ((np.exp(-lambdasd[0]*x) / ((lambdasd[1]-lambdasd[0]) * (lambdasd[2] - lambdasd[0]))) +
(np.exp(-lambdasd[1] * x) / ((lambdasd[0] - lambdasd[1]) * (lambdasd[2] - lambdasd[1]))) +
(np.exp(-lambdasd[2] * x) / ((lambdasd[1] - lambdasd[2]) * (lambdasd[0] - lambdasd[2])))) + A0mCi[1] * lambdasd[2] * (np.exp(-lambdasd[1] * x) - ((np.exp(-lambdasd[2] * x) / (lambdasd[2] - lambdasd[1])))) + A0mCi[2] * np.exp(-lambdasd[2] * x)
yCf249act = A0mCi[3]*np.exp(-lambdasd[3]*x)

fig = plt.figure(figsize=(10,10))
gs = gridspec.GridSpec(1,1)
ax1 = fig.add_subplot(gs[0])
ax1.set_title('Einsteinium Decay and Daughter Ingrowth')
ax1.set_xlabel('Time (days)')
ax1.set_ylabel('Activity (mCi)')

plt.plot(x,yEsact, color = 'b', label = 'Es-254')
plt.plot(x,yBkact, color = 'coral', linestyle = '--', label = 'Bk-250')
plt.plot(x,yCf249act, color = 'g', label = 'Cf-249')
plt.plot(x,yCf250act, color = 'g', linestyle = '--', label = 'Cf-250')
plt.legend()

new_tick_locations = [1,102,192, 284, 376, 468]
new_tick_labels = ["10/22/2019", "2/2/2020", "5/1/2020", "8/1/2020", "11/1/2020", "2/1/2021"]

ax2 = ax1.twiny()
ax2.set_xlim(ax1.get_xlim())
ax2.set_xticks(new_tick_locations)
ax2.set_xticklabels(new_tick_labels)
ax2.set_xlabel('Date')

# SAME PLOT WITH BOKEH --------------------------------------------------------
import bokeh
from bokeh.plotting import figure, output_file, show
output_file("Decay_Activities_Bokeh.html")
p = figure(
    tools = 'pan, box_zoom, reset, save',
    title = "Einsteinium Decay and Daughter Ingrowth (Activity)",
    x_axis_label = "Time (days)",
    y_axis_label = "Activity (mCi)"
)

p.line(x,yEsact,legend='Es254',line_color='blue')
p.line(x,yBkact,legend="Bk250",line_color='coral')
p.line(x,yCf249act,legend='Cf249',line_color='green',line_dash="4 4")
p.line(x,yCf250act,legend='Cf250',line_color='green')


#show(p)

# MASSES PLOT ------------------------------------------------------------------
x = np.linspace(0,500,5000)
yEsmass = yEsact * 3.7*10**7 /specact[0] * 1000 * 1000 * 1000
yBkmass = yBkact * 3.7*10**7 /specact[1] * 1000 * 1000 * 1000
yCf250mass = yCf250act * 3.7*10**7 /specact[2] * 1000 * 1000 * 1000
yCf249mass = yCf249act * 3.7*10**7 /specact[3] * 1000 * 1000 * 1000

fig = plt.figure(figsize=(10,10))
gs = gridspec.GridSpec(1,1)
ax1 = fig.add_subplot(gs[0])
ax1.set_title('Einsteinium Decay and Daughter Ingrowth')
ax1.set_xlabel('Time (days)')
ax1.set_ylabel('Mass (ng)')

plt.plot(x,yEsmass, color = 'b', label = 'Es-254')
plt.plot(x,yBkmass, color = 'coral', linestyle = '--', label = 'Bk-250')
plt.plot(x,yCf249mass, color = 'g', label = 'Cf-249')
plt.plot(x,yCf250mass, color = 'g', linestyle = '--', label = 'Cf-250')
plt.legend()

new_tick_locations = [1,102,192, 284, 376, 468]
new_tick_labels = ["10/22/2019", "2/2/2020", "5/1/2020", "8/1/2020", "11/1/2020", "2/1/2021"]

ax2 = ax1.twiny()
ax2.set_xlim(ax1.get_xlim())
ax2.set_xticks(new_tick_locations)
ax2.set_xticklabels(new_tick_labels)
ax2.set_xlabel('Date')

# SAME PLOT IN BOKEH -------------------------------
output_file("Decay_Mass_Bokeh.html")
p = figure(
    tools = 'pan, box_zoom, reset, save',
    title = "Einsteinium Decay and Daughter Ingrowth (Mass)",
    x_axis_label = "Time (days)",
    y_axis_label = "Mass (ng)"
)

p.line(x,yEsmass,legend='Es254',line_color='blue')
p.line(x,yBkmass,legend="Bk250",line_color='coral')
p.line(x,yCf249mass,legend='Cf249',line_color='green',line_dash="4 4")
p.line(x,yCf250mass,legend='Cf250',line_color='green')

# GAMMA DEPENDENCIES on TIME --------------------------------------------------
def Esactivity(x):
    At = A0mCi[0]*np.exp(-lambdasd[0]*x)
    return At

def Bkactivity(x):
    At = A0mCi[0] * (lambdasd[1]/(lambdasd[1]-lambdasd[0])) * (np.exp(-lambdasd[0]*x) - np.exp(-lambdasd[1]*x)) + (A0[1] * np.exp(-lambdasd[1]*x))
    return At

def Cf250activity(x):
    At = A0mCi[0] * (lambdasd[1]*lambdasd[2]) * ((np.exp(-lambdasd[0]*x) / ((lambdasd[1]-lambdasd[0]) * (lambdasd[2] - lambdasd[0]))) +
    (np.exp(-lambdasd[1] * x) / ((lambdasd[0] - lambdasd[1]) * (lambdasd[2] - lambdasd[1]))) +
    (np.exp(-lambdasd[2] * x) / ((lambdasd[1] - lambdasd[2]) * (lambdasd[0] - lambdasd[2])))) + A0mCi[1] * lambdasd[2] * (np.exp(-lambdasd[1] * x) - ((np.exp(-lambdasd[2] * x) / (lambdasd[2] - lambdasd[1])))) + A0mCi[2] * np.exp(-lambdasd[2] * x)
    return At

def Cf249activity(t):
    At = A0mCi[3]*np.exp(-lambdasd[3]*t)
    return At


activities = [Esactivity(time),Bkactivity(time),Cf249activity(time)]

def gammaplot(time, file_name):
    filename = str(file_name)+".html"
    output_file(filename)
    p = figure(title = 'Simulated gamma spectrum of Es-254, Bk-250, Cf-249', )
    choosecolor = ["blue","coral", "green"]
    activities = np.array([Esactivity(time),Bkactivity(time),Cf249activity(time)])
    elementlist = ['Es-254', 'Bk-250', 'Cf-249']
    energies = [Es_energies, Bk_energies, Cf_energies]
    intensities0 = np.array([np.array(Es_intensities), np.array(Bk_intensities), np.array(Cf_intensities)])
    for i in range(0,3):
        print (i)
        element = elementlist[i]
        energylist = energies[i]
        intensitylist = intensities0[i]
        color = choosecolor[i]
        activity = activities[i]
        intensities = [j * activity for j in intensitylist]
        p.vbar(x=energylist, width = 1, bottom = 0, top = intensities, color = color, legend = element)
    show(p)

filename = str(file_name)+".html"
output_file(filename)
p = figure(title = 'Simulated gamma spectrum of Es-254, Bk-250, Cf-249', )
choosecolor = np.array(["blue","coral", "green"])
activities = np.array([Esactivity(time),Bkactivity(time),Cf249activity(time)])
elementlist = ['Es-254', 'Bk-250', 'Cf-249']
energies = [Es_energies, Bk_energies, Cf_energies]
intensities0 = np.array([np.array(Es_intensities), np.array(Bk_intensities), np.array(Cf_intensities)])

for i in range(0,3):
    print (i)
    element = elementlist[i]
    energylist = energies[i]
    intensitylist = intensities0[i]
    color = choosecolor[i]
    activity = activities[i]
    intensities = [j * activity for j in intensitylist]
    p.vbar(x=energylist, width = 1, bottom = 0, top = intensities, color = color, legend = element)

show(p)




        if element in {'Es','Es254','Es-254','254Es'}:
            energies = Es_energies
            choosecolor = 'blue'
            activity = Esactivity(time)
            intensities = [i * activity for i in Es_intensities]
            p.vbar(x=energies, width = 1, bottom = 0, top = intensities, color = choosecolor, legend = element)
        elif element in {'Bk','Bk250','Bk-250','250Bk'}:
            energies = Bk_energies
            choosecolor = 'coral'
            activity = Bkactivity(time)
            intensities = [i * activity for i in Bk_intensities]
            p.vbar(x=energies, width = 1, bottom = 0, top = intensities, color = choosecolor)
        elif element in {'Cf', 'Cf249','249Cf','Cf-250'}:
            energies = Cf_energies
            choosecolor = 'green'
            activity = Cf249activity(time)
            intensities = [i * activity for i in Cf_intensities]
            p.vbar(x=energies, width = 1, bottom = 0, top = intensities, color = choosecolor)
        else:
            print ("uhoh. Isotope not recognized.")
    show(p)


def Esactivity(x):
    At = A0mCi[0]*np.exp(-lambdasd[0]*x)
    return At
#    Es intensity at time (t):
times = [50, 100, 150, 200, 250]
colors = ['k','b','r','g','y','k']
i=0
for x in times:
    Es_intensities_activity = [i * Esactivity(x) for i in Es_intensities]
    j = times[i]/50
    print(i)
    j = int(j)
    print(colors[j])
    i = i+1
    Es_gammas=[]
    for gamma in range(0,len(Es_energies)):
        entry = np.random.normal(Es_energies[gamma],1/Es_intensities_activity[gamma],1000)
        Es_gammas.append(entry)
    for gamma in Es_gammas:
        sns.distplot(gamma,color=colors[j])



# -----------------------------------------------------------------------------

from bokeh.io import output_file, show
from bokeh.models import Slider

output_file("slider.html")

slider = Slider(start=0, end=10, value=1, step=.1, title="Stuff")

show(slider)



def make_dataset(data, )

times = [50, 100, 150, 200, 250]
colors = ['k','b','r','g','y','k']
i=0
for x in times:
    Es_intensities_activity = [i * Esactivity(x) for i in Es_intensities]
    j = times[i]/50
    print(i)
    j = int(j)
    print(colors[j])
    i = i+1
    Es_gammas=[]
    for gamma in range(0,len(Es_energies)):
        entry = np.random.normal(Es_energies[gamma],1/Es_intensities_activity[gamma],1000)
        Es_gammas.append(entry)
    for gamma in Es_gammas:
        sns.distplot(gamma,color=colors[j])














#------------

# Peak fitting adapted from Emily Ripka's.
# Blog post here:
# ipynb here:

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
import numpy as np
import scipy as scipy
from scipy import optimize
from matplotlib.ticker import AutoMinorLocator
from matplotlib import gridspec
import matplotlib.ticker as ticker

# Define a small segment to work on for now.
#datan = pd.read_csv(os.path.join('c:\\Users\\Kathy Shield\\Desktop\\Berkeley\\AbergelGroup\\Research\\Emily+Hailie-Fr223\\Elutions2019\\1.spe'))
from gamma_import import gamma_import
def _1gaussian(x, amp1, cen1, sigma1):
    return amp1*(1/(sigma1*(np.sqrt(2*np.pi))))*(np.exp((-1.0/2.0)*(((x_array-cen1)/sigma1)**2)))

def extractdata_50keV(data_fr, fraction):
    data_today = data_fr.iloc[400:550,[0,19]]
    x_array = data_today['Energy (keV)'].tolist()
    y_array_gauss = data_today[fraction].tolist()
    print ('i did stuff')
    return data_today, x_array, y_array_gauss

def calculategauss_50keV(x_array, y_array_gauss):
    cen1 = 50
    sigma1 = 5
    amp1 = 200
    popt_gauss, pcov_gauss = scipy.optimize.curve_fit(_1gaussian, x_array, y_array_gauss, p0=[amp1, cen1, sigma1])
    perr_gauss = np.sqrt(np.diag(pcov_gauss))

data_fr = gamma_import()
for fraction in range(0,5):
    fraction = str(fraction)
    data_today = data_fr.iloc[400:550]
    x_array = data_today['Energy (keV)'].values.ravel()
    y_array_gauss = data_today[fraction].tolist()
    calculategauss_50keV(x_array, y_array_gauss)
    ax1.plot(x_array, y_array_gauss, "k.")
    ax1.plot(x_array, _1gaussian(x_array, *popt_gauss), 'k--')


# amp1 = 100
# cen1 = 50
# sigma1 = 2

    # this cell prints the fitting parameters with their errors
popt_gauss, pcov_gauss = scipy.optimize.curve_fit(_1gaussian, x_array, y_array_gauss, p0=[amp1, cen1, sigma1])
perr_gauss = np.sqrt(np.diag(pcov_gauss))
print( "amplitude = " ,popt_gauss[0],"+/-", perr_gauss[0])

fig = plt.figure(figsize=(4,3))
gs = gridspec.GridSpec(1,1)
ax1 = fig.add_subplot(gs[0])
ax1.plot(x_array, y_array_gauss, "k.")
ax1.plot(x_array, _1gaussian(x_array, *popt_gauss), 'k--')



x2_array = data_fr.loc[2400:2600,['Energy (keV)']].as_matrix()
x2_array = x2_array.ravel()
y_array_2gauss = data_fr.loc[2400:2600,1].as_matrix()

def _2gaussian(x, amp1,cen1,sigma1, amp2,cen2,sigma2):
    return amp1*(1/(sigma1*(np.sqrt(2*np.pi))))*(np.exp((-1.0/2.0)*(((x2_array-cen1)/sigma1)**2))) + \
    amp2*(1/(sigma2*(np.sqrt(2*np.pi))))*(np.exp((-1.0/2.0)*(((x2_array-cen2)/sigma2)**2)))
def _2gaussianA(x,amp1,cen1,sigma1):
    return amp1*(1/(sigma1*(np.sqrt(2*np.pi))))*(np.exp((-1.0/2.0)*(((x2_array-cen1)/sigma1)**2)))

popt_2gauss, pcov_2gauss = scipy.optimize.curve_fit(_2gaussian, x2_array, y_array_2gauss, p0=[amp1, cen1, sigma1, amp2, cen2, sigma2])
perr_2gauss = np.sqrt(np.diag(pcov_2gauss))
pars_1 = popt_2gauss[0:3]
pars_2 = popt_2gauss[3:6]
gauss_peak_1 = _2gaussianA(x2_array, *pars_1)
gauss_peak_2 = _2gaussianA(x2_array, *pars_2)

fig = plt.figure(figsize=(4,3))
gs = gridspec.GridSpec(1,1)
ax1 = fig.add_subplot(gs[0])
ax1.plot(x2_array, y_array_2gauss, "k.")
ax1.plot(x2_array, gauss_peak_1, '--g')
ax1.plot(x2_array, gauss_peak_2, '--b')


bkgd_data_fr.plot(x='Energy (keV)', y=range(1,18), legend=False,colormap='Blues',xlim=(0,500),title="Fr Data")

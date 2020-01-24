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

from gamma_import import gamma_import
data_fr = gamma_import()
print ("Data imported")

data_today = data_fr.iloc[400:550,[0,19]]
x_array = data_today['Energy (keV)'].values.ravel()
y_array_gauss = data_today[1].values.ravel()

print (x_array)
print(y_array_gauss)

cen1 = input('Center: ')
amp1 = input('Amplitude: ')
sigma1 = input('Sigma: ')
cen1 = int(cen1)
amp1 = int(amp1)
sigma1 = int(sigma1)
# cen1 = 50
# amp1 = 100
# sigma1 = 2

def _1gaussian(x, amp1, cen1, sigma1):
    return amp1*(1/(sigma1*(np.sqrt(2*np.pi))))*(np.exp((-1.0/2.0)*(((x_array-cen1)/sigma1)**2)))
popt_gauss, pcov_gauss = scipy.optimize.curve_fit(_1gaussian, x_array, y_array_gauss, p0=[amp1, cen1, sigma1])
perr_gauss = np.sqrt(np.diag(pcov_gauss))
print( "amplitude = " ,popt_gauss[0],"+/-", perr_gauss[0])


fig = plt.figure(figsize=(4,3))
gs = gridspec.GridSpec(1,1)
ax1 = fig.add_subplot(gs[0])
ax1.plot(x_array, y_array_gauss, "k.")
ax1.plot(x_array, _1gaussian(x_array, *popt_gauss), 'k--')
plt.show()

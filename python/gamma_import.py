import os
import pandas as pd
import numpy as np
import datetime
import csv
import ggplot
from ggplot import *
import plotnine as p9


# Import data into a pandas dataframe
def gamma_import():
    # build blank dataframes to fill
    data_fr = pd.DataFrame() # raw counts from all the measurements
    cpm_data_fr = pd.DataFrame() # all data converted to cpm
    bkgd_data_fr = pd.DataFrame() # background subtracted cpm data from the fractions
    parameters_fr = pd.DataFrame()
    bkgd_data = pd.DataFrame()
    # START WITH THE BACKGROUND DATA
    # import the background spectrum
    datan = pd.read_csv(os.path.join('c:\\Users\\Kathy Shield\\Desktop\\Berkeley\\AbergelGroup\\Research\\Emily+Hailie-Fr223\\Elutions2019\\background.spe'))

    # pull out info about the energy spectrum of the HPGe
    energyindex = datan.index[datan['$SPEC_ID:'] == '$ENER_FIT:'] # find the right row
    fit_parameters = datan.loc[energyindex[0]+1].values[0]
    parameters = fit_parameters.split() # split m and b in y=mx+b
    energy_intercept = float(parameters[0])
    energy_slope = float(parameters[1])
    # create energy parameters for use later
    paradf = [time_live, time_real, energy_intercept, energy_slope]

    # convert background to usable data format...
    data = datan.loc[11:8202] # only the numbers
    data = data.reset_index(drop=True)
    data = data.rename(columns={'$SPEC_ID:':'b'}) # give it a useful name
    data = data.astype('int64') # convert to integers
    data_fr = pd.concat([data_fr,data],axis=1) # save the background into the full DataFrame

    # use the time info in the file to convert from counts to cpm
    time = datan.loc[8].values[0]
    times = time.split()
    time_live = float(times[0])
    time_real = float(times[1])
    background_cpm_data = (data*60)/time_live

    # save the data into actual files for later
    cpm_data_fr = pd.concat([cpm_data_fr,background_cpm_data],axis=1)

    print ("running file")
    # complete the above procedures for EACH fraction
    for file in range(1,19):
        filex = file
        file = str(file)
        datan = pd.read_csv(os.path.join('c:\\Users\\Kathy Shield\\Desktop\\Berkeley\\AbergelGroup\\Research\\Emily+Hailie-Fr223\\Elutions2019\\',file+'.spe'))
        data = datan.loc[11:8202]
        data = data.reset_index(drop=True)
        data = data.rename(columns={'$SPEC_ID:':filex})
        data = data.astype('int64')
        data_fr = pd.concat([data_fr,data],axis=1)
        time = datan.loc[8].values[0]
        times = time.split()
        time_live = float(times[0])
        time_real = float(times[1])
        energyindex = datan.index[datan['$SPEC_ID:'] == '$ENER_FIT:']
        fit_parameters = datan.loc[energyindex[0]+1].values[0]
        parameters = fit_parameters.split()
        energy_intercept = float(parameters[0])
        energy_slope = float(parameters[1])
        paradf = [time_live, time_real, energy_intercept, energy_slope]
        parameters_fr['Fraction '+file] = paradf
        cpm_data = (data*60)/time_live
        cpm_data_fr = pd.concat([cpm_data_fr,cpm_data],axis=1)
        bkgd_data[filex] = cpm_data[filex].sub(background_cpm_data['b'])
        bkgd_data_fr = pd.concat([bkgd_data_fr,bkgd_data[filex]],axis=1) # p.sure this line and the previous could be combined

        #combine it all
        data_fr['Channel'] = data_fr.reset_index().index
        data_energy = pd.Series(data_fr['Channel'] * energy_slope + energy_intercept,name = 'Energy (keV)')
        data_fr = pd.concat([data_fr,data_energy],axis=1)
        cpm_data_fr = pd.concat([cpm_data_fr,data_energy],axis=1)
        bkgd_data_fr = pd.concat([bkgd_data_fr,data_energy],axis=1)
        #melted = pd.melt(bkgd_data_fr, id_vars = ['Energy (keV)'], var_name = 'Fraction')
    return bkgd_data_fr
    print ("returned complete data set in counts per minute and background subtracted")

#
# def function2():
#     # Format the actual data into dataframe
#     ## only take the data - ignore the initial and final parameters
#     data = datan.loc[11:8202]
#     ## reset the column name to the ID of the run, set channel numbers as indices
#     data = data.reset_index(drop=True)
#     data = data.rename(columns={'$SPEC_ID:':filex})
#     ## convert data to integers (from strings)
#     data = data.astype('int64')
#     ## add the data to a complete dataframe
#     data_fr = pd.concat([data_fr,data],axis=1)
#
#     # Extract the Counting Time from the dataframe
#     time = datan.loc[8].values[0]
#     times = time.split()
#     time_live = float(times[0])
#     time_real = float(times[1])
#
#     # Extract the Energy Fit Parameters from the dataframe
#     energyindex = datan.index[datan['$SPEC_ID:'] == '$ENER_FIT:']
#     fit_parameters = datan.loc[energyindex[0]+1].values[0]
#     parameters = fit_parameters.split()
#     energy_intercept = float(parameters[0])
#     energy_slope = float(parameters[1])
#
#     # Add to the parameters dataframe
#     paradf = [time_live, time_real, energy_intercept, energy_slope]
#     parameters_fr['Fraction '+file] = paradf
#
#     # Make a time-normalized dataframe
#     cpm_data = (data*60)/time_live
#     cpm_data_fr = pd.concat([cpm_data_fr,cpm_data],axis=1)
#
#     # Add the channel numbers & energy values to the dataframe
#     data_fr['Channel'] = data_fr.reset_index().index
#     data_energy = pd.Series(data_fr['Channel'] * energy_slope + energy_intercept,name = 'Energy (keV)')
#     data_fr = pd.concat([data_fr,data_energy],axis=1)
#     cpm_data_fr = pd.concat([cpm_data_fr,data_energy],axis=1)
#
#     # Import background as column 'b'
#     datan = pd.read_csv(os.path.join('c:\\Users\\Kathy Shield\\Desktop\\Berkeley\\AbergelGroup\\Research\\Emily+Hailie-Fr223\\Elutions2019\\background.spe'))
#     data = datan.loc[11:8202]
#     data = data.reset_index(drop=True)
#     data = data.rename(columns={'$SPEC_ID:':'b'})
#     data = data.astype('int64')
#     data_fr = pd.concat([data_fr,data],axis=1)
#     time = datan.loc[8].values[0]
#     times = time.split()
#     time_live = float(times[0])
#     time_real = float(times[1])
#     energyindex = datan.index[datan['$SPEC_ID:'] == '$ENER_FIT:']
#     fit_parameters = datan.loc[energyindex[0]+1].values[0]
#     parameters = fit_parameters.split()
#     energy_intercept = float(parameters[0])
#     energy_slope = float(parameters[1])
#     paradf = [time_live, time_real, energy_intercept, energy_slope]
#     parameters_fr['Fraction '+file] = paradf
#     cpm_data = (data*60)/time_live
#     cpm_data_fr = pd.concat([cpm_data_fr,cpm_data],axis=1)
#
#     #background subtract
#
#     #Melt the data to make plotting with ggplot possible
#     melted = pd.melt(cpm_data_fr, id_vars = ['Energy (keV)'], var_name = 'Fraction')
#print (melted[8100:8300])
#
# colors = [['#440154FF'],
# ['#440154FF'],
# ['#481567FF'],
# ['#482677FF'],
# ['#453781FF'],
# ['#404788FF'],
# ['#39568CFF'],
# ['#33638DFF'],
# ['#2D708EFF'],
# ['#287D8EFF'],
# ['#238A8DFF'],
# ['#1F968BFF'],
# ['#20A387FF'],
# ['#29AF7FFF'],
# ['#3CBB75FF'],
# ['#55C667FF'],
# ['#73D055FF'],
# ['#95D840FF'],
# ['#B8DE29FF'],
# ['#DCE319FF'],
# ['#FDE725FF']]
#plots = []
##ggstring = 'ggplot(data_fr, aes(x="Energy (keV)"))'
#for fraction in range(1,19):
#    fraction = str(fraction)
#    filename = 'Fraction '+ fraction
#    plot = "+ geom_line(aes("+filename+"), color = colors["+ fraction +"]))"
#    plots.append(plot)
#    ggstring += plot
#joined = ''.join(plots)
#ggstring += ')'

#print (ggstring)
#print(plots)
#print (joined)
#print (type(joined))
# print (p9.ggplot(data=melted,
# mapping=p9.aes(x='Energy (keV)', y='value', color='Fraction'))
# + p9.geom_point()
# #+ p9.scale_color_grey()
# + p9.scale_color_cmap_d(name='cividis_r')
# + p9.scale_x_continuous(breaks = range(0, 600, 50))
# + p9.scale_y_continuous(breaks = range(0, 4000, 200), expand = (0,5))
# )
#+ geom_line(aes(y='Fraction 2'), color = "steelblue")

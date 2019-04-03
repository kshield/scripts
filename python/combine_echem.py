#!/c/Users/Public/python
# -*- coding: utf-8 -*-
#"""
#Created on Tue May  8 13:40:20 2018
#@author: Kathy Shield
#"""

# KMS May 8 2018. This script imports csv files from either the LSC output directly
# or the splitLSC.sh outputs. It accepts user inputs about the variables and saves
# the data into individual files for each experiment and
# (eventually) into a massive dataframe
# with all the data from all extraction experiments performed by the user.

# First, import the things you need.

# This includes packages
import os
import glob
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

datafolder = 'c:\\Users\\Kathy Shield\\Desktop\\Berkeley\\AbergelGroup\\Research\\Echem\\'
datafiles = 'c:\\Users\\Kathy Shield\\Desktop\\Berkeley\\AbergelGroup\\Research\\Echem\\*.csv'
rows = ['Length (m)'] #starting with this because it is the first column title
ticker = 0 #to enable a different first from nth parsing
for file in glob.glob(datafiles):
    print (file) #lets me know the program is running
    data = pd.read_csv(os.path.join(datafolder,file)) #make the csv file
    data = np.transpose(data) #transpose b/c I already know how to add rows/adding columns is probably just as easy
    if ticker == 0: #for first data file
        ticker += 1 #add to the ticker
        new_header = data.iloc[0] #keep the first row (lengths) - doesn't keep the "length (m)" name, so I added it into the initial rows list
        filldata = data.iloc[1] #the second row  is the data (there are only two rows in each data file)
        allthedata = pd.concat([new_header,filldata], 1,  ignore_index=True) #combine the two rows into a new dataframe.
        rowname = file.split("at ")[1] #extract the voltage value out of the file name
        rowname = rowname.split(".c")[0]
        rows.append(rowname) #add the voltage value to the rows list
    elif ticker != 0: #everything here is the same except we don't keep the first row (lengths) b/c its always the same
        ticker += 1
        newdata = data.iloc[1]
        allthedata = pd.concat([allthedata,newdata], 1,  ignore_index=True)
        rowname = file.split("at ")[1]
        rowname = rowname.split(".c")[0]
        rows.append(rowname)
rows = pd.Series(rows) #the series can get turned into column names (a list can't)
rows = rows.T #transpose to match the data
allthedata.columns = rows #redefine column names
path = '~\\Desktop\\Berkeley\\AbergelGroup\\Research\\Echem\\'
allthedata.to_csv(datafolder+'allthedata.csv', index=False) #save the file
print ('done!')

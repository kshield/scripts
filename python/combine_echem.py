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
rows = ['Length (m)']
for file in glob.glob(datafiles):
    data = pd.read_csv(os.path.join(datafolder,file))
    data = np.transpose(data)
    if '01)' in file:
        new_header = data.iloc[0]
        filldata = data.iloc[1]
        allthedata = pd.concat([new_header,filldata], 1,  ignore_index=True)
        rowname = file.split("at ")[1]
        rowname = rowname.split(".c")[0]
        rows.append(rowname)
    elif '01)' not in file:
        newdata = data.iloc[1]
        allthedata = pd.concat([allthedata,newdata], 1,  ignore_index=True)
        rowname = file.split("at ")[1]
        rowname = rowname.split(".c")[0]
        rows.append(rowname)
rows = pd.Series(rows)
rows = rows.T
allthedata.columns = rows
allthedata.to_csv(datafolder+'allthedata.csv', index=False)
print ('done!')

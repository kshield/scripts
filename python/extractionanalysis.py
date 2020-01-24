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
import time
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import datetime
import plotly as py
import plotly.graph_objs as go
py.tools.set_credentials_file(username = 'kshield', api_key = 'H9UX6nYroLdbt1W1pjgj')

# find the csv file that exists with ALL the data - this is where we'll eventually add the data at the end of the day
allthedataframe = pd.read_csv(os.path.join('c:\\Users\\Kathy Shield\\Desktop\\Berkeley\\AbergelGroup\\Research\\Extractions\\Results\\ProcessedDataFiles','allthedata.csv'))

##########################################  DATA FROM LSC OUTPUT FILES ######################################
def importdata(filename):
    # make an empty dataframe to import data into
    df_fillmein = pd.DataFrame()
    df_fillmein.reset_index(drop=True, inplace=True)

    # import the data as is from the (truncated) LSC output
    df_LSCoutput = pd.read_csv(filename)
    # split the file into aqueous and organic components
    df_LSCoutput_aqueous = df_LSCoutput.iloc[::2]
    df_LSCoutput_organic = df_LSCoutput.iloc[1::2]
    # reset the indices so they are the same for each table (row 0 aq = row 0 org)
    df_LSCoutput_aqueous.reset_index(drop=True, inplace=True)
    df_LSCoutput_organic.reset_index(drop=True, inplace=True)
    print (df_LSCoutput_aqueous)
    # take the data from the LSC outputs and add to our dataframe for filling in
    df_fillmein["AqCPMA"] = df_LSCoutput_aqueous.CPMA
    if "CPMB" in df_LSCoutput_aqueous.columns:
        df_fillmein["AqCPMB"] = df_LSCoutput_aqueous.CPMB
    if "CPMC" in df_LSCoutput_aqueous.columns:
        df_fillmein["AqCPMC"] = df_LSCoutput_aqueous.CPMC
    if "CPMa" in df_LSCoutput_aqueous.columns:
        df_fillmein["AqCPMC"] = df_LSCoutput_aqueous.CPMa
    df_fillmein["Aqueous LSC Vial"] = df_LSCoutput_aqueous['S#']

    df_fillmein["Count Time"] = df_LSCoutput_organic['Count Time'] # this will create errors in the table for Ce-134 data from Dec 2018 b/c count times were inconsistent
    df_fillmein["Date"] = df_LSCoutput_aqueous.DATE
    date = datetime.datetime.strptime(df_fillmein.loc[0,'Date'],'%m/%d/%Y').strftime('%Y%m%d')

    df_fillmein["OrgCPMA"] = df_LSCoutput_organic.CPMA
    if "CPMB" in df_LSCoutput_organic.columns:
        df_fillmein["OrgCPMB"] = df_LSCoutput_organic.CPMB
    if "CPMC" in df_LSCoutput_organic.columns:
        df_fillmein["OrgCPMC"] = df_LSCoutput_organic.CPMC
    if "CPMa" in df_LSCoutput_organic.columns:
        df_fillmein["OrgCPMC"] = df_LSCoutput_organic.CPMa
    df_fillmein["Organic LSC Vial"] = df_LSCoutput_organic['S#']
    print (df_fillmein)
    return (df_fillmein, df_LSCoutput_aqueous, df_LSCoutput_organic, date)
##########################################  HUMAN INPUT ABOUT INDEPENDENT VARIABLES #########################
def atypicalrun(orgaliquotfactor = 2, aqaliquotfactor = 1):
    def aqueous_varies():
        aqueous_ligand = input('What were the aqueous ligands? (provide ALL CAPS 3-4 letter abbreviations, comma separated): ')
        df_fillmein['Ligand'] = aqueous_ligand
    def aqueous_constant():
        # Input
        aqueous_ligand = input('What was the aqueous ligand? ')
        df_fillmein.loc[:,'Ligand'] = aqueous_ligand
        print(aqueous_ligand)
    def aqueous_concentration_varies():
        triplicate = input ('Is this data in triplicate? (y/n):')
        aqueous_concentrations = input('Please input the aqueous concentrations (mM), comma separated: ')
        # Convert the string into float values (allows for decimals; necessary for numerical entries)
        aqueous_concentrations = [float(x) for x in aqueous_concentrations.split(',')]
        aqueous_concentrations = pd.Series(aqueous_concentrations).values
        if triplicate == 'y':
            aqueous_concentrations = np.tile (aqueous_concentrations,3)
            # Make the list repeat three times
            print (aqueous_concentrations)
        # Convert the floats into a series of values in pandas.
        df_fillmein['Ligand Concentration (mM)'] = aqueous_concentrations
        return (triplicate)
    def aqueous_concentration_constant():
        aqueous_concentrations = input('Please input the aqueous concentration (mM): ')
        aqueous_concentrations = float(aqueous_concentrations)
        datasplit_aqueous.loc[:,'Aq_Conc (mM)'] = aqueous_concentrations
    def pH_varies():
        ph = input('What were the starting pH values? (Input as comma separated numbers): ')
        ph = [float(x) for x in ph.split(',')]
        ph = pd.Series(ph).values
        df_fillmein['Initial pH'] = ph
    def pH_constant():
        ph = input('What was the starting pH? ')
        df_fillmein.loc[:,'Initial pH'] = ph
    def organic_ligand_varies():
        organic_ligand = input("What were the organic extractants? (Input in ALL CAPS, comma separated): ")
        df_fillmein['Extractant'] = organic_ligand
    def organic_ligand_constant():
        organic_ligand = input('What was the organic extractant? (Input in ALL CAPS): ')
        df_fillmein.loc[:,'Extractant'] = organic_ligand
        extractant = organic_ligand
    def organic_concentration_varies():
        organic_concentrations = input ('Please input the organic concentrations (M): ')
        organic_concentrations = [float(x) for x in organic_concentrations.split(',')]
        organic_concentrations = pd.Series(organic_concentrations).values
        df_fillmein['Extractant Concentration (M)'] = organic_concentrations
    def organic_concentration_constant():
        organic_concentrations = input('What was the organic concentration (M)? ')
        df_fillmein.loc[:,'Extractant Concentration (M)'] = organic_concentrations
    def metal_varies():
        isotope = input("What were the isotopes? ")
        isotope = pd.Series(isotope).values
        df_fillmein['Isotope'] = isotope
    def metal_constant():
        isotope = input('What isotope? ')
        df_fillmein.loc[:,'Isotope'] = isotope
        return (isotope)
    def buffer_varies():
        buffer = input("What were the buffers? (Input comma separated): ")
        df_fillmein['Buffer'] = buffer
    def buffer_constant():
        buffer = input('What was the buffer? ')
        df_fillmein.loc[:,'Buffer'] = buffer
    def buffer_concentration_varies():
        buffer_concentrations = input ('Please input the buffer concentrations (mM): ')
        buffer_concentrations = [float(x) for x in buffer_concentrations.split(',')]
        buffer_concentrations = pd.Series(buffer_concentrations).values
        df_fillmein['Buffer Concentration (mM)'] = buffer_concentrations
    def buffer_concentration_constant():
        buffer_concentrations = input('What was the buffer concentration (mM)? ')
        df_fillmein.loc[:,'Buffer Concentration (mM)'] = buffer_concentrations
    varies = input ('What varies? PICK ONE: aql, aqconc, ph, orgl, orgconc, isotope, buffer, bufferconc  > ')
    volumevaried = input ('Were the volumes 100 uL aqueous/200 uL organic? (y/n): ')
    if volumevaried == 'n':
        orgvolume = input ('What was the organic aliquot volume? (uL): ')
        orgvolume = float (orgvolume)
        orgaliquotfactor = orgvolume/100
        aqvolume = input ('What was the aqueous aliquot volume? (uL): ')
        aqvolume = float (aqvolume)
        aqaliquotfactor = aqvolume/100
    if varies == 'aql':
        print ('Okay! The aqueous ligand varies.')
        aqueous_varies()
        aqueous_concentration_constant()
        pH_constant()
        organic_ligand_constant()
        organic_concentration_constant()
        isotope = metal_constant()
        buffer_constant()
        buffer_concentration_constant()
        ligandtype = input('What class of Ligands were used? (Carboxylic Acids, HOPO Derivatives): ')
        independentvariabletitle = 'Varying '+ligandtype
    elif varies == 'aqconc':
        print('Okay! The concentration of the aqueous ligand varies.')
        ligand = aqueous_constant()
        triplicate = aqueous_concentration_varies()
        pH_constant()
        organic_ligand_constant()
        organic_concentration_constant()
        isotope = metal_constant()
        buffer_constant()
        buffer_concentration_constant()
        independentvariabletitle = ligand
    elif varies == 'ph':
        print ('Okay. The starting pH is changing.')
        aqueous_constant()
        aqueous_concentration_constant()
        pH_varies()
        organic_ligand_constant()
        organic_concentration_constant()
        isotope = metal_constant()
        buffer_constant()
        buffer_concentration_constant()
        independentvariabletitle = 'Varying Initial pH'
    elif varies == "orgl":
        print ('Okay, the organic ligand varies.')
        ligand = aqueous_constant()
        aqueous_concentration_constant()
        pH_constant()
        organic_ligand_varies()
        organic_concentration_constant()
        isotope = metal_constant()
        buffer_constant()
        buffer_concentration_constant()
        independentvariabletitle = ligand
    elif varies == 'orgconc':
        print ('Okay! The concentration of the organic ligand varies.')
        aqueous_constant()
        aqueous_concentration_constant()
        pH_constant()
        extractant = organic_ligand_constant()
        organic_concentration_varies()
        isotope = metal_constant()
        buffer_constant()
        buffer_concentration_constant()
        independentvariabletitle = extractant
    elif varies == "isotope":
        print ('Got it. The metal is changing.')
        ligand = aqueous_constant()
        aqueous_concentration_constant()
        pH_constant()
        organic_ligand_constant()
        organic_concentration_constant()
        metal_varies()
        buffer_constant()
        buffer_concentration_constant()
        independentvariabletitle = ligand
    elif varies == 'buffer':
        print ('Sure thing. The buffer is different.')
        aqueous_constant()
        aqueous_concentration_constant()
        pH_constant()
        organic_ligand_constant()
        organic_concentration_constant()
        isotope = metal_constant()
        buffer_varies()
        buffer_concentration_constant()
        independentvariabletitle = 'Various Buffers'
    elif varies == 'bufferconc':
        print ('Okie dokes. The buffer concentration changes.')
        aqueous_constant()
        aqueous_concentration_constant()
        pH_constant()
        organic_ligand_constant()
        organic_concentration_constant()
        isotope = metal_constant()
        buffer = buffer_constant()
        buffer_concentration_varies()
        independentvariabletitle = buffer
    return (orgaliquotfactor, aqaliquotfactor, isotope, triplicate, independentvariable, extractant, ligand)

def parameters(df_fillmein, buffer = 'MES', buffer_conc = 100, extractant = 'HDEHP', extractant_conc = 0.0025, pH = 6, independentvariable = 'Ligand Concentration (mM)'):
    # Find out if we're dealing with the most common experiment (ligand concentration varies)
    normal = input('Is this normal (ligand concentration varying)? (y/n): ')
    if normal == 'y':
    # define the things that change
        isotope = input('What isotope? ')
        ligand = input('What was the aqueous ligand? ')
        triplicate = input ('Is this data in triplicate? (y/n):')
        ligand_conc = input('Please input the aqueous concentrations (mM), comma separated: ')
        ligand_conc = [float(x) for x in ligand_conc.split(',')]
        if triplicate == 'y':
            ligand_conc = ligand_conc + ligand_conc + ligand_conc
        aqaliquotfactor = 1
        orgaliquotfactor = 2
        # put all the parameters into the dataframe
        df_fillmein.loc[:,'Buffer'] = buffer
        df_fillmein.loc[:,'Buffer Concentration (mM)'] = buffer_conc
        df_fillmein.loc[:,'Extractant'] = extractant
        df_fillmein.loc[:,'Extractant Concentration (M)'] = extractant_conc
        df_fillmein.loc[:,'Initial pH'] = pH
        df_fillmein.loc[:,'Isotope'] = isotope
        df_fillmein.loc[:,'Ligand'] = ligand
        df_fillmein['Ligand Concentration (mM)'] = ligand_conc
    else:
        orgaliquotfactor, aqaliquotfactor, isotope, triplicate = atypicalrun()
    return (df_fillmein, aqaliquotfactor, orgaliquotfactor, isotope, triplicate, independentvariable, extractant, ligand)
##########################################  CALCULATED DATA #################################################
def calculate(df_fillmein, aqaliquotfactor, orgaliquotfactor, isotope):
    df_fillmein['AqCPM'] = df_fillmein.AqCPMA
    df_fillmein.AqCPM /= aqaliquotfactor
    df_fillmein['OrgCPM'] = df_fillmein.OrgCPMA
    df_fillmein.OrgCPM /= orgaliquotfactor
    aqueousvalues = df_fillmein.AqCPM.values
    organicvalues = df_fillmein.OrgCPM.values
    extractionpercent = []
    for line in range(0,organicvalues.size):
        extractionpercent.append(organicvalues[line]/(aqueousvalues[line]+organicvalues[line]))
    distributionvalue = []
    for line in range(0,organicvalues.size):
        distributionvalue.append(organicvalues[line]/aqueousvalues[line])
    df_fillmein['Extraction %'] = extractionpercent
    df_fillmein['Distribution Value'] = distributionvalue
    def daughtercalc(df_fillmein, isotope, column):
        df_fillmein['AqDaughterCPM'] = df_fillmein['Aq'+column]
        df_fillmein.AqDaughterCPM /= aqaliquotfactor
        df_fillmein['OrgDaughterCPM'] = df_fillmein['Org'+column]
        df_fillmein.OrgDaughterCPM /= orgaliquotfactor
        aqueousdaughtervalues = df_fillmein.AqDaughterCPM.values
        organicdaughtervalues = df_fillmein.OrgDaughterCPM.values
        daughterextraction = []
        for line in range(0,organicvalues.size):
            daughterextraction.append(organicdaughtervalues[line]/(aqueousdaughtervalues[line]+organicdaughtervalues[line]))
        daughterdistributionvalue = []
        for line in range(0,organicvalues.size):
            daughterdistributionvalue.append(organicdaughtervalues[line]/aqueousdaughtervalues[line])
        df_fillmein['Daughter Extraction %'] = daughterextraction
        df_fillmein['Daughter Distribution Value'] = daughterdistributionvalue
        return (df_fillmein)
    if isotope == 'Bk249':
        column = 'CPMC'
        df_fillmein = daughtercalc(df_fillmein, isotope, column)
    elif isotope == 'Ac227':
        column = 'CPMC'
        df_fillmein = daughtercalc(df_fillmein, isotope, column)
    elif isotope == 'Ce134':
        column = 'CPMB'
        df_fillmein = daughtercalc(df_fillmein, isotope, column)
    df_fillmein.fillna(0)
    # make lists & do the math
    return (df_fillmein)

##########################################  MAKE A QUICK PLOT ###############################################
def quickplot(df_fillmein, triplicate, independentvariable, ligand, extractant, date):
    saveme = input("Should this get added to the total data file? (aka, is this the first time you're running through this data?) (y/n): ")
    if triplicate == 'y':
        number_of_points = int(len(df_fillmein[independentvariable])/3)
        xvalues = df_fillmein[independentvariable].tolist()
        xvalues = xvalues[0:number_of_points]
        yvalues = []
        yerror = []
        for point in range(0,number_of_points):
            value = df_fillmein.loc[(df_fillmein[independentvariable] == xvalues[point]), 'Extraction %'].mean()
            standard_deviation = df_fillmein.loc[(df_fillmein[independentvariable] == xvalues[point]), 'Extraction %'].std()
            yvalues.append(value)
            yerror.append(standard_deviation)
    else:
        yvalues = df_fillmein['Extraction %'].tolist()
        xvalues = df_fillmein[independentvariable].tolist()
        yerror = 0
    def daughterplot(df_fillmein, triplicate, independentvariable, ligand, extractant, date):
        if triplicate == 'y':
            yvalues2 = []
            yerror2 = []
            for point in range(0,number_of_points):
                value2 = df_fillmein.loc[(df_fillmein[independentvariable] == xvalues[point]), 'Daughter Extraction %'].mean()
                standard_deviation2 = df_fillmein.loc[(df_fillmein[independentvariable] == xvalues[point]), 'Daughter Extraction %'].std()
                yvalues2.append(value2)
                yerror2.append(standard_deviation2)
        else:
            yvalues2 = df_fillmein['Daughter Extraction %'].tolist()
            yerror2 = 0
        trace2 = go.Scatter(
            x = xvalues,
            y = yvalues2,
            mode = 'markers',
            name = ligand+' Daughters',
            error_y = dict(
                type = 'data',
                array = yerror2,
                visible = 'True'
                )
            )
        return (df_fillmein, trace2)
    trace = go.Scatter(
        x = xvalues,
        y = yvalues,
        mode = 'markers',
        name = ligand,
        error_y = dict(
            type = 'data',
            array = yerror,
            visible = 'True'
            )
        )
    allthedata.append(trace)
    if isotope == 'Bk249':
        df_fillmein = daughterplot(df_fillmein, isotope)
        allthedata.append(trace2)

    elif isotope == 'Ac227':
        df_fillmein = daughterplot(df_fillmein, isotope)
        allthedata.append(trace2)

    elif isotope == 'Ce134':
        column = 'CPMB'
        df_fillmein = daughterplot(df_fillmein, isotope)
        allthedata.append(trace2)

    layout = go.Layout(
        xaxis = dict(
            type = 'log',
            autorange = True,
            domain = [0,1],
            range = [-4,-2],
            title = independentvariable,
            showgrid = True,
            showline = True,
            exponentformat = 'none',
            #nticks = 5
            tick0 = -4,
            dtick = 1
        ),
        yaxis = dict(
            type = 'linear',
            autorange = False,
            domain = [0,1],
            range = [0,1.1],
            title = 'Extraction Percent',
            showgrid = True,
            showline = True
        ),
        title=str(isotope)+' Extraction into '+str(extractant)+' with varying '+str(independentvariable)
    )
    fig = go.Figure(data=allthedata, layout=layout)
    path = '~\\Desktop\\Berkeley\\AbergelGroup\\Research\\Extractions\\Results\\'
    print (path+'Images/'+date+isotope+'_'+ligand+'_'+extractant+'.png')
    plot = py.offline.plot(fig, image = 'png')
    return (saveme)
##########################################  SAVE EVERYTHING #################################################
def save(df_fillmein, date, isotope, saveme):
     #export the data file as a CSV
    allthedataframe = pd.read_csv(os.path.join('c:\\Users\\Kathy Shield\\Desktop\\Berkeley\\AbergelGroup\\Research\\Extractions\\Results\\ProcessedDataFiles','allthedata.csv'))
    path = '~\\Desktop\\Berkeley\\AbergelGroup\\Research\\Extractions\\Results\\'
    if saveme == 'y':
        allthedataframe = pd.concat([allthedataframe,df_fillmein],ignore_index=True)
        allthedataframe.to_csv(path+'ProcessedDataFiles/allthedata.csv', index=False)
        print ('done!')
    else:
        print ('Okay -- have fun re-running stuff ;)')

    aqueous_ligand = df_fillmein.Ligand[0]
    organic_ligand = df_fillmein.Extractant[0]
    df_fillmein.to_csv(path+'ProcessedDataFiles\\'+date+isotope+'_'+aqueous_ligand+'_'+organic_ligand+'.csv', index=False)
    filename = str(path)+'ProcessedDataFiles\\'+str(date)+str(isotope)+'_'+str(aqueous_ligand)+'_'+str(organic_ligand)+'.csv'
    return (filename)

##########################################  RUN THE ACTUAL CODE #############################################
howmanyfiles = input('How many files are there? ')
allthedata = []
for value in range(int(howmanyfiles)):
        # Filenames are in this format when they come out of splitLSC.sh
    #filename is either ExperTable.csv or Report1.txt
    filename_general = 'ExperTable.csv'
    filename = os.path.join('C:\\Users\\Kathy Shield\\Desktop\\Berkeley\\AbergelGroup\\Research\\Extractions\\RawData\\splitfiles', str(value+1)+'.'+filename_general)


    df_fillmein, df_LSCoutput_aqueous, df_LSCoutput_organic, date = importdata(filename)

    df_fillmein, aqaliquotfactor, orgaliquotfactor, isotope, triplicate, independentvariable, extractant, ligand = parameters (df_fillmein)
    df_fillmein = calculate (df_fillmein, aqaliquotfactor, orgaliquotfactor, isotope)
    allthedataframe.append(df_fillmein)
    saveme = quickplot(df_fillmein, triplicate, independentvariable, ligand, extractant, date)
    filename = save(df_fillmein, date, isotope, saveme)

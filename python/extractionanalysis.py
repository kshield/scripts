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
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt

# And the data.
#
# (Note: the first 6 rows of the data output from the LSC isn't needed; this program does not import it)

# Asks for the number of data files there are.
# This will be the number of skipped vials +1.

def expertableanalysis():
    # Imports the data
    my_data = datasplit = pd.read_csv(filename)

    # Prints the datatable's first column (sample numbers) for referencing sample info
    print(datasplit.ix[:,0])

    # Making the table to get filled with data and export
    datamerge = pd.DataFrame()

    # Separate the data into aqueous and organic tables
    datasplit_aqueous = datasplit[datasplit['S#']%2 ==0]
    datasplit_organic = datasplit[datasplit['S#']%2!=0]

    # Reset the indices so they are the same for each table (row 0 aq = row 0 org)
    datasplit_aqueous.reset_index(drop=True, inplace=True)
    datasplit_organic.reset_index(drop=True, inplace=True)

    # # Determine which variables have changed.
    # pH_varies = input('Does the pH change over the series? (y/n): ')
    # aqueous_concentration_varies = input('Does the aqueous concentration change over the series? (y/n): ')
    # aqueous_ligand_varies = input('Does the aqueous ligand change over the series? (y/n): ')
    # metal_varies = input('Does the metal change over the series? (y/n): ')
    # metal_concentration_varies = input('Does the metal concentration change over the series? (y/n): ')
    # organic_ligand_varies = input('Does the organic ligand change over the series? (y/n): ')
    # organic_concentration_varies = input('Does the organic concentration change over the series? (y/n): ')
    # buffer_varies = input('Does the buffer change over the series? (y/n): ')
    # buffer_concentration_varies = input('Does the buffer concentration change over the series? (y/n): ')

    # For each variable, get the value(s) for the series


    def aqueous_varies():
        # Input
        aqueous_ligand = input('What were the aqueous ligands? (provide ALL CAPS 3-4 letter abbreviations): ')
        datasplit_aqueous['Aq_Ligand'] = aqueous_ligand

    def aqueous_constant():
        # Input
        aqueous_ligand = input('What was the aqueous ligand? ')
        # Fill every row in this newly named column with the inputted value.
        datasplit_aqueous.loc[:,'Aq_Ligand'] = aqueous_ligand

    def aqueous_concentration_varies():
        aqueous_concentrations = input('Please input the aqueous concentrations (mM): ')
        # Convert the string into float values (allows for decimals; necessary for numerical entries)
        aqueous_concentrations = [float(x) for x in aqueous_concentrations.split(',')]
        # Convert the floats into a series of values in pandas.
        aqueous_concentrations = pd.Series(aqueous_concentrations).values
        datasplit_aqueous['Aq_Conc (mM)'] = aqueous_concentrations

    def aqueous_concentration_constant():
        aqueous_concentrations = input('Please input the aqueous concentration (mM): ')
        aqueous_concentrations = float(aqueous_concentrations)
        datasplit_aqueous.loc[:,'Aq_Conc (mM)'] = aqueous_concentrations

    def pH_varies():

    def pH_constant():

    def organic_ligand_varies():
        organic_ligand = input("What were the organic ligands? (Input in ALL CAPS): ")
        datasplit_organic['Org_Ligand'] = organic_ligand

    def organic_ligand_constant():
        organic_ligand = input('What was the organic ligand? ')
        datasplit_organic.loc[:,'Org_Ligand (M)'] = organic_ligand

    def organic_concentration_varies():
        organic_concentrations = input ('Please input the organic concentrations (M): ')
        organic_concentrations = [float(x) for x in organic_concentrations.split(',')]
        organic_concentrations = pd.Series(organic_concentrations).values
        datasplit_organic['Org_Ligand (M)'] = organic_concentrations

# random comment

    def organic_concentration_constant():
        organic_concentrations = input('What was the organic concentration (M)? ')
        datasplit_organic.loc[:,'Org_Conc (M)'] = organic_concentrations

    def metal_varies():
        isotope = input("What were the isotopes? ")
        isotope = pd.Series(isotope).values
        datasplit_aqueous['Isotope'] = isotope
        datasplit_organic['Isotope'] = isotope

    def metal_constant():
        isotope = input('What isotope? ')
        datasplit_aqueous.loc[:,'Isotope'] = isotope

    def buffer_varies():

    def buffer_constant():

    def buffer_concentration_varies():

    def buffer_concentration_constant():

# ONLY ALLOWS FOR ONE VARIABLE PER EXPERIMENT. E.G. YOU CAN CHANGE THE LIGAND
# CONCENTRATION --OR-- THE LIGAND ITSELF, NOT BOTH.
# THIS ENABLES EASIER COMPARATIVE PLOTTING IN THE FUTURE
    for retry in range(3):
        varies = input ('What varies? PICK ONE: aql, aqcon, ph, orgl, orgcon, isotope, buffer, buffercon  > ')
        if varies == 'aql':
            print ('Okay! The aqueous ligand varies.')
            aqueous_varies()
            aqueous_concentration_constant()
            pH_constant()
            organic_ligand_constant()
            organic_concentration_constant()
            metal_constant()
            buffer_constant()
            buffer_concentration_constant()
            break
        elif varies == 'aqcon':
            print('Okay! The concentration of the aqueous ligand varies.')
            aqueous_constant()
            aqueous_concentration_varies()
            pH_constant()
            organic_ligand_constant()
            organic_concentration_constant()
            metal_constant()
            buffer_constant()
            buffer_concentration_constant()
            break
        elif varies == 'pH':
            print ('Okay. The starting pH is changing.')
            aqueous_constant()
            aqueous_concentration_constant()
            pH_varies()
            organic_ligand_constant()
            organic_concentration_constant()
            metal_constant()
            buffer_constant()
            buffer_concentration_constant()
            break
        elif varies == "orgl":
            print ('Okay, the organic ligand varies.')
            aqueous_constant()
            aqueous_concentration_constant()
            pH_constant()
            organic_ligand_varies()
            organic_concentration_constant()
            metal_constant()
            buffer_constant()
            buffer_concentration_constant()
            break
        elif varies == 'orgconc':
            print ('Okay! The concentration of the organic ligand varies.')
            aqueous_constant()
            aqueous_concentration_constant()
            pH_constant()
            organic_ligand_constant()
            organic_concentration_varies()
            metal_constant()
            buffer_constant()
            buffer_concentration_constant()
            break
        elif varies == "isotope":
            print ('Got it. The metal is changing.')
            aqueous_constant()
            aqueous_concentration_constant()
            pH_constant()
            organic_ligand_constant()
            organic_concentration_constant()
            metal_varies()
            buffer_constant()
            buffer_concentration_constant()
            break
        elif varies == 'buffer':
            print ('Sure thing. The buffer is different.')
            aqueous_constant()
            aqueous_concentration_constant()
            pH_constant()
            organic_ligand_constant()
            organic_concentration_constant()
            metal_constant()
            buffer_varies()
            buffer_concentration_constant()
            break
        elif varies == 'buffercon':
            print ('Okie dokes. The buffer concentration changes.')
            aqueous_constant()
            aqueous_concentration_constant()
            pH_constant()
            organic_ligand_constant()
            organic_concentration_constant()
            metal_constant()
            buffer_constant()
            buffer_concentration_varies()
            break
        else:
            print("Error: That isn't one of the accepted inputs.")
    else:
        print("Error: Too many wrong inputs.")


    datamerge["AqCPMA"] = datasplit_aqueous.CPMA
    datamerge["OrgCPMA"] = datasplit_organic.CPMA

    # change the CPM values to adjust to 100 uL volumes (CPMA = CPM/100uL)
    volumeadjust = input('Was the aqueous aliquot 100uL and the organic aliquot 200 uL? (y/n): ')
    if volumeadjust == 'y':
        datasplit_organic.loc[:,'CPMA'] /= 2
    if volumeadjust =='n':
        organicvolume = input('What was the organic aliquot volume? (input in uL with no units): ')
        organicvolume = float(organicvolume)
        datasplit_organic.loc[:,'CPMA'] /= organicvolume/100
        aqueousvolume = input('What was the aqueous aliquot volume? (provide in uL with no units): ')
        aqueousvolume = float(aqueousvolume)
        datasplit_aqueous.loc[:,'CPMA'] /= organicvolume/100
    #

    print(datamerge)
    #
    datasplit_aqueous = datasplit_aqueous.rename({'CPMA':'CPM'},axis='columns')
    datasplit_organic = datasplit_organic.rename({'CPMA':'CPM'},axis='columns')


    # Create two new variables as lists from the CPM values
    organicvalues = datasplit_organic["CPM"].values
    aqueousvalues = datasplit_aqueous["CPM"].values
    # organicvalues.size

    datamerge["AqCPM"] = datasplit_aqueous.CPM
    datamerge["OrgCPM"] = datasplit_organic.CPM

    #
    # Solve for the % extraction
    # (% ext. = org. CPM/(org. CPM + aq CPM))

    extractionpercent=[]
    for line in range(0,organicvalues.size):
        extractionpercent.append(organicvalues[line]/(aqueousvalues[line]+organicvalues[line]))
            #datasplit_organic.loc[organic,"CPMA"]/(datasplit_aqueous.loc[aqueous,"CPMA"]+datasplit_organic.loc[organic,"CPMA"])
    extractionpercent

    datamerge['Ext%'] = extractionpercent
    datamerge['AqS#'] = datasplit_aqueous['S#']
    datamerge['OrgS#'] = datasplit_organic['S#']
    datamerge['Count Time'] = datasplit_organic['Count Time']
    datamerge['DATE'] = datasplit_aqueous.DATE
    datamerge['Isotope'] = datasplit_aqueous.Isotope
    datamerge['AqL'] = datasplit_aqueous.Aq_Ligand
    datamerge['AqLConc (mM)'] = datasplit_aqueous['Aq_Conc (mM)']
    datamerge['OrgL'] = datasplit_organic.Org_Ligand
    datamerge['OrgLConc (M)'] = datasplit_organic['Org_Conc (M)']
    #
    #
    # # ### Time to plot this
    #
    date = datetime.datetime.strptime(datamerge.loc[0,'DATE'],'%m/%d/%Y').strftime('%Y%m%d')
    #
    print(datamerge)
    #

    #plt.plot(aqueous_concentrations,extractionpercent,'bo')
    # plt.xscale('log')
    # plt.title('HDEHP Extracts Gd Down to 2.5 mM')
    # plt.xlabel('HDEHP Concentration (M)')
    # plt.ylabel('% Extraction')
    # plt.grid(True)
    #plt.savefig(date+isotope+'_'+aqueous_ligand+'_'+organic_ligand+'.png')
    # plt.show()
    #export the data file as a CSV
    datamerge.to_csv(date+isotope+'_'+aqueous_ligand+'_'+organic_ligand+'.csv')


howmanyfiles = input('How many files are there? ')

# If there is only one file, use filename = "ExperTable.csv"
if howmanyfiles == '1':
    filename = 'ExperTable.csv'
    print(filename)
    expertableanalysis()

# If there is more than one file, first use splitLSC.sh to split properly.
# Everything else is a loop through all the files.
else:
    for value in range(int(howmanyfiles)):
        # Filenames are in this format when they come out of splitLSC.sh
        filename = str(value+1)+'.ExperTable.csv'
        print (filename)
        expertableanalysis()
        print(value)

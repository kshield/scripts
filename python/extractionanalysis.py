#!/c/Users/Public/python

# -*- coding: utf-8 -*-
#"""
#Created on Tue May  8 13:40:20 2018

#@author: Kathy Shield
#"""


# coding: utf-8

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
howmanyfiles = input('How many files are there?')

# If there is only one file, use filename = "ExperTable.csv"
if howmanyfiles == '1':
    print('quit now')
    filename = 'ExperTable.csv'
    print(filename)
    my_data = datasplit = pd.read_csv(filename)
    print(datasplit.ix[:,0])
# If there is more than one file, first use splitLSC.py to split properly.
# Everything else is a loop through all the files.
else:
    for value in range(int(howmanyfiles)):
        filename = str(value+1)+'.ExperTable.csv'
        print (filename)
        # Filenames are in this format when
        my_data = datasplit = pd.read_csv(filename)

        # Prints the datatable's first column (sample numbers) for referencing sample info
        print(datasplit.ix[:,0])
        
        # The exported data is always called 'ExperTable.csv'

        # Making the Table for csv Export
        datamerge = pd.DataFrame()


        # Separate the data into aqueous and organic tables
        datasplit_aqueous = datasplit[datasplit['S#']%2 ==0]
        datasplit_organic = datasplit[datasplit['S#']%2!=0]

        datasplit_aqueous.reset_index(drop=True, inplace=True)
        datasplit_organic.reset_index(drop=True, inplace=True)

         # The aq. concentrations will need to be inputted at the start of the program

        aqueous_concentrations = input('Please input the aqeous concentrations (mM): ')
        aqueous_concentrations = [int(x) for x in aqueous_concentrations.split(',')]
        aqueous_concentrations = pd.Series(aqueous_concentrations).values
        print (aqueous_concentrations)


        # Add other information to the appropriate tables (to make future data analysis super easy) including:
        # # - the isotope
        # # - the aq. ligand & concentration
        # # - the org. ligand & concentration
        #
         #isotope
        isotope = input('What isotope?')
        datasplit_aqueous.loc[:,'Isotope'] = isotope
        print(datasplit_aqueous)
        #
        #ligands
        aqueous_ligand = input('What was the aqueous ligand?')
        organic_ligand = input('What was the organic ligand?')
        datasplit_aqueous.loc[:,'Aq_Ligand'] = aqueous_ligand
        datasplit_organic.loc[:,'Org_Ligand'] = organic_ligand
        #
        #Concentrations
        organic_concentration = input('What was the organic concentration (M)?')
        datasplit_organic.loc[:,'Org_Conc (M)'] = organic_concentration
        #
        datasplit_aqueous['Aq_Conc (mM)'] = aqueous_concentrations
        #
        print(datasplit_aqueous)
        print(datasplit_organic)

        datamerge["AqCPMA"] = datasplit_aqueous.CPMA
        datamerge["OrgCPMA"] = datasplit_organic.CPMA
        #
        # change the CPM values to adjust to 100 uL volumes (CPMA = CPM/100uL)
        # datasplit_aqueous.loc[:,'CPMA'] /= 1
        datasplit_organic.loc[:,'CPMA'] /= 2
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

        # plt.plot(aqueous_concentrations,extractionpercent,'bo')
        # plt.xscale('log')
        # plt.title('HDEHP Extracts Gd Down to 2.5 mM')
        # plt.xlabel('HDEHP Concentration (M)')
        # plt.ylabel('% Extraction')
        # plt.grid(True)
        # plt.savefig(date+isotope+'_'+aqueous_ligand+'_'+organic_ligand+'.png')
        # plt.show()
        #export the data file as a CSV
        datamerge.to_csv(date+isotope+'_'+aqueous_ligand+'_'+organic_ligand+'.csv')

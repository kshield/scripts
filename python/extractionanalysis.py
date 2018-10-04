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

    allthedataframe = pd.read_csv(os.path.join('c:\\Users\\Kathy Shield\\Desktop\\Berkeley\\AbergelGroup\\Research\\Extractions\\Results\\ProcessedDataFiles','allthedata.csv'))
    # Separate the data into aqueous and organic tables
    datamerge.reset_index(drop=True, inplace=True)

    datasplit_aqueous = datasplit.iloc[::2]
    datasplit_organic = datasplit.iloc[1::2]

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
        aqueous_ligand = input('What were the aqueous ligands? (provide ALL CAPS 3-4 letter abbreviations, comma separated): ')
        datasplit_aqueous['Aq_Ligand'] = aqueous_ligand

    def aqueous_constant():
        # Input
        aqueous_ligand = input('What was the aqueous ligand? ')
        #    if aqueous_ligand = 'none':
        #        datasplit_aqueous.loc[:,'Aq_Conc (mM)'] = 0
        #        break
        # Fill every row in this newly named column with the inputted value.
        datasplit_aqueous.loc[:,'Aq_Ligand'] = aqueous_ligand
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
        datasplit_aqueous['Aq_Conc (mM)'] = aqueous_concentrations
        return (triplicate)

    def aqueous_concentration_constant():
        aqueous_concentrations = input('Please input the aqueous concentration (mM): ')
        aqueous_concentrations = float(aqueous_concentrations)
        datasplit_aqueous.loc[:,'Aq_Conc (mM)'] = aqueous_concentrations

    def pH_varies():
        ph = input('What were the starting pH values? (Input as comma separated numbers): ')
        ph = [float(x) for x in ph.split(',')]
        ph = pd.Series(ph).values
        datasplit_aqueous['pH'] = ph

    def pH_constant():
        ph = input('What was the starting pH? ')
        datasplit_aqueous['pH'] = ph

    def organic_ligand_varies():
        organic_ligand = input("What were the organic extractants? (Input in ALL CAPS, comma separated): ")
        datasplit_organic['Org_Ligand'] = organic_ligand

    def organic_ligand_constant():
        organic_ligand = input('What was the organic extractant? (Input in ALL CAPS): ')
        datasplit_organic.loc[:,'Org_Ligand'] = organic_ligand

    def organic_concentration_varies():
        organic_concentrations = input ('Please input the organic concentrations (M): ')
        organic_concentrations = [float(x) for x in organic_concentrations.split(',')]
        organic_concentrations = pd.Series(organic_concentrations).values
        datasplit_organic['Org_Conc (M)'] = organic_concentrations

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
        buffer = input("What were the buffers? (Input comma separated): ")
        datasplit_aqueous['Buffer'] = buffer


    def buffer_constant():
        buffer = input('What was the buffer? ')
        datasplit_aqueous.loc[:,'Buffer'] = buffer

    def buffer_concentration_varies():
        buffer_concentrations = input ('Please input the buffer concentrations (mM): ')
        buffer_concentrations = [float(x) for x in buffer_concentrations.split(',')]
        buffer_concentrations = pd.Series(buffer_concentrations).values
        datasplit_aqueous['Buffer (mM)'] = buffer_concentrations

    def buffer_concentration_constant():
        buffer_concentrations = input('What was the buffer concentration (mM)? ')
        datasplit_aqueous.loc[:,'Buffer (mM)'] = buffer_concentrations

# ONLY ALLOWS FOR ONE VARIABLE PER EXPERIMENT. E.G. YOU CAN CHANGE THE LIGAND
# CONCENTRATION --OR-- THE LIGAND ITSELF, NOT BOTH.
# THIS ENABLES EASIER COMPARATIVE PLOTTING IN THE FUTURE
    varies = input ('What varies? PICK ONE: aql, aqconc, ph, orgl, orgconc, isotope, buffer, bufferconc  > ')
    for retry in range(3):
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
            ligandtype = input('What class of Ligands were used? (Carboxylic Acids, HOPO Derivatives): ')
            independentvariabletitle = 'Varying '+ligandtype
            break
        elif varies == 'aqconc':
            print('Okay! The concentration of the aqueous ligand varies.')
            aqueous_ligand = aqueous_constant()
            triplicate = aqueous_concentration_varies()
            pH_constant()
            organic_ligand_constant()
            organic_concentration_constant()
            metal_constant()
            buffer_constant()
            buffer_concentration_constant()
            independentvariabletitle = aqueous_ligand
            break
        elif varies == 'ph':
            print ('Okay. The starting pH is changing.')
            aqueous_constant()
            aqueous_concentration_constant()
            pH_varies()
            organic_ligand_constant()
            organic_concentration_constant()
            metal_constant()
            buffer_constant()
            buffer_concentration_constant()
            independentvariabletitle = 'Varying Initial pH'
            break
        elif varies == "orgl":
            print ('Okay, the organic ligand varies.')
            aqueous_ligand = aqueous_constant()
            aqueous_concentration_constant()
            pH_constant()
            organic_ligand_varies()
            organic_concentration_constant()
            metal_constant()
            buffer_constant()
            buffer_concentration_constant()
            independentvariabletitle = aqueous_ligand
            break
        elif varies == 'orgconc':
            print ('Okay! The concentration of the organic ligand varies.')
            aqueous_constant()
            aqueous_concentration_constant()
            pH_constant()
            organic_ligand = organic_ligand_constant()
            organic_concentration_varies()
            metal_constant()
            buffer_constant()
            buffer_concentration_constant()
            independentvariabletitle = organic_ligand
            break
        elif varies == "isotope":
            print ('Got it. The metal is changing.')
            aqueous_ligand = aqueous_constant()
            aqueous_concentration_constant()
            pH_constant()
            organic_ligand_constant()
            organic_concentration_constant()
            metal_varies()
            buffer_constant()
            buffer_concentration_constant()
            independentvariabletitle = aqueous_ligand
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
            independentvariabletitle = 'Various Buffers'
            break
        elif varies == 'bufferconc':
            print ('Okie dokes. The buffer concentration changes.')
            aqueous_constant()
            aqueous_concentration_constant()
            pH_constant()
            organic_ligand_constant()
            organic_concentration_constant()
            metal_constant()
            buffer = buffer_constant()
            buffer_concentration_varies()
            independentvariabletitle = buffer
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
    print(datamerge)
    datasplit_aqueous = datasplit_aqueous.rename({'CPMA':'CPM'},axis='columns')
    datasplit_organic = datasplit_organic.rename({'CPMA':'CPM'},axis='columns')
    # Create two new variables as lists from the CPM values
    organicvalues = datasplit_organic["CPM"].values
    aqueousvalues = datasplit_aqueous["CPM"].values
    datamerge["AqCPM"] = datasplit_aqueous.CPM
    datamerge["OrgCPM"] = datasplit_organic.CPM
    #
    # Solve for the % extraction
    # (% ext. = org. CPM/(org. CPM + aq CPM))
    extractionpercent=[]
    for line in range(0,organicvalues.size):
        extractionpercent.append(organicvalues[line]/(aqueousvalues[line]+organicvalues[line]))
    datamerge['Extraction %'] = extractionpercent
    datamerge['Isotope'] = datasplit_aqueous.Isotope
    datamerge['Ligand'] = datasplit_aqueous.Aq_Ligand
    datamerge['Ligand Concentration (mM)'] = datasplit_aqueous['Aq_Conc (mM)']
    datamerge['Extractant'] = datasplit_organic.Org_Ligand
    datamerge['Extractant Concentration (M)'] = datasplit_organic['Org_Conc (M)']
    datamerge['Buffer'] = datasplit_aqueous.Buffer
    datamerge['Buffer Concentration (mM)'] = datasplit_aqueous['Buffer (mM)']
    datamerge['Initial pH'] = datasplit_aqueous.pH
    datamerge['Aqueous LSC Vial'] = datasplit_aqueous['S#']
    datamerge['Organic LSC Vial'] = datasplit_organic['S#']
    datamerge['Count Time'] = datasplit_organic['Count Time']
    datamerge['Date'] = datasplit_aqueous.DATE
    date = datetime.datetime.strptime(datamerge.loc[0,'Date'],'%m/%d/%Y').strftime('%Y%m%d')
    print(datamerge)
    #plt.plot(aqueous_concentrations,extractionpercent,'bo')
    # plt.xscale('log')
    # plt.title('HDEHP Extracts Gd Down to 2.5 mM')
    # plt.xlabel('HDEHP Concentration (M)')
    # plt.ylabel('% Extraction')
    # plt.grid(True)
    #plt.savefig(date+isotope+'_'+aqueous_ligand+'_'+organic_ligand+'.png')
    # plt.show()
    #export the data file as a CSV
    isotope = datamerge.Isotope.ix[0]
    aqueous_ligand = datamerge.Ligand[0]
    organic_ligand = datamerge.Extractant[0]
    path = '~/Desktop/Berkeley/AbergelGroup/Research/Extractions/Results/'
    datamerge.to_csv(path+'ProcessedDataFiles/'+date+isotope+'_'+aqueous_ligand+'_'+organic_ligand+'.csv', index=False)
    filename_datamerge = str(path)+'ProcessedDataFiles/'+str(date)+str(isotope)+'_'+str(aqueous_ligand)+'_'+str(organic_ligand)+'.csv'

    if input("Should this get added to the total data file? (aka, is this the first time you're running through this data?) (y/n): ") == 'y':
        allthedataframe = pd.concat([allthedataframe,datamerge],ignore_index=True)
        allthedataframe.to_csv(path+'ProcessedDataFiles/allthedata.csv', index=False)
        print ('done!')
    else:
        print ('Okay -- have fun re-running stuff ;)')

    if varies == 'aql':
        independentvariable = 'Ligand'

    elif varies == 'aqconc':
        independentvariable = 'Ligand Concentration (mM)'
    elif varies == 'ph':
        independentvariable = 'Initial pH'
    elif varies == 'orgl':
        independentvariable = 'Extractant'

    elif varies == 'orgconc':
        independentvariable = 'Extractant Concentration (M)'

    elif varies == 'isotope':
        independentvariable = 'Isotope'

    elif varies == 'buffer':
        independentvariable = 'Buffer'

    elif varies == 'bufferconc':
        independentvariable = 'Buffer Concentration (mM)'


    datan = pd.read_csv(filename_datamerge)
    if triplicate == 'y':
        number_of_points = int(len(datan[independentvariable])/3)
        xvalues = datan[independentvariable].tolist()
        xvalues = xvalues[0:number_of_points]
        yvalues = []
        yerror = []
        for point in range(0,number_of_points):
            value = datan.loc[(datan[independentvariable] == xvalues[point]), 'Extraction %'].mean()
            standard_deviation = datan.loc[(datan[independentvariable] == xvalues[point]), 'Extraction %'].std()
            yvalues.append(value)
            yerror.append(standard_deviation)
    else:
        yvalues = datan['Extraction %'].tolist()
        xvalues = datan[independentvariable].tolist()
        yerror = 0
    trace = go.Scatter(
        x = xvalues,
        y = yvalues,
        mode = 'markers',
        name = aqueous_ligand,
        error_y = dict(
            type = 'data',
            array = yerror,
            visible = 'True'
            )
        )
    allthedata.append(trace)

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
        title=str(isotope)+' Extraction into '+str(organic_ligand)+' with varying '+str(independentvariable)
    )
    fig = go.Figure(data=allthedata, layout=layout)
    print (path+'Images/'+date+isotope+'_'+aqueous_ligand+'_'+organic_ligand+'.png')
    plot = py.offline.plot(fig, image = 'png')
    time.sleep(1)
    #py.image.save_as(plot, path+date+isotope+'_'+aqueous_ligand+'_'+organic_ligand)
    programfilename = os.path.join('C:/Users/Kathy Shield/Desktop','plot_image.png').replace('\\','/')
    print (programfilename)
    newfilename = os.path.join('C:/Users/Kathy Shield/Desktop/Berkeley/AbergelGroup/Research/Extractions/Results/Images',date+isotope+'_'+aqueous_ligand+'_'+organic_ligand+'.png').replace('\\','/')
    print (newfilename)
    os.rename(programfilename, newfilename)
    if os.path.exists(programfilename):
        os.remove(programfilename)
    print ('file removed')

#We really start here...
howmanyfiles = input('How many files are there? ')
allthedata = []
for value in range(int(howmanyfiles)):
        # Filenames are in this format when they come out of splitLSC.sh
    #filename is either ExperTable.csv or Report1.txt
    filename_general = input('What is the core file name? (Likely either ExperTable.csv or Report1.txt): ')
    filename = os.path.join('C:\\Users\\Kathy Shield\\Desktop\\Berkeley\\AbergelGroup\\Research\\Extractions\\RawData\\splitfiles', str(value+1)+'.'+filename_general)
    expertableanalysis()

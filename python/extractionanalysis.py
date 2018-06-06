# -*- coding: utf-8 -*-
"""
Created on Tue May  8 13:40:20 2018

@author: Kathy Shield
"""


# coding: utf-8

# First, import the things you need.

# This includes packages

# In[55]:


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

# In[2]:


#####        import data file (csv)
my_data = datasplit = pd.read_csv('1.ExperTable.csv', ',')


# The exported data is always called 'ExperTable.csv'

# Making the Table for csv Export

# In[3]:


datamerge = pd.DataFrame()


# Separate the data into aqueous and organic tables

# In[4]:


datasplit_aqueous = datasplit[datasplit['S#']%2 ==0]
datasplit_organic = datasplit[datasplit['S#']%2!=0]
datasplit_organic = datasplit_organic.drop([0])
datasplit_background = datasplit.iloc[0,:]


# In[5]:


datasplit_aqueous.reset_index(drop=True, inplace=True)
datasplit_organic.reset_index(drop=True, inplace=True)


# The aq. concentrations will need to be inputted at the start of the program

# In[6]:


aqueous_concentrations = [0,0,0]
aqueous_concentrations = pd.Series(aqueous_concentrations)


# Add other information to the appropriate tables (to make future data analysis super easy) including:
# - the isotope
# - the aq. ligand & concentration
# - the org. ligand & concentration

# In[37]:


#isotope
Isotope = datasplit_aqueous.loc[:,'Isotope'] = 'Gd153'

#ligands
AqL= datasplit_aqueous.loc[:,'Aq_Ligand'] = 'DTPA'
OrgL= datasplit_organic.loc[:,'Org_Ligand'] = 'HDEHP'

#Concentrations
datasplit_organic.loc[:,'Org_Conc (M)'] = 0.1

datasplit_aqueous['Aq_Conc (mM)'] = aqueous_concentrations.values


# In[8]:


datamerge["AqCPMA"] = datasplit_aqueous.CPMA
datamerge["OrgCPMA"] = datasplit_organic.CPMA


# Change the CPMA column to CPM & rename as such
# (assumes 6 minute count (as is in the actinide LSC program), 2 organic aliquots and 1 aqueous aliquot)

# In[10]:


# accurate CPM counts
datasplit_aqueous.loc[:,'CPMA'] /= 6
datasplit_organic.loc[:,'CPMA'] /= 12


# In[11]:


datasplit_aqueous = datasplit_aqueous.rename({'CPMA':'CPM'},axis='columns')
datasplit_organic = datasplit_organic.rename({'CPMA':'CPM'},axis='columns')


# Create two new variables as lists from the CPM values

# In[12]:


organicvalues = datasplit_organic["CPM"].values
aqueousvalues = datasplit_aqueous["CPM"].values
organicvalues.size

# In[13]:


datamerge["AqCPM"] = datasplit_aqueous.CPM
datamerge["OrgCPM"] = datasplit_organic.CPM


# Solve for the % extraction
# (% ext. = org. CPM/(org. CPM + aq CPM))

# In[15]:


extractionpercent=[]
for line in range(0,organicvalues.size):
    extractionpercent.append(organicvalues[line]/(aqueousvalues[line]+organicvalues[line]))
        #datasplit_organic.loc[organic,"CPMA"]/(datasplit_aqueous.loc[aqueous,"CPMA"]+datasplit_organic.loc[organic,"CPMA"])
extractionpercent


# In[16]:


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


# ### Time to plot this

# In[44]:


date = datetime.datetime.strptime(datamerge.loc[0,'DATE'],'%m/%d/%Y').strftime('%Y%m%d')


# In[54]:


plt.plot(aqueous_concentrations,extractionpercent,'bo')
plt.xscale('log')
plt.title('HDEHP Extracts Gd Down to 2.5 mM')
plt.xlabel('HDEHP Concentration (M)')
plt.ylabel('% Extraction')
plt.grid(True)
plt.savefig(date+Isotope+'_'+AqL+'_'+OrgL+'.png')
plt.show()


# In[43]:


datamerge.to_csv(date+Isotope+'_'+AqL+'_'+OrgL+'.csv')

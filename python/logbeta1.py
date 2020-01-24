#!/c/Users/Public/python

import os
import pandas as pd
import numpy as np
import datetime
import warnings
warnings.filterwarnings("ignore")
import csv

#  input the pKa values for your ligands

#  input the pH of the experiment

#  based on the pH and pKa's,
#  determine how deprotonated the ligand is expected to be
###  pKa is, by definition, the pH at which 50% of that proton is protonated
###  more acidic (lower pH) means more free H+, which means more of the
###  ligand will be protonated.
###  Extremely acidic systems, therefore, should start with fully protonated
###  ligands, while they should be fully deprotonated at extremely basic pH

##  HySS can be used to determine the primary species (singular or multiple)
##  at any single pH. This can be done easily if the log betas of the ligand
##  are known.

###  Nathan Bessen (Colorado School of Mines) assumed 5 deprotonations (DTPA)
###  --> fully deprotonated ligand
###  Working at pH ~4.2, nearly none of the ligand is fully deprotonated
###  --> tracks with his spreadsheet, which has values of E-11 for the conc.
###  Rather, ~70% is DTPAH_3^{2-}

###  SO WHY DOES HE STILL CONSIDER ONLY THE FULLY DEPROTONATED LIGAND?

###  Actual log beta calculation is from (D0/D)-1 (y) and [DTPAH_3^{2-}] (x),
###  where log_beta = log[slope] of that ^

###  DIFFERENCES BETWEEN NATHANS DATA AND MINE
###   - direction of (D0/D)-1 slope -- Nathan's has positive slope while mine
###     have negative slopes
###   - D0 - calculated from Kex, extractant concentration, and some weird eq
###     vs. observed. 



                                             (N4*O4*P4*Q4*R4*S4)
------------------------------------------------------------------------------------------------------------------
((T10^6)+(T10^5*N4)+(T10^4*N4*O4)+(T10^3*N4*O4*P4)+(T10^2*N4*O4*P4*Q4)+(T10*N4*O4*P4*Q4*R4)+(N4*O4*P4*Q4*R4*S4))

T10 = proton_concentration
N4 = 10^-pKa1
O4 = 10^-pKa2
P4 = 10^-pKa3
Q4 = 10^-pKa4
R4 = 10^-pKa5
S4 = 10^-pKa6
# where pKa6 is the last proton to be deprotonated (that with the highest/most basic pKa)

## Questions about Nathan's spreadsheet:
# 1. Why/how are there six pKa's for DTPA - DTPA only has 5 carboxylic acids?
# 1b. Unless you consider the three amino groups on the backbone, in which case
#     there should be 8 pKa's.
# 2. Why do you have the same value labeled in one place as [L5-] and in another
#    place as L2- (presumably LH_3^{2-}, which makes sense given the
#    experimental pH.)
# 3. Why is the L5- / L2- concentration calculated with all six pKa's?

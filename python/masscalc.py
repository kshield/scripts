#!/usr/bin/env python
"""
--------------------------------------------------------------------------------
(c) 2017 Julian Rees

License: GNU GPLv3

Description: Calculate mass from moles and FW

Run: python molcalc.py

Dependencies: numpy
--------------------------------------------------------------------------------
"""
import sys
import math
import subprocess
import numpy as np

subprocess.check_call('clear')
print(__doc__)

print("""         MASS CALCULATOR

------- !!! IMPORTANT !!! -------
 DON'T LOOSE TRACK OF YOUR UNITS!
---------------------------------

""")
fw = raw_input('formula weight of compound: ')
try:
    fw = float(fw)
except ValueError:
    sys.exit("You must input a number!")

mols = raw_input('millimoles of compound: ')
try:
    mols = float(mols)/1000
except ValueError:
    sys.exit("You must input a number!")

mass = mols * fw

if np.round_(mass, decimals = 4) > 0.1:
    mass = str(np.round_(mass, decimals = 4))
elif np.round_(mass*1000, decimals = 3) > 0.1:
    mass = str(np.round_(mass*1000, decimals = 3)) + ' x10^-3'
else:
    mass = str(np.round_(mass*1000000, decimals = 3)) + ' x10^-6'

print('\n' + mass + ' g \n')

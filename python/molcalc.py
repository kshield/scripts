#!/usr/bin/env python
"""
--------------------------------------------------------------------------------
(c) 2017 Julian Rees

License: GNU GPLv3

Description: Calculate moles from mass and FW

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

print("""         MOLE CALCULATOR

------- !!! IMPORTANT !!! -------
 DON'T LOOSE TRACK OF YOUR UNITS!
---------------------------------

""")
fw = raw_input('formula weight of compound: ')
try:
    fw = float(fw)
except ValueError:
    sys.exit("You must input a number!")

mass = raw_input('mass of compound: ')
try:
    mass = float(mass)
except ValueError:
    sys.exit("You must input a number!")

mol = mass / fw

if np.round_(mol, decimals = 4) > 0.1:
    mol = str(np.round_(mol, decimals = 4))
elif np.round_(mol*1000, decimals = 3) > 0.1:
    mol = str(np.round_(mol*1000, decimals = 3)) + ' x10^-3'
else:
    mol = str(np.round_(mol*1000000, decimals = 3)) + ' x10^-6'

print('\n' + mol + ' mols \n')

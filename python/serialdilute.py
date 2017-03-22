#!/usr/bin/env python
"""
--------------------------------------------------------------------------------
(c) 2017 Julian Rees

License: GNU GPLv3

Description: Calculate a serial dilution

Run: python serialdilute.py

Dependencies: numpy
--------------------------------------------------------------------------------
"""
import sys
import math
import subprocess
import numpy as np

subprocess.check_call('clear')
print(__doc__)

print("""    SERIAL DILUTION CALCULATOR

------- !!! IMPORTANT !!! -------
 DON'T LOOSE TRACK OF YOUR UNITS!
---------------------------------

""")

ndilutes = raw_input('number of dilutions: ')
try:
    ndilutes = int(ndilutes)
except ValueError:
    sys.exit("You must input an integer!")

stock = raw_input('concentration of stock solution: ')
try:
    m1 = float(stock)
except ValueError:
    sys.exit("You must input a number!")

preload = raw_input('volume of pre-loaded solution: ')
try:
    pre = float(preload)
except ValueError:
    sys.exit("You must input a number!")

aliq = raw_input('volume of stock solution in first dilution: ')
try:
    v1 = float(aliq)
except ValueError:
    sys.exit("You must input a number!")

pipette = raw_input('volume of solution to transfer in dilution: ')
try:
    xfer = float(pipette)
except ValueError:
    sys.exit("You must input a number!")

topoff = raw_input('volume of reagent to add after dilution: ')
try:
    top = float(topoff)
except ValueError:
    sys.exit("You must input a number!")

v2 = v1 + pre

concs = []
concs.append((m1*v1)/v2)

v2 = xfer + pre

for i in range(1,ndilutes):
    concs.append((concs[i-1]*xfer)/v2)

if top != 0:
    concs = np.divide(np.multiply(concs, pre), (pre + top))

for i in range(0,ndilutes):
    if np.round_(concs[i], decimals = 4) > 0.01:
        concs[i] = np.round_(concs[i], decimals = 4)
    else:
        concs[i] = str(np.round_(concs[i]*1000, decimals = 3)) + ' x10^-3'

print(str(ndilutes) + ' dilutions of your stock solution [ ] = ' + stock + ' will be calculated.\n')

for i in range(0,ndilutes):
    print(concs[i])

print('\n')

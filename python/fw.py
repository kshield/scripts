#!/usr/bin/env python3
"""
--------------------------------------------------------------------------------
(c) 2017 Julian Rees

License: GNU GPLv3

Description: Calculate mass from moles and FW

Run: python molcalc.py

Dependencies: numpy, periodictable
--------------------------------------------------------------------------------
"""
import sys
import math
import subprocess
import numpy as np
import periodictable as pt

subprocess.check_call('clear')
print(__doc__)

print("""
------- !!! FW CALCULATOR !!! -------
-------------------------------------

""")

from periodictable import *

# open filename
totalmass = 0
fname = str(sys.argv[1])
with open(fname) as f:

# search lines for element counts, skipping first line
    for line in f:
         arg = "pt." + line[0] + ".mass"
#         print(line[2])
         mass = eval(arg) * int(line[2])
         totalmass = totalmass + mass
print(totalmass)

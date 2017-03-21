#!/usr/bin/env python
"""
--------------------------------------------------------------------------------
(c) 2017 Julian Rees

License: GNU GPLv3

Description: Plot the energy trajectory of a geometry optimization in ORCA.

Run: python geomenergymap.py filename

Arguments: filename - file name with extension

Dependencies: matplotlib
--------------------------------------------------------------------------------
"""
print(__doc__)
import sys
import math
import matplotlib.pyplot as plt

# check for correct number of inputs
if len(sys.argv) != 2:
    sys.exit("You must supply exactly one filename!")

# define search string and clear the list
searchfor = "SUCCESS "
searchfor1 = "SCF NOT CONVERGED"
searchfor2 = "FINAL SINGLE POINT ENERGY"
cycles = []
energies = []

# open filename
fname = str(sys.argv[1])
with open(fname) as f:

# search lines for string and move down two lines to get energy
    for line in f:
        if searchfor in line:
            line = f.next()
            cycle = int(line.split()[4])
            cycles.append(cycle)
	elif searchfor1 in line:
	    cycle = 125
	    cycles.append(cycle)
        elif searchfor2 in line:
            energy = float(line.split()[4])
            energies.append(energy)

# plot cycles and energies
plt.plot(cycles, 'o-')
plt.title('%d Geometry Iterations' %len(cycles))
plt.xlabel('Geometry Iteration')
plt.ylabel('SCF Cycles')
plt.show()

plt.plot(energies, 'o-')
plt.title('%d Geometry Iterations' %len(cycles))
plt.xlabel('Geometry Iteration')
plt.ylabel('Final SP Energies')
plt.show()

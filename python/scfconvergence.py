#!/usr/bin/python
# shortcut "nel", return alpha and beta HOMO numbers and spin for ORCA output files

import sys
import math
import matplotlib.pyplot as plt

# check for correct number of inputs
if len(sys.argv) != 2:
    sys.exit("You must supply exactly one filename!")

# define search string and clear the list
searchfor = "SCF ITERATIONS"
energies = []

# open filename
fname = str(sys.argv[1])
with open(fname) as f:

# search lines for string and move down two lines to get energy
    i = 0
    for line in f:
        if searchfor in line:
            next(f)
            line = f.next()
            # run a loop over the first SCF convergence
            while "SUCCESS" not in line:
                if not line.strip():
                    break
                # check to see if the line is an iteration
                elif line.split()[0].isdigit():
                    # get the energy as a number and add it to the list
                    energy = float(line.split()[1])
                    energies.append(energy)
                line = f.next()
            break

# plot energies
plt.plot(energies,'o-')
plt.title('%d SCF Iterations' %len(energies))
plt.xlabel('SCF Iteration')
plt.ylabel('SCF Energy')
plt.show()

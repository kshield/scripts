#!/usr/bin/python
# shortcut "nel", return alpha and beta HOMO numbers and spin for ORCA output files

import sys
import math
import matplotlib.pyplot as plt

# check for correct number of inputs
if len(sys.argv) < 2:
    sys.exit("You must supply exactly one filename!")
elif len(sys.argv) == 2:
    print('- - !! ONLY THE FIRST SCF WILL BE PRINTED !! - -')
elif len(sys.argv) > 3:
    sys.exit('You must supply exactly one filename and an optional SCF number!')
elif sys.argv[2].isdigit() == False:
    sys.exit('You must supply exactly one filename and an optional SCF number!')

# define search string and clear the list
searchfor = "SCF ITERATIONS"
energies = []
delta_energies = []

# optionally assign the SCF to print
if len(sys.argv) == 3:
    scfnum = int(sys.argv[2])
else:
    scfnum = 1

# open filename
fname = str(sys.argv[1])
with open(fname) as f:

# search lines for string and move down two lines to get energy
    i = 1
    for line in f:
        if searchfor in line:
            next(f)
            try:
                line = f.next()
            except:
                print(' ')
                sys.exit('- - !! REACHED THE END OF THE OUTPUT FILE !! - -')
            # check if i = scfnum
            if i < scfnum:
                i = i + 1
            else:
                # run a loop over the first SCF convergence
                while "SUCCESS" not in line:
                    if not line.strip():
                        break
                    # check to see if the line is an iteration
                    elif line.split()[0].isdigit():
                        # get the energy as a number and add it to the list
                        energy = float(line.split()[1])
                        energies.append(energy)
                        delta_energies.append(float(line.split()[2]))
                    try:
                        line = f.next()
                    except:
                        print(' ')
                        print('- - !! THE SCF IS NOT YET CONVERGED !! - -')
                        break
                break

# plot energies
plt.plot(energies,'o-')
plt.title('%d SCF Iterations' %len(energies))
plt.xlabel('SCF Iteration')
plt.ylabel('SCF Energy')
plt.show()
plt.plot(delta_energies,'o-')
plt.title('%d SCF Iterations' %len(delta_energies))
plt.xlabel('SCF Iteration')
plt.ylabel('SCF Energy')
plt.show()

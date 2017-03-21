#!/usr/bin/env python
"""
--------------------------------------------------------------------------------
(c) 2017 Julian Rees

License: GNU GPLv3

Description: Plot the performance of the SCF convergence in ORCA.

Run: python scfconvergence.py filename [scfnum skip]

Arguments: filename - file name with extension;
                      there should be at least one SCF cycle present
           scfnum   - optional: if more than one SCF cycle (e.g. a geometry
                      optimization), the desired cycle to plot
           skip     - optional: SCF iterations to truncate from start;
                      to better visualize late-stage convergence

Dependencies: matplotlib
--------------------------------------------------------------------------------
"""
print(__doc__)
import sys
import math
import matplotlib.pyplot as plt

# check for correct number of inputs
if len(sys.argv) < 2:
    print(' ')
    sys.exit("You must supply exactly one filename!")
elif len(sys.argv) == 2:
    print(' ')
    print('- - !! ONLY THE FIRST SCF WILL BE PRINTED !! - -')
elif (len(sys.argv) == 3 and sys.argv[2].isdigit() == True):
    pass
elif (len(sys.argv) == 4 and sys.argv[2].isdigit() == True and
    sys.argv[3][1].isdigit() == True and sys.argv[3][0] is '-'):
    pass
else:
    print(' ')
    str1 = 'You must supply exactly one filename, '
    str2 = 'and an optional SCF number and pre-cutoff (negative)!'
    sys.exit(str1 + str2)

# define search string and clear the list
searchfor = "SCF ITERATIONS"
energies = []
delta_energies = []

# optionally assign the SCF to print
if len(sys.argv) == 3:
    scfnum = int(sys.argv[2])
    skip = 0
elif len(sys.argv) == 4:
    scfnum = int(sys.argv[2])
    skip = int(float(sys.argv[3])*-1)
else:
    scfnum = 1
    skip = 0


# open filename
fname = str(sys.argv[1])
try:
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
                            try:
                                energy = float(line.split()[1])
                                energies.append(energy)
                                delta_energies.append(float(line.split()[2]))
                            except ValueError:
                                pass
                        try:
                            line = f.next()
                        except:
                            print(' ')
                            print('- - !! THE SCF IS NOT YET CONVERGED !! - -')
                            break
                    break
except IOError:
    sys.exit("The specified file does not exist!")
# truncate the list if needed
if skip == 0:
    pass
else:
    energies[0:skip] = []
    delta_energies[0:skip] = []

# plot energies
x_axis = range(1+skip, 1+len(energies)+skip)
plt.plot(x_axis, energies,'o-')
plt.title('%d SCF Iterations' %len(energies))
plt.xlabel('SCF Iteration')
plt.ylabel('SCF Energy')
plt.show()
x_axis = range(1+skip, 1+len(delta_energies)+skip)
plt.plot(x_axis, delta_energies,'o-')
plt.title('%d SCF Iterations' %len(delta_energies))
plt.xlabel('SCF Iteration')
plt.ylabel('SCF Energy Change')
plt.show()

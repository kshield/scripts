#!/usr/bin/env python
"""
--------------------------------------------------------------------------------
(c) 2017 Julian Rees

License: GNU GPLv3

Description: Print the HOMO and LUMO numbers of an ORCA output file.

Run: python gethomolumo.py filename

Arguments: filename - file name with extension

Dependencies: none
--------------------------------------------------------------------------------
"""
print(__doc__)
import sys
import math

# check for correct number of inputs
if len(sys.argv) != 2:
    sys.exit("You must supply exactly one filename!")

# look for the alpha and beta occupancies
searchfor = "N(Alpha)"
searchfor2 = "N(Beta)"
fname = str(sys.argv[1])
with open(fname) as f:
    content = [line.strip('\n') for line in f.readlines()]

# define integers for alpha and beta HOMOs
for line in content:
   if searchfor in line:
        Nalpha = int(math.floor(float(line.split()[2]))) -1
   elif searchfor2 in line:
        Nbeta = int(math.floor(float(line.split()[2]))) -1

# print output
if 'Nalpha' in locals():
    print " "
    print "- - !! ORBITAL ANALYSIS FINISHED !! - -"
    print "Spin-up HOMO: %d" %Nalpha
    print "Spin-down HOMO: %d" %Nbeta
    if Nalpha != Nbeta:
        print "The system is S=%d/2" %(Nalpha - Nbeta)
    else:
        print "The system is a singlet!"
    print " "
else:
    sys.exit("The file %s does not contain a HOMO!" %fname)

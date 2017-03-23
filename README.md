This is a collection of handy scripts that make my life easier.  
Feel free to use any and all of them to make yours easier too.  
At the moment, they are written in R, python, and a combination of bash and tcsh shells. 

A rough table of contents:

# Python #
## Useful scripts for interacting with ORCA ##
- **geomenergymap.py** first plots the number of SCF iterations required and then the final energy for each step of a geometry optimization.
  * `usage: geomenergymap.py optimization.out`
- **scfconvergence.py** plots the energy and energy difference of each iteration of a selected SCF cycle. One can input both a specific cycle, as well as truncate a desired number of initial iterations (with large energy changes) to better inspect final convergence behavior. 
  * `usage: scfconvergence.py calculation.out 2 -4` will for example plot the second SCF cycle in the output file, skipping the first 4 iterations
- **gethomolumo.py** simply reads the output file and prints the MO number of the alpha and beta HOMO and LUMO, as well as printing the multiplicity.
  * `usage: gethomolumo.py calculation.out`
- **electrostaticpotential.py** has been borrowed from Marius Retegan (http://github.com/mretegan), and will generate a .cube file of the electrostatic potential following an ORCA calculation. A note here, one must use the `! KeepDens` keyword to prevent ORCA from removing the `.scfp` file folloing the calculation. ORCA must also be locally installed.  This calculation can take quite a while (up to hours). 
  * `usage: electrostaticpotential.py jobname` where jobname (without the file extension) is the same for the .out, .scfp, and .xyz files.

## Useful scripts that take the place of your calculator in lab ##
- **masscalc.py** calculates the mass of a compound given a formula weight and number of moles
  * `usage: masscalc.py`
- **molcalc.py** calculates the number of moles of a compound given a formula weight and mass
  * `usage: molcalc.py`
- **serialdilute.py** calculates an array of concentrations for a serial dilution, given the relevant concentrations and volumes. An optional uniform volume addition at the end can also be specified.
  * `usage: serialdilute.py`
  
# R #
- **compile_variables.R** merges a series of variables in the R workspace with a common name stem according the variable id. This currently is only functioning for vectors of data (single columns), not arrays.
  * `usage: output <- var_compile(name_stem, x)` creates a variable output with a single column 'x' and the observational values from all data objects beginning with 'name_stem'
- **import_directory.R** imports into the R workspace all files in a directory with a specified file extension. 
  * `usage: import_directory('/path/to/directory/', '.txt', '\t', TRUE)` imports all .txt files in a directory assuming tab-separated values and a header line
- **pseudo_inverse.R** computes the pseudoinverse of a matrix using singular value decomposition. This is useful for least-squares fitting.
  * `usage: Ainv <- pinv(A)` computes 'Ainv', the psuedoinverse of the matrix 'A'
- **savitzky-golay.R** is an implementation of the popular filter, and requires the above `psuedo_inverse.R` function. 
  * `usage: filtered_data <- sav.gol(data, 5, forder=4, dorder=0)` returns the filtered 'data' using a window of 5 and a 4th order polynomial. Note that using dorder=1 or 2 will return the filtered first or second derivatives of 'data'
- **well_byletter.R** will assemble workspace variables corresponding to 96-well plate names.  
  * `usage: well_byletter` returns a single dataframe for each well letter. Note that the well letters must be capitalized, and other variables beginning with e.g. 'A' will interfere with this function.



Cheers,
Julian

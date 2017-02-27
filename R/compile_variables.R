var_compile <- function(varname, id){
  # this function compiles a series of variables with a common name stem according the variable id
  # known bugs - this module currently cannot handle (due to dim mismatch) data w/ more than one variable to merge
  # redoing how the column naming functions should take care of this

  varname <- glob2rx(as.character(varname))
  varlist <- ls(.GlobalEnv, pattern = varname)

  # assign compd as the first variable in the set
  arg <- paste('compd <- ', varlist[1], sep = '')
  eval(parse(text = arg))

  for(i in 2:length(varlist)){
    # get the column name that matches the id string
    arg <- paste('dropcol <- which( colnames(', varlist[i], ') == id )', sep = '')
    eval(parse(text = arg))

    # drop that column and make the rest the variable add
    arg <- paste('add <- ', varlist[i], '[-', dropcol, ']', sep = '')
    eval(parse(text = arg))

    # combine the collection and the addition data
    compd <- cbind(compd, add)
  }

  # assign the column names to the data
  colnames(compd) <- c(id, varlist)
  return(compd)
}

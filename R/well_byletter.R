well_byletter <- function(){
  # well_byletter takes no arguments. for workspace variables
  # formatted A01, A02, ... H12, consolidates well plate data
  # by letter row and returns a single dataframe for each letter
  # Other workspace variables that begin with capital A through H
  # will interfere with this script.

  # make a character vector of letters
  welllet = LETTERS[1:8]

  for(i in 1:length(welllet)){
    arg1 <-  glob2rx(paste(welllet[i], '*', sep = ''))
    arg2 <- paste("col", welllet[i], sep = "")

    # take the arguments above and make a vector of well names for each letter
    c <- paste(arg2, "<- ls(.GlobalEnv, pattern = arg1, )", sep = "")
    eval(parse(text = c))

    # make the variable tt that is the first well name in each row, make the
    # dataframe of that row's letter
    t <- paste('tt <- ', arg2, "[1]", sep = "")
    eval(parse(text = t))
    d <- paste(welllet[i], " <- ", tt, sep = "")
    eval(parse(text = d))

    # get the number of wells in each row for the next loop
    wn <- paste('wellnum <- length(', arg2,')', sep = "")
    eval(parse(text = wn))
    for(j in 2:wellnum){

      # cbind the additional wells w/ that letter to the above dataframe
      t <- paste('tt <- ', arg2, "[", j, "]", sep = "")
      eval(parse(text = t))
      e <- paste(welllet[i], " <- cbind(", welllet[i], ",", tt, "[2])", sep = "")
      eval(parse(text = e))
    }

    # correct the column names of the dataframe
    arg <- paste("colnames(", welllet[i], ") <- c('wl', ", arg2, ")", sep = "")
    eval(parse(text = arg))

    # make the variable gobal
    glob <- paste("assign('",as.character(welllet[i]), "', ", welllet[i], ", envir = .GlobalEnv)", sep = "")
    eval(parse(text = glob))
  }}

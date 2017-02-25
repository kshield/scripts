well_byletter <- function(){
  E03 <- E03[1:51,]
  welllet = LETTERS[1:8]
  for(i in 1:length(welllet)){
    arg1 <-  glob2rx(paste(welllet[i], '*', sep = ''))
    arg2 <- paste("col", welllet[i], sep = "")
    c <- paste(arg2, "<- ls(.GlobalEnv, pattern = arg1, )", sep = "")
    eval(parse(text = c))
    t <- paste('tt <- ', arg2, "[1]", sep = "")
    eval(parse(text = t))
    d <- paste(welllet[i], " <- ", tt, sep = "")
    eval(parse(text = d))
    del <- paste("rm(",tt,")", sep = "")
    wn <- paste('wellnum <- length(', arg2,')', sep = "")
    eval(parse(text = wn))
    for(j in 2:wellnum){
      t <- paste('tt <- ', arg2, "[", j, "]", sep = "")
      eval(parse(text = t))
      e <- paste(welllet[i], " <- cbind(", welllet[i], ",", tt, "[2])", sep = "")
      eval(parse(text = e))
      #f <- paste("rm(", tt, ")", sep = "")
      #eval(parse(text = f))
    }
    arg <- paste("colnames(", welllet[i], ") <- c('wl', ", arg2, ")", sep = "")
    eval(parse(text = arg))
    glob <- paste("assign('",as.character(welllet[i]), "', ", welllet[i], ", envir = .GlobalEnv)", sep = "")
    eval(parse(text = glob))
    #eval(parse(text = del))
  }}
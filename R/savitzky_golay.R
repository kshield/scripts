sav.gol <- function(T, fl, forder=4, dorder=0)
{
    m <- length(T)
    dorder <- dorder + 1

    # -- calculate filter coefficients --
    fc <- (fl-1)/2                          # index: window left and right
    X  <- outer(-fc:fc, 0:forder, FUN="^")  # polynomial terms and
coefficients
    Y  <- pinv(X);                          # pseudoinverse

    # -- filter via convolution and take care of the end points --
    T2 <- convolve(T, rev(Y[dorder,]), type="o")    # convolve(...)
    T2 <- T2[(fc+1):(length(T2)-fc)]
    return(T2)
}

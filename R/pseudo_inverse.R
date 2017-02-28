pinv <- function (A)
{
    s <- svd(A)
    # D <- diag(s$d); Dinv <- diag(1/s$d)
    # U <- s$u; V <- s$v
    # A = U D V'
    # X = V Dinv U'
    s$v %*% diag(1/s$d) %*% t(s$u)
}

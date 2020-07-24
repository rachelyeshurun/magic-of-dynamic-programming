def solve(X, Y):

    m, n = len(X), len(Y)
    if m == 0 or n == 0:
        return 0 

    if X[m - 1] == Y[n - 1]:
        return 1 + solve(X[0: m - 1], Y[0: n - 1])

    return max(solve(X[0:m], Y[0:n - 1]), solve(X[0:m - 1], Y[0:n]))

#unit tests
assert(solve('a', '') == 0)
assert(solve('happiness', 'pinecones') == 5)
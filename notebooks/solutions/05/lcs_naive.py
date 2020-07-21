def lcs(X, Y, count = 0):

    m, n = len(X), len(Y)
    if m == 0 or n == 0:
        return count 

    if X[m - 1] == Y[n - 1]:
        count = lcs(X[0: m - 1], Y[0: n - 1], count + 1)

    return max(count, lcs(X[0:m], Y[0:n-1], 0), lcs(X[0:m-1], Y[0:n], 0))

def lcs_count(X,Y):
    return lcs(X, Y, 0)

#unit tests
assert(lcs('', '') == 0)
assert(lcs('', 'b') == 0)
assert(lcs('a', '') == 0)
assert(lcs('happiness', 'pinecones') == 4)
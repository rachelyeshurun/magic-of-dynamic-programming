def solve_counter(X, Y, count = 0):

    m, n = len(X), len(Y)
    if m == 0 or n == 0:
        return count 

    if X[m - 1] == Y[n - 1]:
        count = solve_counter(X[0: m - 1], Y[0: n - 1], count + 1)

    return max(count, solve_counter(X[0:m], Y[0:n-1], 0), solve_counter(X[0:m-1], Y[0:n], 0))

def solve(X,Y):
    return solve_counter(X, Y, 0)

#unit tests
assert(solve('', '') == 0)
assert(solve('', 'b') == 0)
assert(solve('a', '') == 0)
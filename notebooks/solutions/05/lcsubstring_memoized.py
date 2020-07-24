    # This clever memoization is from:
    # Schmatz, S. (2017, December 7). Intermediate Dynamic Programming. https://stevenschmatz.github.io/blog/2017/12/07/intermediate-dynamic-programming/
    # However, the memo space looks polynomial since indexes into memo are created for each unique set of input arguments
    # So one for each cell in the grid.
def memoize(original_function):
    memo = {}
    
    def wrapper(*args):
        t_args = tuple(args)
        if t_args in memo:
            return memo[t_args]
            
        result = original_function(*args)
        memo[t_args] = result
        
        return result
        
    return wrapper


@memoize
def solve_count(X, Y, count = 0):

    m, n = len(X), len(Y)
    #print ('in solve_count', m, " : ", X, "   ", n, " : ", Y , " -->", count)
    if m == 0 or n == 0:
        return count 

    if X[m - 1] == Y[n - 1]:
        count = solve_count(X[0: m - 1], Y[0: n - 1], count + 1)

    return max(count, solve_count(X[0:m], Y[0:n-1], 0), solve_count(X[0:m-1], Y[0:n], 0))

def solve_count(X,Y):
    return lcs(X, Y, 0)

#unit tests
solve('abc', 'abc', 0)
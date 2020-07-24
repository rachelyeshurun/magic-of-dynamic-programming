def memoize(original_function):
        memo = {}

        def wrapper(X,Y):
            key = tuple([X,Y])
            if key not in memo:
                memo[key] = original_function(X,Y)
                
                #uncomment the following lines to see how many times the grid gets filled 
                #memoize.counter+=1 
                #print (memoize.counter, memo)
                
            return memo[key]

        return wrapper
  
memoize.counter = 0 ### function attribute to count filled cells

@memoize
def solve(X, Y):

    m, n = len(X), len(Y)
    if m == 0 or n == 0:
        return 0 

    if X[m - 1] == Y[n - 1]:
        return 1 + solve(X[0: m - 1], Y[0: n - 1])

    return max(solve(X[0:m], Y[0:n - 1]), solve(X[0:m - 1], Y[0:n]))


#unit tests
#solve('abc', 'abc')
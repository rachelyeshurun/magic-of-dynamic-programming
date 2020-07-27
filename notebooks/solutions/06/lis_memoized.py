def memoize(original_function):
        memo = {}

        def wrapper(top, v):
            key = tuple([top, len(v)])
            if key not in memo:
                memo[key] = original_function(top, v)
                
                #uncomment the following lines to see how many times the grid gets filled 
                #memoize.counter+=1 
                #print (memoize.counter, memo)
                
            return memo[key]

        return wrapper
  
memoize.counter = 0 ### function attribute to count filled cells

@memoize
# Solution from here https://www.techiedelight.com/longest-increasing-subsequence-using-dynamic-programming/
# but I started from the end of the sequence, just as a matter of preference.
def lis(top, v):
    n = len(v)
    if n == 0:
        return 0

    # exclude the last item
    excluded = lis(v[n - 1], v[0:n -1])
    
    # include the last item - but only if it's less than the current item at top of sequence
    if v[n - 1] < top:
        included =  1 + lis(v[n - 1], v[0:n -1])
    else:
        included = 0

    return max(included, excluded)


def solve(v):
    # start with infinite, so the last item in the list gets a chance to be in the final subsequence
    return lis(float('inf'), v)
          
        
# unit tests
# YOUR CASES HERE ###
assert(solve(v = [3, 1, 4, 1, 5, 1, 9, 2, 6]) == 5)
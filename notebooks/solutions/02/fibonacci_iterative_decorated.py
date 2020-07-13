def iterate(f):
    memo = {0:0}

    def helper(n):
        # print ('helper called for ', n)
        if n not in memo:
            for k in range(1, n + 1):
                memo[k] = f(k)
        # print(memo)
        return memo[n]
    return helper

@iterate
def fib(n):
    if n <= 2:
        return 1
    return fib(n - 1) + fib(n - 2)

#unit tests
#assert(fib(0) == 1)
#assert(fib(1) == 1)
#assert(fib(2) == 1)
#assert(fib(6) == 8)
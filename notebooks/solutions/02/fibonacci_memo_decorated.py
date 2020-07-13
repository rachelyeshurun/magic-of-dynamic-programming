def memoize(f):
    memo = {}

    def helper(n):
        if n not in memo:
            memo[n] = f(n)
        return memo[n]

    return helper

@memoize
def fib(n):
    if n <= 2:
        return 1
    return fib(n - 1) + fib(n - 2)

#assert(fib(1) == 1)
#assert(fib(2) == 1)
#assert(fib(6) == 8)
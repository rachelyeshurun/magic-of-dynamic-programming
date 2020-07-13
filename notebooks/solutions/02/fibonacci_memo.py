def fib(n, memo):
    if n in memo:
        return memo[n]
    if n <= 2:
        f = 1
    else:
        f = fib(n-1, memo) + fib(n-2, memo)
    memo[n] = f
    return memo[n]

### unit tests ###
#assert(fib(1, {}) == 1)
#assert(fib(2, {}) == 1)
#assert(fib(3, {}) == 2)
#assert(fib(4, {}) == 3)
#assert(fib(5, {}) == 5)
#assert(fib(6, {}) == 8)
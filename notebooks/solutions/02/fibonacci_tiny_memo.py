def fib(n):
    f, next_total = 1, 1
    for i in range(n-1):
        f, next_total = next_total, next_total + f
    return f

#assert(fib(1) == 1)
#assert(fib(2) == 1)
#assert(fib(6) == 8)
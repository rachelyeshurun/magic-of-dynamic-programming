def solve(v):
    
    n = len(v)
    if n == 2:
        return max(v[0], v[1])
    elif n == 1:
        return v[0]
    elif n == 0:
        return 0

    return max(v[n-1] + solve(v[0: n - 2]), solve(v[0: n - 1]))

# unit tests
assert(solve([]) == 0)
assert(solve([5]) == 5)
assert(solve([5, 6]) == 6)
assert(solve([5, 5, 5, 5, 5]) == 15)
assert(solve([3, 1, 4, 1, 5, 9, 2, 6]) == 22)
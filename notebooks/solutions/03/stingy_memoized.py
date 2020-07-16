def memoize(f):
    memo = {}

    def helper(v):
        n = len(v)
        if n not in memo:
            memo[n] = f(v)
        return memo[n]

    return helper

@memoize
def solve_stingy(v):

        n = len(v)
        if n == 3:
            return max(v[0], v[1], v[2]) 
        elif n == 2:
            return max(v[0], v[1])
        elif n == 1:
            return v[0]
        elif n == 0:
            return 0

        return max(v[n-1] + solve_stingy(v[0: n - 3]), solve_stingy(v[0: n - 2]), solve_stingy(v[0: n - 1]))

#unit tests
assert(solve_stingy([]) == 0)
assert(solve_stingy([3]) == 3)
assert(solve_stingy([3, 1]) == 3)
assert(solve_stingy([3, 1, 4]) == 4)
assert(solve_stingy([3, 1, 4, 1, 5, 9, 2, 6]) == 14)
def sum(numbers):

    n = len(numbers)
    if n <= 0:
        return 0
    return sum(numbers[0: n - 1]) + numbers[n - 1]
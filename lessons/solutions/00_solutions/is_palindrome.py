def is_palindrome(s):

    n = len(s)

    if n == 0 or n == 1:
        return 1
    return s[0] == s[n - 1] and is_palindrome(s[1:n - 1])
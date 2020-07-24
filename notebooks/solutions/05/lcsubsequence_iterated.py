def solve(X, Y):
    
    # will hold only two rows
    memo = {}
    m, n = len(X), len(Y)

    for i in range(m + 1):       
        for j in range(n + 1):
            
            # run along all the columns, but only need 2 rows: row 0 and row 1          
            col = j 
            row = i%2
        
            # The 'upper' row will alternate:  first row 0 is the upper row, then row 1 becomes the 'upper' row
            if row == 0:
                upper = row + 1
            else:
                upper = row - 1
                
            key = tuple([row, col])    
            if i == 0 or j == 0:
                memo[key] = 0
            elif X[i - 1] == Y[j - 1]:
                memo[key] = 1 + memo[tuple([upper, col - 1])]
            else:
                memo[key] = max(memo[tuple([row, col - 1])], memo[tuple([upper, col])])
            
            #solve.counter += 1
            #print(solve.counter, memo)
    
    return memo[tuple([row,col])]

solve.counter = 0 ### function attribute to count filled cells

#unit tests
#solve('rachel', 'rachel')
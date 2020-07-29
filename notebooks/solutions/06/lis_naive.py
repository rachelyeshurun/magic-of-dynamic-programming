# solution based on this code: https://www.geeksforgeeks.org/longest-increasing-subsequence-dp-3/  by NIKHIL KUMAR SINGH 

# maximum over all n
global maximum 
  
def max_ending_here(v): 
  
    global maximum 
  
    n = len(v)
    
    # base cases
    if n == 0:
        return 0
    if n == 1: 
        return 1
  
    # max_length_ending_here is the length of the longest increasing subsequence ending with v[n-1] 
    max_length_ending_here = 1
  
    for i in range(1, n): 
        # recursively get all LIS ending with v[0], ..., v[i - 2]
        res = max_ending_here(v[0: i]) 
        
        # if an element before v[n-1] is smaller than v[n-1] and its LIS is greater, then its LIS becomes the new local maximum
        if v[i - 1] < v[n-1] and res + 1 > max_length_ending_here: 
            max_length_ending_here = res + 1
  
    # update overall maximum 
    maximum = max(maximum , max_length_ending_here) 
  
    return max_length_ending_here 
  
def lis(v): 
  
    global maximum 
  
    # will be updated by the recursive function 'max_ending_here' 
    maximum = 0
  
    m = max_ending_here(v)
    print ('maximum ending here: ', m, 'global maximum: ', maximum)
    
    return maximum
  
#unit tests
assert(lis([3, 1, 4, 1, 5, 1, 9, 2, 6]) == 4)
assert(lis([3, 1, 4, 1, 5, 1, 9, 2, 6, 5]) == 4)
assert(lis([1, 2, 3]) == 3)
assert(lis([3, 2, 1, 0]) == 1)
assert(lis([]) == 0)
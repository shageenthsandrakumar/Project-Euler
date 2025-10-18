def ispalindrome(n):
    num = str(n)
    x = len(num)//2
    for i in range(x):
     if num[i] != num[-1-i]:
         return False
    return True 

largest = (0,0,0)

for i in range(100, 1000):       
    j_start = (100000 + i - 1) // i
    j_start_11 = ((j_start + 10) // 11) * 11
    for j in range(j_start_11, 1000, 11):
        product = i * j
        if ispalindrome(product) and product > largest[0]:
                largest = (product,i,j)
        
if not sum(largest):
    for i in range(100, 1000):
        j_start = (10000 + i - 1) // i
        j_end = min(999, 99999 // i)
        for j in range(j_start, j_end + 1):
            product = i * j
            if ispalindrome(product) and product > largest[0]:
                largest = (product,i,j)

answer,a,b = largest
print(f"The largest palindrome product of two 3-digit numbers is: {answer}")
print(f"It is the product of {a} × {b}")

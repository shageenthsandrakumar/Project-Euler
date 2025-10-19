def ispalindrome(n):
    num = str(n)
    x = len(num)//2
    for i in range(x):
     if num[i] != num[-1-i]:
         return False
    return True 

largest = (0,0,0)

for i in range(999, 99, -1):
    if i*990 < largest[0]:
        break
    j_small = max((100000 + i - 1) // i,100)
    j_small_11 = ((j_small + 10) // 11) * 11
    for j in range(990, j_small_11-1, -11):
        product = i * j
        if product > largest[0]:
            if ispalindrome(product):
                largest = (product,i,j)
        else:
            break
if not sum(largest):
    for i in range(999,99,-1):
        j_end = min(999, 99999 // i)
        if i*j_end < largest[0]:
            break
        for j in range(j_end,99,-1):
            product = i * j
            if product > largest[0]:
                if ispalindrome(product):
                    largest = (product,i,j)
            else:
                break

answer,a,b = largest
print(f"The largest palindrome product of two 3-digit numbers is: {answer}")
print(f"It is the product of {a} × {b}")

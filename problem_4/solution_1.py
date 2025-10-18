def ispalindrome(n):
    num = str(n)
    x = len(num)//2
    for i in range(x):
     if num[i] != num[-1-i]:
         return False
    return True 

largest = (0,0,0)
for i in range(100,1000):
    for j in range(i,1000):
        product = i*j
        if ispalindrome(product):
            if product > largest[0]:
                largest = (product,i,j)
answer,a,b = largest
print(f"The largest palindrome product of two 3-digit numbers is: {answer}")
print(f"It is the product of {a} × {b}")

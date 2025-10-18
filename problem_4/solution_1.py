def ispalindrome(n):
    num = str(n)
    x = len(num)//2
    for i in range(x):
     if num[i] != num[-1-i]:
         return False
    return True 

palindromes = []
for i in range(100,1000):
    for j in range(i,1000):
        product = i*j
        if ispalindrome(product):
            palindromes.append((product,i,j))
palindromes.sort(reverse=True)

answer,a,b = palindromes[0]
print(f"The largest palindrome product of two 3-digit numbers is: {answer}")
print(f"It is the product of {a} × {b}")

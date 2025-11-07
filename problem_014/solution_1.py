def collatz_length(n):
    if n == 1:
        return 1
    elif n%2:
        return 1+collatz_length(3*n+1)
    else:
        return 1+collatz_length(n//2)
max_length = 0
start_number = 0
for i in range(1,1000000):
    c = collatz_length(i)
    if max_length < c:
        max_length = c
        start_number = i
print(start_number)

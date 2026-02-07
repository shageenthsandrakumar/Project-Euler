def diagonal_sum(n):
    if n == 1:
        return 1
    elif n%2==1 and n>1:
        answer = diagonal_sum(n-2)
        corner = n**2
        for corners in range(4):
            answer += corner
            corner -= n-1
        return answer
    else:
        print("Error: n should be a positive odd integer!")
        
s = 1001
print(diagonal_sum(s))

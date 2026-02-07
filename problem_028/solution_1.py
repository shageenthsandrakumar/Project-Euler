def diagonal_sum(n):
    if not n%2:
        print("Error: n should be an odd integer!")
    elif n == 1:
        return 1
    else:
        answer = diagonal_sum(n-2)
        corner = n**2
        for corners in range(4):
            answer += corner
            corner -= n-1
        return answer
s = 1001
print(diagonal_sum(s))

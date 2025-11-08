collatz_lengths = {}
collatz_lengths[1] = 1

def collatz_length(n):
    sequence = []
    while n not in collatz_lengths:
        sequence.append(n)
        n,is_odd = divmod(n,2)
        n += is_odd*(5*n+4)
    L = collatz_lengths[n]
    for num in reversed(sequence):
        L += 1
        collatz_lengths[num] = L
    return L

max_length = 0
start_number = 0
for i in range(1000000-1,1,-1):
    c = collatz_length(i)
    if max_length < c:
        max_length = c
        start_number = i
print(start_number)

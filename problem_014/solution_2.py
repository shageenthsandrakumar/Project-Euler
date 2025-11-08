collatz_lengths = {}
collatz_lengths[1] = 1

def collatz_length(n):
    if n in collatz_lengths:
        return collatz_lengths[n]
    nxt,is_odd = divmod(n,2)
    nxt += is_odd*(5*nxt+4)
    L = 1+collatz_length(nxt)
    collatz_lengths[n] = L
    return L

max_length = 0
start_number = 0
for i in range(1000000-1,1,-1):
    c = collatz_length(i)
    if max_length < c:
        max_length = c
        start_number = i
print(start_number)

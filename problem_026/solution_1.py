def cycle_length(d):
    if not d:
        return 0
    while not d%2:
        d //= 2
    while not d%5:
        d //= 5
    if not d-1:
        return 0
    power = 1
    while pow(10,power,d)-1:  # 10^power ≡ 1 (mod d)
        power += 1
    return power

threshold = 1000
d_max = 0
max_length = 0
for d in range(threshold):
    length = cycle_length(d)
    if length > max_length:
        max_length =length
        d_max = d
print(d_max)

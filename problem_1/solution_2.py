threshold = 1000
sum = 0
for n in range(1,threshold):
    if not (n%3*n%5):
        sum += n
print(sum)

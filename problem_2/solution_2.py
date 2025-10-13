previous = 0
current = 1
sum = 0 
threshold = 4000000
while current < threshold:
    previous,current = current,previous+current
    if not previous%2:
        sum += previous
print(sum)

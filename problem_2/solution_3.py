previous = 0
current = 2
sum = 0 
threshold = 4000000
while current < threshold:
    previous,current = current,previous+4*current
    sum += previous
print(sum)

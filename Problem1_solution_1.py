
number_of_3s = int(1000/3)
number_of_5s = 1000/5-1
number_of_15s = int(1000/15)

sum_of_3s = 3*(number_of_3s)*(number_of_3s+1)/2
sum_of_5s = 5*(number_of_5s)*(number_of_5s+1)/2
sum_of_15s = 15*(number_of_15s)*(number_of_15s+1)/2

final_sum = sum_of_3s + sum_of_5s - sum_of_15s
print(int(final_sum))


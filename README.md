# Project-Euler
This repository contains my Python solutions to Project Euler problems. Each problem may have multiple solutions that explore different mathematical or algorithmic approaches. The goal is to understand the reasoning behind each method and compare their efficiency and simplicity.



Problem 1: Multiples of 3 and 5

Problem statement:
Find the sum of all the multiples of 3 or 5 below a given threshold (default 1000).

Solution approach:

Count the number of multiples below the threshold for 3, 5, and 15.

Use the formula for the sum of an arithmetic series to calculate:

Sum of multiples of 3

Sum of multiples of 5

Sum of multiples of 15 (to correct for double-counting)

Calculate the final sum as:

final_sum = sum_of_3s + sum_of_5s - sum_of_15s


Why subtract multiples of 15?
Numbers divisible by both 3 and 5 are counted twice when summing multiples of 3 and 5 separately. Subtracting the sum of multiples of 15 corrects this.

Code (Problem1_solution_1.py):

threshold = 1000
number_of_3s = (threshold-1)//3
number_of_5s = (threshold-1)//5
number_of_15s = (threshold-1)//15

sum_of_3s = 3*(number_of_3s)*(number_of_3s+1)//2
sum_of_5s = 5*(number_of_5s)*(number_of_5s+1)//2
sum_of_15s = 15*(number_of_15s)*(number_of_15s+1)//2

final_sum = sum_of_3s + sum_of_5s - sum_of_15s
print(final_sum)


Output:

233168


Notes:

The threshold variable can be changed to calculate the sum below any upper limit.

This solution uses the arithmetic series formula, which is more efficient than iterating through each number.

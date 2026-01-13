#include <iostream>

long long  multiples_3_5_solution_1 (long long threshold) {
	long long number_of_3s = (threshold - 1) / 3;
	long long number_of_5s = (threshold - 1) / 5;
	long long number_of_15s = (threshold - 1) / 15;

	long long sum_of_3s = 3 * (number_of_3s) * (number_of_3s + 1);
	long long sum_of_5s = 5 * (number_of_5s) * (number_of_5s + 1);
	long long sum_of_15s = 15 * (number_of_15s) * (number_of_15s + 1);
	return (sum_of_3s + sum_of_5s - sum_of_15s)/2;
}

long long multiples_3_5_solution_2(long long threshold) {
	long long sum = 0;
	for (long long i = 0; i < threshold; i++) {
		if (i % 3 == 0 || i % 5 == 0) {
			sum += i;
		}
	}
	return sum;
}

int main() {
	long long threshold;
	int solution_choice;
	std::cout << "Would you like to try Solution_1 or Solution_2? Solution_1 is better for bigger thresholds!" << std::endl;
	std::cout << "Please Enter 1 or 2: ";
	std::cin >> solution_choice;
		while (solution_choice != 1 && solution_choice != 2) {
			std::cout << "Invalid choice. Please enter 1 or 2." << std::endl;
			std::cin >> solution_choice;
		}
	std::cout << "Enter the threshold value: ";
	std::cin >> threshold;
	if (solution_choice == 1) {
		long long result = multiples_3_5_solution_1(threshold);
		std::cout << "The sum of all multiples of 3 or 5 below " << threshold << " is: " << result << std::endl;
		return 0;
	}
	else if (solution_choice == 2) {
		long long result2 = multiples_3_5_solution_2(threshold);
		std::cout << "The sum of all multiples of 3 or 5 below " << threshold << " is: " << result2 << std::endl;
		return 0;
	}
}

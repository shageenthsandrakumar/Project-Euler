#include <iostream>

long long trial_division(long long n) {
	long long max_factor = 1;
	long long factor = 2;
	while (factor <= n){
		if (n% factor == 0) {
			n /= factor;
			max_factor = factor;
		}
		else {
			factor++;
		}
	}
	return max_factor;

}

long long optimized_trial_division(long long n) {
	long long max_factor = 1;
	long long factor = 2;
	while (factor*factor <= n) {
		if (n % factor == 0) {
			n /= factor;
			max_factor = factor;
		}
		else {
			factor++;
		}
	}
	if (n > 1) {
		max_factor = n;
	}
	return max_factor;

}

long long wheel_factorization(long long n) {
	if (n <= 1) return 0;
	long long max_factor = 1;
	while (n % 2 == 0) {
		n /= 2;
		max_factor = 2;
	}
	while (n % 3 == 0) {
		n /= 3;
		max_factor = 3;
	}
	long long factor = 5;
	int step = 2;
	while (factor * factor <= n) {
		while (n % factor == 0) {
			n /= factor;
			max_factor = factor;
		}
		factor += step;
		step = 6 - step;
	}
	if (n > 1) {
		max_factor = n;
	}
	return max_factor;

}




int main() {
	long long threshold;
	int solution_choice;
	std::cout << "Would you like to try Solution_1, Solution_2, or Solution_3?" << std::endl;
	std::cout << "Please enter a number from 1-3: ";
	std::cin >> solution_choice;
		while (solution_choice != 1 && solution_choice != 2 &&  solution_choice != 3) {
			std::cout << "Invalid choice. Please enter a number from 1-4." << std::endl;
			std::cin >> solution_choice;
		}
	std::cout << "Enter the threshold value: ";
	std::cin >> threshold;

	if (solution_choice == 1) {
		long long result = trial_division(threshold);
		std::cout << "The largest prime factor of " << threshold << " is: " << result << std::endl;
		return 0;
	}
	else if (solution_choice == 2) {
		long long result2 = optimized_trial_division(threshold);
		std::cout << "The largest prime factor of " << threshold << " is: " << result2 << std::endl;
		return 0;
	}
	else if (solution_choice == 3) {
		long long result3 = wheel_factorization(threshold);
		std::cout << "The largest prime factor of " << threshold << " is: " << result3 << std::endl;
		return 0;
	}

	
}

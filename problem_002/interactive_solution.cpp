#include <iostream>
#include <cmath>

long long binet_geometric_series(long long threshold)
{
	long double phi = (1.0L + std::sqrt(5.0L)) / 2.0L;
	long double psi = (1.0L - std::sqrt(5.0L)) / 2.0L;
	long double ephi = std::pow(phi, 3.0L);
	long double epsi = std::pow(psi, 3.0L);
	// Using Binet's approximation to find a candidate value for N
	long long n_cand = static_cast<long long> (std::log(threshold * std::sqrt(5.0L)) / std::log(ephi));
		//We must check index below just in case because Binet's appoximation is an upper bound. 
	long long N = n_cand - 1;
	long double E_N = (std::pow(ephi, N) - std::pow(epsi, N)) / std::sqrt(5.0L);
		while (E_N < threshold) {
			N += 1;
			E_N = (std::pow(ephi, N) - std::pow(epsi, N)) / std::sqrt(5.0L);}
	N -= 1;
	long double sum_ephi = ephi * (std::pow(ephi,N) - 1) / (ephi - 1);
	long double sum_epsi = epsi * (std::pow(epsi,N) - 1) / (epsi - 1);
	long long sum_even = static_cast<long long>(std::round((sum_ephi - sum_epsi) / std::sqrt(5.0L)));
	return sum_even;
}

long long iterative_mod_solution(long long threshold) {
	long long sum_even = 0;
	long long previous = 0;
	long long current = 1;
	while (current < threshold) {
		long long next = previous + current;
		previous = current;
		current = next;
		if (previous % 2 == 0) {
			sum_even += previous;
		}
	}
	return sum_even;
}

long long iterative_even_solution(long long threshold) {
	long long sum_even = 0;
	long long previous = 0;
	long long current = 2;
	while (current < threshold) {
		long long next = previous + 4*current;
		previous = current;
		current = next;
		sum_even += previous;
	}
	return sum_even;
}
long long iterative_binet_solution(long long threshold) {
	long double sum_even = 0;
	long long n = 0;
	long double phi = (1.0L + std::sqrt(5.0L)) / 2.0L;
	long double psi = (1.0L - std::sqrt(5.0L)) / 2.0L;
	long double ephi = std::pow(phi, 3.0L);
	long double epsi = std::pow(psi, 3.0L);
	long double E_n = (std::pow(ephi, n) - std::pow(epsi, n)) / std::sqrt(5.0L);
		while (E_n < threshold) {
			n += 1;
			E_n = (std::pow(ephi, n) - std::pow(epsi, n)) / std::sqrt(5.0L);
			sum_even += E_n;
		}
		sum_even -= E_n; // Remove the last added term that exceeded the threshold
		
	return static_cast<long long>(std::round(sum_even));
}



int main() {
	long long threshold;
	int solution_choice;
	std::cout << "Would you like to try Solution_1, Solution_2, Solution_3, or Solution 4?" << std::endl;
	std::cout << "Please enter a number from 1-4: ";
	std::cin >> solution_choice;
		while (solution_choice != 1 && solution_choice != 2 &&  solution_choice != 3 && solution_choice != 4) {
			std::cout << "Invalid choice. Please enter a number from 1-4." << std::endl;
			std::cin >> solution_choice;
		}
	std::cout << "Enter the threshold value: ";
	std::cin >> threshold;

	if (solution_choice == 1) {
		long long result = binet_geometric_series(threshold);
		std::cout << "The sum of all even Fibonacci numbers below " << threshold << " is: " << result << std::endl;
		return 0;
	}
	else if (solution_choice == 2) {
		long long result2 = iterative_mod_solution(threshold);
		std::cout << "The sum of all even Fibonacci numbers below " << threshold << " is: " << result2 << std::endl;
		return 0;
	}
	else if (solution_choice == 3) {
		long long result3 = iterative_even_solution(threshold);
		std::cout << "The sum of all even Fibonacci numbers below " << threshold << " is: " << result3 << std::endl;
		return 0;
	}
	else if (solution_choice == 4) {
		long long result4 = iterative_binet_solution(threshold);
		std::cout << "The sum of all even Fibonacci numbers below " << threshold << " is: " << result4 << std::endl;
		return 0;
	}
	
}

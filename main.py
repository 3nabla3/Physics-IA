import numpy as np

jerome_tt_data = {
	38.9: 372,
	38.4: 356,
	38.1: 358,
	35.6: 289,
	33.8: 269,
	31.6: 233,
	30.5: 201,
	28.3: 171,
	28	: 171,
	26.5: 157,
	25.3: 135
}

alban_tt_data = {
	36.3: 252,
	34.4: 221,
	31.1: 183,
	28.4: 145,
	27.7: 131,
	26.2: 117,
	25.5: 110
}

jerome_rb_data = {
	25.6: 152,
	28.1: 206,
	30.9: 250,
	31.8: 267,
	32.8: 280,
	34.9: 311,
	35.4: 359,
}

alban_rb_data = {
	22.1: 100,
	22.9: 110,
	24.0: 115,
	24.6: 125,
	26.1: 138,
	27.3: 151,
	28.7: 173,
	29.5: 194,
	31.6: 236
}

alban_pack_data = {
	25.5: 93,
	28.3: 125,
	30.7: 158,
	31.8: 169,
	32.8: 191,
	34.9: 202,
	35.1: 238,
}


class Results:
	def __init__(self, error, cd, cr):
		self.error = error
		self.optimal_cd = cd
		self.optimal_cr = cr


def calculate_power(speed: float, mass: float, cd: float, cr: float) -> float:
	pd = cd * (speed / 3.6) ** 3
	dr = cr * (speed / 3.6) * 9.81 * mass
	return pd + dr


def calculate_error(cd: float, cr: float, dataset: dict[float, int]) -> float:
	total_error = 0
	denominator = 0
	for i in dataset:
		calculated_power = calculate_power(i, 78 + 10, cd, cr)
		error = (calculated_power - dataset[i]) ** 2
		total_error += error
		denominator += dataset[i] ** 2

		# print(error, data[i] ** 2, denominator)
		# print(data[i], end="\t")
		# print(round(calculated_power, 1), end="\t")
		# print(round(error, 2), end="\t")
		# print()
	coef_error = np.sqrt(total_error / denominator)
	return coef_error


def calculate_best_coef(dataset: dict[float, int]) -> Results:
	lowest_error = 1e10
	cd_of_lowest = None
	cr_of_lowest = None
	for potential_cd in np.arange(0.12, 0.32, 0.001):
		for potential_cr in np.arange(0.005, 0.015, 0.00005):
			error = calculate_error(potential_cd, potential_cr, dataset)
			if error < lowest_error:
				lowest_error = error
				cd_of_lowest = potential_cd
				cr_of_lowest = potential_cr

	return Results(lowest_error, cd_of_lowest, cr_of_lowest)


def calculate_best_coef_from_fixed_cr(dataset: dict[float, int], fixed_cr: float) -> Results:
	lowest_error = 1e10
	cd_of_lowest = None
	for potential_cd in np.arange(0.12, 0.32, 0.0001):
		error = calculate_error(potential_cd, fixed_cr, dataset)
		if error < lowest_error:
			lowest_error = error
			cd_of_lowest = potential_cd

	return Results(lowest_error, cd_of_lowest, fixed_cr)


def calculate_best_coef_from_multiple_datasets(datasets: list[dict[float, int]]) -> list[Results]:
	lowest_total_error = 1e10
	errors_of_lowest = []
	cds_of_lowest = []
	cr_of_lowest = None
	for potential_cr in np.arange(0.005, 0.015, 0.000005):
		total_error = 0
		current_errors = []
		current_cds = []
		for dataset in datasets:
			result = calculate_best_coef_from_fixed_cr(dataset, potential_cr)
			total_error += result.error
			current_cds.append(result.optimal_cd)
			current_errors.append(result.error)

		if total_error < lowest_total_error:
			lowest_total_error = total_error
			cr_of_lowest = potential_cr
			cds_of_lowest = current_cds
			errors_of_lowest = current_errors

	return [Results(error, cd_of_lowest, cr_of_lowest) for error, cd_of_lowest in zip(errors_of_lowest, cds_of_lowest)]


def print_results(results: Results) -> None:
	print(f"error = {round(results.error * 100, 1)}%")
	print(f"cd = {round(results.optimal_cd, 3)}")
	print(f"cr = {round(results.optimal_cr, 4)}")
	print()


def main():
	alban_tt = calculate_best_coef(jerome_tt_data)
	print("--- Alban TT ---")
	print_results(alban_tt)

	print("--- Jerome TT ---")
	jerome_tt = calculate_best_coef(alban_tt_data)
	print_results(jerome_tt)

	print("--- Alban RB ---")
	alban_rb = calculate_best_coef(alban_rb_data)
	print_results(alban_rb)

	print("--- Jerome RB ---")
	jerome_rb = calculate_best_coef(jerome_rb_data)
	print_results(jerome_rb)

	print("--- Alban PK ---")
	alban_pack = calculate_best_coef(alban_pack_data)
	print_results(alban_pack)

	# print("--- Optimal cr ---")
	# datasets = [alban_tt_data, jerome_tt_data, alban_rb_data, jerome_rb_data, alban_pack_data]
	# results = calculate_best_coef_from_multiple_datasets(datasets)
	#
	# for result in results:
	# 	print_results(result)


if __name__ == '__main__':
	main()

import math
import sys
import os

import pandas as pd
from pandas.api.types import is_numeric_dtype

def series_count(series):
	count = 0

	for i, _ in series.items():
		count += 1

	return count

def series_agg(series):
	agg = 0

	for _, v in series.items():
		agg += v

	return agg

def series_mean(series):
	return series_agg(series) / series_count(series)

def series_std(series):
	count = series_count(series)
	mean = series_mean(series)
	tmp = 0

	for _, value in series.items():
		tmp += (value - mean) * (value - mean)

	return math.sqrt(tmp / (count - 1))

def series_min(series):
	m = series[0]

	for _, v in series.items():
		if m > v:
			m = v

	return m

def series_max(series):
	m = series[0]

	for _, v in series.items():
		if m < v:
			m = v

	return m

def series_range(series):
	return series_max(series) - series_min(series)

def series_percentile(series, p):
	series = series.sort_values(ignore_index=True)
	count = series_count(series)
	i = int((count - 1) * p)
	j = i + 1
	fraction = ((count - 1) * p) % 1
	percentile = series[i] + (series[j] - series[i]) * fraction
	return percentile

def series_variance(series):
	count = series_count(series)
	agg = series_agg(series)
	mean = agg / count
	squared_deviations = [(x - mean) ** 2 for x in series]
	total_squared_deviations = sum(squared_deviations)
	variance = total_squared_deviations / (count - 1)

	return variance

def describe(df):
	names = []
	counts = []
	means = []
	medians = []
	vars = []
	stds = []
	ranges = []
	mins = []
	p20s = []
	p40s = []
	p60s = []
	p80s = []
	maxs = []

	for name, series in df.items():
		if is_numeric_dtype(series):
			series = series.dropna().sort_values(ignore_index=True)
			if series_count(series) == 0:
				continue ;
			names.append(name)
			counts.append(series_count(series))
			means.append(series_mean(series))
			medians.append(series_percentile(series, 0.5))
			vars.append(series_variance(series))
			stds.append(series_std(series))
			ranges.append(series_range(series))
			mins.append(series_min(series))
			p20s.append(series_percentile(series, 0.2))
			p40s.append(series_percentile(series, 0.4))
			p60s.append(series_percentile(series, 0.6))
			p80s.append(series_percentile(series, 0.8))
			maxs.append(series_max(series))

	description_table = pd.DataFrame([counts, means, medians, vars, stds, ranges, mins, p20s, p40s, p60s, p80s, maxs],
									columns=names,
									index=["count", "mean", "median", "var", "std", "range", "min", "20%", "40%", "60%", "80%", "max"])
  
	print(description_table)

def check_argv():
    if len(sys.argv) != 2:
        print("Error: Programm needs exactly 1 argument!")
        sys.exit(1)
    if not sys.argv[1].endswith('.csv'):
        print("Error: The input file must be a .csv file!")
        sys.exit(1)
    if os.path.exists(sys.argv[1]) == 0:
        print(f"Error: The file '{sys.argv[1]}' does not exist!")
        sys.exit(1)
    if os.path.getsize(sys.argv[1]) == 0:
        print(f"Error: The file '{sys.argv[1]}' is empty!")
        sys.exit(1)

# Script entry
pd.set_option("display.max_columns", 1000)

check_argv()

path = sys.argv[1]
df = pd.read_csv(path)
describe(df)

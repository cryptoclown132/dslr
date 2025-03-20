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

def series_percentile(series, p):
	series = series.sort_values(ignore_index=True)
	count = series_count(series)
	i = int((count - 1) * p)
	j = i + 1
	fraction = ((count - 1) * p) % 1
	percentile = series[i] + (series[j] - series[i]) * fraction
	return percentile

def describe(df):
	names = []
	counts = []
	means = []
	stds = []
	mins = []
	p25s = []
	p50s = []
	p75s = []
	maxs = []

	for name, series in df.items():
		if is_numeric_dtype(series):
			series = series.dropna().sort_values(ignore_index=True)
			if series_count(series) == 0:
				continue ;
			names.append(name)
			counts.append(series_count(series))
			means.append(series_mean(series))
			stds.append(series_std(series))
			mins.append(series_min(series))
			p25s.append(series_percentile(series, 0.25))
			p50s.append(series_percentile(series, 0.5))
			p75s.append(series_percentile(series, 0.75))
			maxs.append(series_max(series))

	description_table = pd.DataFrame([counts, means, stds, mins, p25s, p50s, p75s, maxs],
									columns=names,
									index=["count", "mean", "std", "min", "25%", "50%", "75%", "max"])
  
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

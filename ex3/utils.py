
import pandas as pd
import math
import numpy as np
import json
import sys

def series_count(series):
	count = 0

	for _, i in series.items():
		if pd.isna(i) == False:
			count += 1
	return count

def series_agg(series):
	agg = 0

	for _, v in series.items():
		if pd.isna(v) == False:
			agg += v

	return agg

def series_mean(series):
	return series_agg(series) / series_count(series)

def series_std(series):
	count = series_count(series)
	mean = series_mean(series)
	tmp = 0

	for _, value in series.items():
		if pd.isna(value) == False:
			tmp += (value - mean) * (value - mean)

	return math.sqrt(tmp / (count - 1))

def standardize_data(train_data):
	mean_train = train_data.apply(series_mean)
	std_scaled = train_data.apply(series_std)
	train_data_standardized = (train_data - mean_train) / std_scaled
	train_data_standardized = np.hstack([np.ones((train_data_standardized.shape[0], 1)), train_data_standardized])
	return mean_train, std_scaled, train_data_standardized

def load_data(filename):
	df = pd.read_csv(filename)
	features = df.columns.drop(['Index', 'Hogwarts House', 'First Name', 'Last Name', 
								'Birthday', 'Best Hand', 'Arithmancy','Astronomy','Herbology','Divination',
								'Muggle Studies','History of Magic','Transfiguration','Potions','Care of Magical Creatures','Flying']).tolist()
	df = df.dropna()
	df = df.reset_index(drop=True)

	mean_train, std_scaled, train_data_standardized = standardize_data(df[features].copy())
	labels = pd.get_dummies(df['Hogwarts House'])
	return train_data_standardized, labels, features, mean_train, std_scaled

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def save_models(models, features, mean_train, std_scaled, filename):
	data = {
		'features': features,
		'mean_train': mean_train.to_dict(),
		'std_scaled': std_scaled.to_dict(),
		'models': {house: weights.tolist() for house, weights in models.items()}
	}
	with open(filename, 'w') as f:
		json.dump(data, f)

def get_data():
	if len(sys.argv) != 2:
		print("Usage: logreg_train.py dataset_train.csv")
		sys.exit(1)
	return load_data(sys.argv[1])

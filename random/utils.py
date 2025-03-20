import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import sys
import os

def initialize_parameters(n_features):
    W = np.zeros((n_features, 1))
    b = 0
    return W, b

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def logistic_regression(X, W, b):
    z = np.dot(X, W) + b
    return sigmoid(z)

def scale_df(df_dropped):
	scaler = StandardScaler()
	df_scaled = scaler.fit_transform(df_dropped)
	df_scaled = pd.DataFrame(df_scaled, columns=df_dropped.columns)
	return df_scaled

def update_parameters(learning_rate, W, b, dw, db):
    W -= learning_rate * dw
    b -= learning_rate * db
    return W, b

def parse_weights(value):
    try:
        clean_value = value.replace('\n', '').replace('[', '').replace(']', '').strip()
        array = np.fromstring(clean_value, sep=' ').reshape(-1, 1)
        return array
    except Exception as e:
        return None

def read_model_weights(sys):
    model_weights = pd.read_csv(sys.argv[1])
    model_weights = model_weights.drop(columns=['Unnamed: 0'])
    model_weights['W'] = model_weights['W'].apply(parse_weights)
    return model_weights

def check_file_err_train(sys):
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

def check_file_err_predict(sys):
    if len(sys.argv) != 3:
        print("Error: Programm needs exactly 2 arguments!")
        sys.exit(1)
    if not sys.argv[1].endswith('.csv') or not sys.argv[2].endswith('.csv'):
        print("Error: The input file must be a .csv file!")
        sys.exit(1)
    if os.path.exists(sys.argv[1]) == 0 or os.path.exists(sys.argv[2]) == 0:
        print(f"Error: The file '{sys.argv[1]}' or the file is '{sys.argv[2]}' does not exist!")
        sys.exit(1)
    if os.path.getsize(sys.argv[1]) == 0 or os.path.getsize(sys.argv[2]) == 0:
        print(f"Error: The file '{sys.argv[1]}' or the file is '{sys.argv[2]}' empty!")
        sys.exit(1)


import pandas as pd
import numpy as np
import json
import sys

def load_models(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    features = data['features']
    mean_train = pd.Series(data['mean_train'])
    std_scaled = pd.Series(data['std_scaled'])
    models = {house: np.array(weights) for house, weights in data['models'].items()}
    return models, features, mean_train, std_scaled

def preprocess_test_data(df, features, mean_train, std_scaled):
    test_data = df[features].copy()
    test_data = test_data.fillna(mean_train)
    test_data_standardized = (test_data - mean_train) / std_scaled
    test_data_standardized = np.hstack([np.ones((test_data_standardized.shape[0], 1)), test_data_standardized])
    return test_data_standardized

def sigmoid(z):
    return 1 / (1 + np.exp(-z))
    
def predict(models, test_data):
    probabilities = {}
    for house, weights in models.items():
        z = test_data.dot(weights)
        probabilities[house] = sigmoid(z)
    prob_df = pd.DataFrame(probabilities)
    predictions = prob_df.idxmax(axis=1)
    return predictions

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: logreg_predict.py dataset_test.csv weights.json")
        sys.exit(1)
    test_file, weights_file = sys.argv[1], sys.argv[2]
    models, features, mean_train, std_scaled = load_models(weights_file)
    df_test = pd.read_csv(test_file)
    test_data = preprocess_test_data(df_test, features, mean_train, std_scaled)
    predictions = predict(models, test_data)
    output = pd.DataFrame({'Index': df_test['Index'], 'Hogwarts House': predictions})
    output.to_csv('houses.csv', index=False)

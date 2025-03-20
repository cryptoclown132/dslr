
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../ex3')))
from utils import *

def gradient_descent(train_data, labels, learning_rate, iterations):
	weights = np.zeros(train_data.shape[1])
	
	for _ in range(iterations):
		rand_idx = np.random.randint(0, train_data.shape[0])
		
		z = train_data[rand_idx, :].dot(weights)
		predictions = sigmoid(z)
		gradients = train_data[rand_idx, :].T.dot(predictions - labels[rand_idx])
		weights -= learning_rate * gradients
	return weights

def train_models(train_data, labels):
    models = {}
    for house in labels.columns:
        weights = gradient_descent(train_data, labels[house], 0.1, 500)
        models[house] = weights
    return models

if __name__ == "__main__":
	train_data, labels, features, mean_train, std_scaled = get_data()
	models = train_models(train_data, labels)
	save_models(models, features, mean_train, std_scaled, 'weights.json')

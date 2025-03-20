
from utils import *

def gradient_descent(train_data, labels, learning_rate, iterations):
	num_samples, num_features = train_data.shape
	weights = np.zeros(num_features)

	for _ in range(iterations):
		z = train_data.dot(weights)
		predictions = sigmoid(z)
		gradients = train_data.T.dot(predictions - labels) / num_samples
		weights -= learning_rate * gradients
	return weights

def train_models(train_data, labels):
    models = {}
    for house in labels.columns:
        weights = gradient_descent(train_data, labels[house], 0.1, 150)
        models[house] = weights
    return models

if __name__ == "__main__":
	train_data, labels, features, mean_train, std_scaled = get_data()
	models = train_models(train_data, labels)
	save_models(models, features, mean_train, std_scaled, 'weights.json')

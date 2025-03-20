import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../ex3')))
from utils import *

def	get_batch_pos(batch_idx, batches_per_epoch, batch_size):
	epoch_batch_idx = batch_idx % batches_per_epoch
	start = epoch_batch_idx * batch_size
	end = start + batch_size
	return start, end

def	shuffle_train_data(num_samples, train_data, labels):
	shuffled_indices = np.random.permutation(num_samples)
	train_data_shuffled = train_data[shuffled_indices]
	labels_shuffled = labels[shuffled_indices]
	return train_data_shuffled, labels_shuffled

def get_mini_batch(batch_idx, batches_per_epoch, batch_size, train_data_shuffled, labels_shuffled):
	start, end = get_batch_pos(batch_idx, batches_per_epoch, batch_size)
	mini_batch = train_data_shuffled[start:end]
	batch_labels = labels_shuffled[start:end]
	return mini_batch, batch_labels

def calc_batches_per_epoch(num_samples, batch_size):
	batches_per_epoch = num_samples // batch_size
	if num_samples % batch_size != 0:
		batches_per_epoch += 1
	return batches_per_epoch

def gradient_descent(train_data, labels, learning_rate, iterations, batch_size):
	weights = np.zeros(train_data.shape[1])
	batches_per_epoch = calc_batches_per_epoch(train_data.shape[0], batch_size)

	for batch_idx in range(iterations):
		if batch_idx % batches_per_epoch == 0:
			train_data_shuffled, labels_shuffled = shuffle_train_data(train_data.shape[0], train_data, labels)
		mini_batch, batch_labels = get_mini_batch(batch_idx, batches_per_epoch, batch_size, train_data_shuffled, labels_shuffled)
		
		z = mini_batch.dot(weights)
		predictions = sigmoid(z)
		gradients = mini_batch.T.dot(predictions - batch_labels) / batch_size
		weights -= learning_rate * gradients
	return weights

def train_models(train_data, labels):
    models = {}
    for house in labels.columns:
        weights = gradient_descent(train_data, labels[house], 0.1, 200, 16)
        models[house] = weights
    return models

if __name__ == "__main__":
	train_data, labels, features, mean_train, std_scaled = get_data()
	models = train_models(train_data, labels)
	save_models(models, features, mean_train, std_scaled, 'weights.json')

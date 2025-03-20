#!/bin/bash

# python3 ex1/describe.py datasets/dataset_train.csv

# python3 ex2/histogram.py datasets/dataset_train.csv
# python3 ex2/scatter_plot.py datasets/dataset_train.csv
# python3 ex2/pair_plot.py datasets/dataset_train.csv

rm houses.csv weights.json

# python3 ex3/logreg_train.py datasets/dataset_train.csv

# python3 ex_bonus/logreg_mini_batch.py datasets/dataset_train.csv
# python3 ex_bonus/logreg_stoch.py datasets/dataset_train.csv

# python3 ex3/logreg_predict.py datasets/dataset_test.csv weights.json
# python3 evaluate.py

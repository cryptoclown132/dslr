import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

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

path = sys.argv[1]
df = pd.read_csv(path)

columns_to_drop = list(df.columns[:6]) + ['Arithmancy', 'Care of Magical Creatures', 'Potions', 'Astronomy']
df = df.drop(columns=columns_to_drop)

df.corr().to_csv('corr.csv')

pd.plotting.scatter_matrix(df, figsize=(5,5))
# plt.savefig(f"pair_plot.png")
plt.show(block=True)
plt.close()

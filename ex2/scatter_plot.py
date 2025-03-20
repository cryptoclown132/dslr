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

x = df['Defense Against the Dark Arts']
y = df['Astronomy']

plt.scatter(x, y)
# plt.savefig(f"{course}_histogram.png")
plt.show(block=True)

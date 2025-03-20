import numpy as np
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

df = pd.read_csv(sys.argv[1])
df.drop(columns=['Index'], inplace=True)
houses = df['Hogwarts House'].unique()

datasets = [group for _, group in df[['Hogwarts House'] + list(df.select_dtypes(include=['number']).columns)].groupby('Hogwarts House')]

def get_count(course_values):
    count = 0
    for i in range(len(course_values)):
        if pd.isna(course_values[i]) == False:
            count += 1
    return count

def get_min(column):
    min_val = float('inf')
    for value in column:
        if pd.isna(value) == False:
            if value < min_val:
                min_val = value
    return min_val

def get_max(column):
    max_val = float('-inf')
    for value in column:
        if pd.isna(value) == False:
            if value > max_val:
                max_val = value
    return max_val

def get_mean_percentage(course_values, course):
    sum = 0
    for i in range(len(course_values)):
        if pd.isna(course_values[i]) == False:
            sum += course_values[i]
    mean_value = sum / get_count(course_values)
    min_val = get_min(df[course].values)
    return (mean_value - min_val) / (get_max(df[course].values) - min_val)

course_house_average = pd.DataFrame()
course_house_average = datasets[0].head(0).copy()

for i in range(4):
    new_row = {}
    for course in datasets[i].columns:
        if course != 'Hogwarts House':
            course_values = datasets[i][course].values
            new_row [course] = get_mean_percentage(course_values, course)
        else:
            new_row [course] = datasets[i]['Hogwarts House'].iloc[0]
    course_house_average.loc[i] = new_row



categories = course_house_average.columns[1:]
houses = course_house_average['Hogwarts House']


#one histogram

x = np.arange(len(categories)) * 1.4
width = 0.2

fig, ax = plt.subplots(figsize=(14, 8))

for i, house in enumerate(houses):
    ax.bar(x + i * width, course_house_average.iloc[i, 1:] * 100, width, label=house)

ax.set_xlabel('Courses', fontsize=14)
ax.set_ylabel('Relative Scores in %', fontsize=14)
ax.set_title('Relative Scores in Percent by Hogwarts House of each Course', fontsize=20)
ax.set_xticks(x + (len(houses) - 1) * width / 2)

ax.set_xticklabels(categories, rotation=90)

ax.set_ylim(0, 100)

ax.legend(title='Hogwarts House')

plt.tight_layout(pad=4)
# plt.savefig(f"{course}_histogram.png")
plt.show()


#multiple histograms

# width = 0.5

# for course in categories:
#     fig, ax = plt.subplots(figsize=(4, 3))

#     scores = course_house_average[course] * 100

#     for i, house in enumerate(houses):
#         ax.bar(i, scores.iloc[i], width, label=house)

#     ax.set_xlabel('Houses', fontsize=11)
#     ax.set_ylabel('Relative Scores in %', fontsize=11)
#     ax.set_title(f'Relative Scores for {course}', fontsize=14)
#     ax.set_xticks(range(len(houses)))
#     ax.set_xticklabels(houses, rotation=45)

#     ax.set_ylim(0, 100)


    # plt.tight_layout()
#     # plt.savefig(f"{course}_histogram.png")
    # plt.show()

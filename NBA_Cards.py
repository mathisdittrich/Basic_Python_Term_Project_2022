
# import libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# read the data
df = pd.read_csv('./Data/Player_Information.csv', index_col=0)

# Was geeht ab

print(df.head)


'''
# 1.)
# The function should compute the most common type combination of the given dataset.
most_common_types = df.groupby('Type 1')['Type 2'].value_counts().idxmax()

# 2.1 & 2.3
# creating new counts column and sort it
count_types = df[['Type 1','Type 2']].value_counts().reset_index(name='counts')

# 2.2
# add Combination Column
count_types["Types"] = count_types["Type 1"] + "_" + count_types["Type 2"]

# 2.4
# only first 12 columns
subset_count_types = count_types[:12]
# print(subset_count_types)

# 2.5
# Plot the dataset from section 2.4 with Horizontal Barplot using the created column types in section 2.2
plt.rcdefaults()
fig, ax = plt.subplots()
y_pos = np.arange(12)

ax.barh(y_pos, subset_count_types["counts"], align='center')
ax.set_yticks(y_pos, labels= subset_count_types["Types"])
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Counts')
ax.set_title('Most common type combinations')

plt.show()

# 3.
# Using the original Pokemon dataset. make a Scatterplot of their attack and defense.

# print(df.head(20))

# Create data
colors = (0,0,0)
area = np.pi*3

# Plot
plt.scatter(df["Attack"], df["Defense"], s=area, c=colors, alpha=0.5)
plt.xlabel('Attack')
plt.ylabel('Defence')
plt.show()


# 4. (Bonus)
# How speed of Pokemon relates to various base factors? (Speed vs Attack & Speed vs Defense) use subploting 
# Note: The Speed on both x-axis should be the same.


f = plt.figure()    
f, axes = plt.subplots(nrows = 1, ncols = 2)

axes[0].scatter(df["Speed"], df["Defense"], c=colors, alpha=0.5)
axes[0].set_xlabel('Speed-Defense-Relation', labelpad = 5)

axes[1].scatter(df["Speed"], df["Attack"], c=colors, alpha=0.5)
axes[1].set_xlabel('Speed-Attack-Relation', labelpad = 5)

plt.show()

'''
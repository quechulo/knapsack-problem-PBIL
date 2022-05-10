import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random

random.seed(0)

def generateData(count=5, cor=False):
    data = []
    licz = 2
    if cor is False:
        for x in range(0, count):
            tmp = []
            for j in range(1, 3):
                tmp.append((licz+random.randint(-1, 8)) % 23)
                licz = random.randint(1, 5)
            data.append(tmp)
    else:
        for x in range(0, count):
            tmp = []

            tmp.append(licz + random.randint(1, 3))
            tmp.append(abs(licz + random.randint(-2, 3)))
            licz += random.randint(1, 3)
            licz = licz % 20
            data.append(tmp)

    df = pd.DataFrame(data)
    return df

### USAGE ###
df = generateData(20, True)
print(df)

# Correlation between different variables
#
corr = df.corr(method='spearman')
print(corr)
#
# Set up the matplotlib plot configuration
#
# f, ax = plt.subplots(figsize=(10, 10))
#
# Generate a mask for upper traingle
#
mask = np.triu(np.ones_like(corr, dtype=bool))
#
# Configure a custom diverging colormap
#
cmap = sns.diverging_palette(230, 20, as_cmap=True)
#
# Draw the heatmap
#
sns.heatmap(corr, annot=True, mask=mask, cmap=cmap)
plt.show()
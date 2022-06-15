import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
import numpy as np
from matplotlib.pyplot import scatter

np.random.seed(10)

def generateItems(num_of_items=5, cor=False):
    if cor is False:
        corr = 0.01  # correlation
    else:
        corr = 0.9  # correlation
    xx = np.array([1, 50])
    yy = np.array([2, 10])
    means = [xx.mean(), yy.mean()]
    stds = [xx.std() / 3, yy.std() / 3] # tutaj można podzielić obie przez 3 `/ 3` wtedy nie ma ujemnych

    covs = [[stds[0] ** 2, stds[0] * stds[1] * corr],
            [stds[0] * stds[1] * corr, stds[1] ** 2]]

    m = np.random.multivariate_normal(means, covs, num_of_items).T
    scatter(m[0], m[1])
    plt.show() # print distribution of generated items

    df = pd.DataFrame(m)
    df = df.T[[1,0]] # swap order of columns to [weight; value]
    df[0] = df[0].astype('int')
    df[1] = df[1].astype('int')
    df = df.values.tolist()
    return df


if __name__ == "__main__":
    ### USAGE ###
    df = generateItems(100, True)
    print(df)

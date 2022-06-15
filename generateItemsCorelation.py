import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
import numpy as np
from matplotlib.pyplot import scatter

# random.seed(0)

def generateItems(num_of_items=5, cor=False):
    if cor is False:
        corr = 0.01  # correlation
    else:
        corr = 0.9  # correlation
    xx = np.array([0.1, 50.0])
    yy = np.array([0.1, 1.0])
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
    df[1] = df[1].round(2)
    df = df.values.tolist()
    return df


if __name__ == "__main__":
    ### USAGE ###
    df = generateItems(100, True)
    print(df)

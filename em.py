from scipy.stats import multivariate_normal
import pandas as pd
import numpy as np


# Calculate cluster probabilities(hidden-matrix) from data, means, and STDs
def expectation(parameters_df, clusters):
    for cluster in clusters:
        mus = np.array([mu for mu in cluster.mus])
        sigs = np.diag(np.array([sig for sig in cluster.sigs]), 0)
        cluster.probabilities = parameters_df.apply(lambda x: multivariate_normal.pdf(x, mean=mus, cov=sigs), axis=1)


# calculate means and STDs from hidden-matrix(probabilities) and data
def maximization(parameters_df, clusters):
    joint = pd.DataFrame()
    for i in range(len(clusters)):
        joint = pd.concat([joint, clusters[i].probabilities.rename(i)], axis=1)

    # Assign each row to a cluster
    

    return


def maximum_likelyhood_expectation(parameters_df, clusters_df):
    return

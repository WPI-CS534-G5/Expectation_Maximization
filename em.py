from __future__ import division
from scipy.stats import multivariate_normal
from math import log
import pandas as pd
import numpy as np


# Calculate cluster probabilities(hidden-matrix) from data, means, and STDs
def expectation(parameters_df, clusters):
    # Get Probabilities per cluster
    for cluster in clusters:
        # Calculate multivariate normal pdf for each point and get its probability
        mvn = multivariate_normal(mean=cluster.mus, cov=cluster.sigmas)
        cluster.probabilities = parameters_df.apply(lambda x: mvn.pdf(x), axis=1)


# Assign each row (point) to a cluster
def assign_clusters(clusters):
    # Joint Cluster Probabilities into DataFrame
    joint = pd.DataFrame()
    for i in range(len(clusters)):
        joint = pd.concat([joint, clusters[i].probabilities.rename(i)], axis=1)

    # Assign each row to a cluster
    for row_i in range(len(joint)):
        max_i = pd.Series.idxmax(joint.iloc[row_i])
        row = joint.iloc[1]

        for col_i in range(len(row)):
            if col_i == max_i:
                joint[col_i][row_i] = 1
            else:
                joint[col_i][row_i] = 0

    return joint


# calculate means and STDs from hidden-matrix(probabilities) and data
def maximization(parameters_df, clusters, hm):
    # Get offset of Hidden-Matrix for use in Joint DataFrame
    offset = len(parameters_df.columns)

    # Calculate MEANs and STDs of points for every cluster
    for cluster_i in range(len(clusters)):
        # Indices of cluster points
        m = hm[cluster_i]
        indices = m[m == 1].index
        cluster = parameters_df.filter(indices, axis=0)

        # Assign New MEANs and STDs
        if not cluster.empty:
            c = cluster.iloc[:, :offset]
            clusters[cluster_i].sigmas = np.array(c.cov())
            clusters[cluster_i].mus = np.array(c.mean())
        else:
            print '# ####### cluster is empty ####### #'

    return


def maximum_likelyhood_expectation(clusters, hm):
    # Joint cluster probabilities and cluster assignments
    joint = pd.DataFrame()  # type: pd.DataFrame
    for i in range(len(clusters)):
        joint = pd.concat([joint, clusters[i].probabilities.rename(i)], axis=1)

    # Get Probability of each cluster
    pi_c = list()
    total_points = len(hm)
    for label in hm:
        cluster_probabilities = hm[label]
        pi_c.append(sum(cluster_probabilities) / total_points)

    # Calculate Log Likelihood
    total = 0
    for index, row in joint.iterrows():
        current = 0

        # Calculate log( P(x_i) )
        for i in range(len(pi_c)):
            current += pi_c[i] * row[i]  # Add cluster-probability[i] * point-probability[i]

        # Add point probability if > 0
        if not current == 0:
            total += log(current)

    return total


# Iterates EM until convergence of Log-Likelihood
def em(df, clusters):
    # Iterate E-M until convergence of Log-Likelihood
    ll = 0
    while True:
        # Expectation - generate hidden matrix
        expectation(df, clusters)

        # Assign points to clusters (get hidden matrix)
        hm = assign_clusters(clusters)  # type: pd.DataFrame

        # Maximization - generate new MEANs and STDs
        maximization(df, clusters, hm)

        # Maximum Likelyhood Expectation
        new_ll = maximum_likelyhood_expectation(clusters, hm)

        # Check for convergence of LL
        if abs(new_ll - ll) < 0.0001:
            break

        ll = new_ll

    return ll

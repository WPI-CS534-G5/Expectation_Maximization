import random
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


class Cluster(object):
    """docstring for Cluster."""
    def __init__(self, mus=None, sigmas=None, probabilities=None, cp=None):
        self.cp = cp
        self.mus = mus
        self.sigmas = sigmas
        self.probabilities = probabilities


# Initialize Sigs and Mus from data read
def initialize_clusters(clusters, parameters_df):
    num_points = len(parameters_df)
    stds = np.diag(parameters_df.std())

    for cluster_i in range(len(clusters)):
        row_i = random.randint(0, num_points) % num_points
        row = np.array(parameters_df.iloc[row_i])  # type: pd.Series

        clusters[cluster_i].mus = row
        clusters[cluster_i].sigs = stds


# !! For Two Dimensional Data Only - No Size Checks Here !!
# Print Data-Points and Cluster Centers
def print_clusters(df, clusters):
    plt.scatter(df[0], df[1], marker='.', color='blue')  # Plot Points

    # Plot Cluster Centers
    for i in range(len(clusters)):
        cluster = clusters[i]  # type: cl.Cluster
        plt.scatter(cluster.mus[0], cluster.mus[1], marker=',', color='red')
    plt.show()


# Print Debug Information on Clusters
def print_info(clusters, ll, bic=None):
    num_clusters = len(clusters)
    print 'Number of Clusters:', num_clusters
    for cluster_i in range(len(clusters)):
        cluster = clusters[cluster_i]
        print 'Cluster[' + str(cluster_i) + ']: MEANs = ', cluster.mus
        print 'Cluster[' + str(cluster_i) + ']: STDs  = ', np.diagonal(cluster.sigs)
    print 'Log-Likelihood:', ll
    if bic:
        print 'BIC-Value:', bic
    print '\n\n'
import em
import cluster as cl
from math import log


# Random Restarts on EM
def em_random_restarts(num_restarts, num_clusters, parameters_df):
    ll = None
    clusters = None

    for i in range(num_restarts):
        # Initialize cluster statistics
        new_clusters = [cl.Cluster() for j in range(num_clusters)]
        cl.initialize_clusters(new_clusters, parameters_df)

        # Run EM & Get LL Value
        new_ll = em.em(parameters_df, new_clusters)

        # Save Best LL Value and its clusters
        if ll is None or new_ll > ll:
            ll = new_ll
            clusters = new_clusters

    return ll, clusters


# Bayesian Information Criterion Wrapper
def bayesian_information_criterion(parameters_df):
    nc = 1
    num_points = len(parameters_df)

    ll = None
    bic = None
    clusters = None
    while True:
        # Get Best Values For Current #of Clusters
        new_ll, new_clusters = em_random_restarts(10, nc, parameters_df)

        # Calculate BIC of Clustering
        k = 5 * nc - 1
        new_bic = (log(num_points) * k) - (2 * new_ll)
        cl.print_info(new_clusters, new_ll, new_bic)

        # Check for convergence of BIC
        if bic is not None and new_bic > bic:
            return ll, bic, clusters
        else:
            nc += 1
            ll = new_ll
            bic = new_bic
            clusters = new_clusters






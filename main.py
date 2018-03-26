import em
import pandas as pd
import cluster as cl

# Setup
filename = "sample EM data v2_labeled.csv"
df = pd.read_csv(filename)
num_iterations = 100

# Initialize cluster statistics
num_clusters = 3
clusters = pd.Series([cl.Cluster() for i in range(num_clusters)])


for i in range(num_iterations):
    # Expectation - generate hidden matrix
    em.expectation(df, clusters)

    # Maximization - generate new MEANs and STDs
    em.maximization(df, clusters)

    # Maximum Likelyhood Expectation
    em.maximum_likelyhood_expectation(df, clusters)





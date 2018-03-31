import pandas as pd
from sklearn import datasets as ds
from matplotlib import pyplot as plt


# Create Clusters
num_clusters = 3
num_samples = 1000
standard_dev = 4.0

blob = ds.make_blobs(n_samples=num_samples, centers=num_clusters, cluster_std=standard_dev)
data = blob[0]
clusters = pd.Series(blob[1])

# Put into DataFrame
df = pd.DataFrame(data)
df = pd.concat([df, pd.Series(blob[1])], axis=1)  # type: pd.DataFrame
df.columns = ['x', 'y', 'c']

# Plot Points
colors = ['red', 'green', 'blue', 'yellow']
for i in range(num_clusters):
    cluster = df[df.c == i]
    plt.scatter(cluster.x, cluster.y, marker='.', color=colors[i])
plt.show()

# Ask to Save Data Points to File
filepath = 'data/generated_data.csv'
filepath_labeled = 'data/generated_data_labeled.csv'
df.to_csv(filepath_labeled, columns=['x', 'y', 'c'], index=False)  # Labeled Data
df.to_csv(filepath, columns=['x', 'y'], index=False, header=False)  # Unlabeled Data

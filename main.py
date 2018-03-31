import time
import pandas as pd
from cluster import print_info

import settings
import em_wrapper as emw

start_time = time.time()


# Setup environment variables
file_path, nc, run_bic = settings.init_env()
df = pd.read_csv(file_path, header=None)
num_dimensions = df.shape[1]


# Run E w||w/o BIC
ll = None
bic = None
clusters = None
if run_bic:
    ll, bic, clusters = emw.bayesian_information_criterion(df)
else:
    ll, clusters = emw.em_random_restarts(10, nc, df)


# Print Results
print '# ####### Final Result ####### #'
print_info(clusters, ll, bic)
print 'Total Time:', time.time() - start_time, 'seconds'

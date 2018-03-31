from sys import argv

# ToDo: Check if file exists
# ToDo: Check if nc is numeric before casting


def init_env():
    if len(argv) is not 3:
        print 'Usage: $main.py [file-name] [#-clusters]'
        exit(1)

    # Set Variables From ARGV
    filepath = argv[1]
    num_clusters = argv[2]

    # Set USE_BIC Flag
    run_bic = False
    if num_clusters == 'X':
        run_bic = True
    else:
        num_clusters = int(num_clusters)

    return filepath, num_clusters, run_bic

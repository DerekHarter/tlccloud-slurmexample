#! /usr/bin/env python3
#
# Example of multicore shared memory training.  This script trains a RandomForestClassifier
# of 500 random trees using 1, 2, 4, 8 and 16 cores.  We time how long it takes to
# fit the classifier in each case and display the results.  This script uses
# scikit-learn `n_jobs` metaparameter and assumes that the number of specified cpus/cores are
# available for training when the script is run.
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from time import time

n_cores = [1, 2, 4, 8, 16]
n_samples = 10000
n_estimators = 1000

def main():
    """Main entry point, this script simply runs loop to create model and fit it with
    different number of cores/n_jobs each iteration of the loop
    """
    X, y = make_classification(n_samples=n_samples, n_features=20, n_informative=15, n_redundant=5, random_state=3)

    for n in n_cores:
        # define a model, n_jobs determines degree of multi-core parallelism
        model = RandomForestClassifier(n_estimators=n_estimators, n_jobs=n)
        
        # record start time
        print('-' * 60)
        print('Train RandomForest n_estimators=%d using n=%d cpu cores' % (n_estimators, n))
        start = time()

        # fit the model
        model.fit(X, y)

        # record the end time
        end = time()

        # report execution time needed to fit the model
        total_time = end - start
        print('Fit using %d cpu/core total time: %.5f secs' % (n, total_time))
    
    
if __name__ == "__main__":
    main()

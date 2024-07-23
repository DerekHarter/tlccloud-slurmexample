# Shared Memory / Multicore Jobs: A job that uses multiple cores on a single machine

One common type of parallel excution are jobs that make use of multiple cpu cores running
on the same machine, all within the same memory address space.  Many types of scientific
computing applications and libraries have mutti-core shared memory modes of execution.

## `scikit-learn` Multi-core Training Example

For example, the `scikit-learn` Python scientific library allows for multi-core
parallel execution of many fit/train versions of algorithms in the library.  This is 
usually done (when supported) by specifying the `njobs=n` parameter when creating
a `scikit-learn` object that will be fit to a set of data.  Read the following
for more examples of using `njobs` for multicore training in `scikit-learn` see the
additional resources.

Some `scikit-learn` models can make use of multi-core parallelism when fitting or training
a model.  As a simple example, a `RandomForestClassifier` is simply a collection of `N`
random trees, and each tree that makes up the forest can be trained/fitted independently using
a separate cpu core.

The file `randomforest-example.py` defines and trains a `RandomForestClassifier` on a set of randomly generated data.
The model is first fit and timed on a single cpu core, ehtn the same model is fit using all available
cpu cores.

The file `randomforest-example.sh` can be used to submit a batch job to run the example.  It requests 16 cpu cores
(the maximum available currently on TLC compute nodes) and runs the example.  By using `n_jobs=16` for the
second training example, it will make use of all cores allocated for this job that we request in the batch
script using `--cpus-per-task=16` lines.  Adjust for the number of cpus/cores as needed.

You can submit the batch job for this example python multi-core training by executing:

```
$ sbatch random-forest-example.sh
```

NOTE: it is not good practice to request 16 cores but have parts of your job only using 1, 2, 4 cores, etc.
as in this example.  Try not to request cores, memory, gpus or any resource that you do not end up using
in a batch job.





## Additional Resources

- [Multi-Core Machine Learning in Python with Scikit-Learn](https://machinelearningmastery.com/multi-core-machine-learning-in-python/)

# Getting Information about the Slurm Batching System

The following is a list of all of the major command line slurm commands that are available in a slurm
batching system (taken from the [Slurm Workload Manager Quick Start User Guide](https://slurm.schedmd.com/quickstart.html):

- `sacct` is used to report job or job step accounting information about active or completed jobs.
- `salloc` is used to allocate resources for a job in real time. Typically this is used to allocate resources and spawn a shell. The shell is then used to execute srun commands to launch parallel tasks.
- `sattach` is used to attach standard input, output, and error plus signal capabilities to a currently running job or job step. One can attach to and detach from jobs multiple times.
- `sbatch` is used to submit a job script for later execution. The script will typically contain one or more srun commands to launch parallel tasks.
- `sbcast` is used to transfer a file from local disk to local disk on the nodes allocated to a job. This can be used to effectively use diskless compute nodes or provide improved performance relative to a shared file system.
- `scancel` is used to cancel a pending or running job or job step. It can also be used to send an arbitrary signal to all processes associated with a running job or job step.
- `scontrol` is the administrative tool used to view and/or modify Slurm state. Note that many scontrol commands can only be executed as user root.
- `sinfo` reports the state of partitions and nodes managed by Slurm. It has a wide variety of filtering, sorting, and formatting options.
- `sprio` is used to display a detailed view of the components affecting a job's priority.
- `squeue` reports the state of jobs or job steps. It has a wide variety of filtering, sorting, and formatting options. By default, it reports the running jobs in priority order and then the pending jobs in priority order.
- `srun` is used to submit a job for execution or initiate job steps in real time. srun has a wide variety of options to specify resource requirements, including: minimum and maximum node count, processor count, specific nodes to use or not use, and specific node characteristics (so much memory, disk space, certain required features, etc.). A job can contain multiple job steps executing sequentially or in parallel on independent or shared resources within the job's node allocation.
- `sshare` displays detailed information about fairshare usage on the cluster. Note that this is only viable when using the priority/multifactor plugin.
- `sstat` is used to get information about the resources utilized by a running job or job step.
- `strigger` is used to set, get or view event triggers. Event triggers include things such as nodes going down or jobs approaching their time limit.
- `sview` is a graphical user interface to get and update state information for jobs, partitions, and nodes managed by Slurm.

Of these, the ones you will use the most to start up jobs are `sbatch`
and `srun`, which you will see examples of usage in this guide.  The
`scancel` may be needed occassionally by you to cancel a job that you
start that is a mistake or is having problems and you want to fix and
restart it.

## `sinfo` command

You can use the `sinfo` command to get information about the current nodes, states
and resources available in the cluster.

```
user@slurmctl:~$ sinfo
PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST
debug*       up   infinite     32   idle slurm[01-31],slurm-gpu01
```

This shows available partitions that you can submit jobs on, and the nodes
and state of nodes in those partitions.

You can get more detailed information about resources using flags for `sinfo`.
For example to list memory and gpu resources available on nodes do:

```
user@slurmctl:~$ sinfo -o "%20N %10c %10m %10G"
NODELIST             CPUS       MEMORY     GRES      
slurm-gpu01          16         32517      gpu:5     
slurm[01-31]         16         9940+      (null)    
```

## `squeue` command

The `squeue` command can be used to list all jobs that are running
or are waiting on / pending resources in the slurm batching system.

```
user@slurmctl:~$ squeue
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)

```

Often you may only want to see your own current and pending jobs, rather than all jobs running
by you and other users:

```
user@slurmctl:~$ squeue -u user
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
```

The reason jobs are not running may simply be that available resoures are not available yet, e.g.
all nodes are busy.  But at times jobs can get stuck, and the reason codes will give an indication
of the issue of why the job cannot be allocated to run on any nodes.

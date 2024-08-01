# Interactive `srun` Resource Allocation: Allocating and using slurm resources interactively

We have mostly given examples in this tutorial of running jobs using the batching system
and the `sbatch` command.  In this model of computation, the job is submitted to a queue and
once all resources requested are available, they are allocated and the job is run on the
node(s) with the resources asked for.

We can use the `srun` command in a slurm cluster to obtain resources and use them interactively.
`srun` will actually not start the interactive session until resources are available to do so,
so executing `srun` is not guaranteed to start immediately.

The most common use case for using `srun` is to obtain a set of nodes and resources so that
you can test interactively resource usage needs for a program or simulation being developed.

Another common use case, that we will describe here, is to obtain a gpu (or multiple
gpu) resources that we can use interactively.  We will often run a Jupyter Lab
server on the obtained session, and then develop using Jupyter notebooks our code.

# Single gpu Allocation using `srun`

For example, to obtain an interactive bash shell with an allocated gpu on the TLC slurm
we would do the following:

```
(base) user@slurmctl:~$ srun --gres=gpu:1 --pty bash
(base) user@slurm-gpu01:~$ 
```

A couple of things to note from the prompt here.  This invocation of `srun` returned a new
`bash` shell session.  The session was allocated 1 gpu and is running on the host
`slurm-gpu01`.  You may need to verify the host and the gpu or other resources are
allocated to this session.  For example:

```
(base) user@slurm-gpu01:~$ squeue
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
             23282     debug     bash     user  R       1:10      1 slurm-gpu01
(base) user@slurm-gpu01:~$ hostname
slurm-gpu01
(base) user@slurm-gpu01:~$ echo $CUDA_VISIBLE_DEVICES
0
```

We are job 23282 in this example running on the `slurm-gpu01` node.  We were allocated 1 gpu
resources as requested.  The `$CUDA_VISIBLE_DEVICES` environment variable confirms that
we are using gpu device id 0 in this session.  This environment variable is used
by TensorFlow and PyTorch libraries to determine which gpu devices to use when running
jobs.

We would like to use this gpu resource in a jupyter notebook session.  As shown in
previous tutorials, we will first enable an appropriate conda environment to use.
The conda environment has already had the jupyter lab and needed tools installed
into it.  We then start a jupyter lab notebook to serve itself on port 9099

```
(base) user@slurm-gpu01:~$ conda activate keras-tf-gpu
(keras-tf-gpu) user@slurm-gpu01:~$ jupyter-lab --no-browser --port 9099
.
.
.
[I 2024-08-01 14:37:03.894 ServerApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 2024-08-01 14:37:03.937 ServerApp] 
    
    To access the server, open this file in a browser:
        file:///home/user/.local/share/jupyter/runtime/jpserver-22214-open.html
    Or copy and paste one of these URLs:
        http://localhost:9099/lab?token=786f9f532729d14434687c0699079d5d499e55180044324d
        http://127.0.0.1:9099/lab?token=786f9f532729d14434687c0699079d5d499e55180044324d

```

This shows that we have started a jupyter lab server and it is running and being served over http on the localhost
at port 9099.  Notice also that a token was generated that we need to use to access this jupyter lab server.

This terminal session is now no longer available, as it is running the jupyter lab server.  So to access the running
jupyter lab we need to do some ssh magic to create a tunnel to the port on `slurm-gpu01` that we can
connect to.  Run something like the following in a new terminal session from your local machine:

```
user@yourmachine:~$ ssh -t -t user@slurm.tlc.pro -L 7077:localhost:8088 ssh slurm-gpu01 -L 8088:localhost:9099
```

This looks a bit complicated/magical.  To explain a bit, on your laptop or local machine we are performing an
`ssh` session to the `slurm.tlc.pro` machine, as you normally do to log in.  But the first -L option specifies 
to `ssh` to open up a tunnel that is at port 7077 on `yourmachine` and ends at port 8088 on the `slurmctl`
machine.  But from there we use `ssh` again to open up yet another tunnel.  This tunnel connects the
port 8088 to the port 9099 on the `slurm-gpu01` machine.  In this example your port number needs to match what
you choose when starting the jupyter lab server.  And the hostname and your user name may differ, e.g. since
we were allocated a gpu on `slurm-gpu01`, that needs to be the target of the second tunnel we create.

If this works, you will actually have a running ssh session to `slurm-gpu01`.  But more importantly the
port 7077 should be tunneled to connect to the running jupyter lab on `slurm-gpu01` that was
allocated the gpu to use.  On `yourmachine` open a browser and navigate to 

http://127.0.0.1:7077

to access the jupyter lab server.  If you are using jupyter lab, you may need to copy/paste the authentication
token that will be displayed in the original session when you started jupyter lab in order to log in.
This token was shown in the output above when starting jupyter lab (it will be a different token each time
you run).  You can alternatively copy the url you get, just changing the port number to 7077 that you
tunnelled to on your local host.

The iPython notebook named `gpu-test.ipynb` in this directory can be used from a Jupyter lab
server to test gpu resource allocation.  If you run this, it should correctly show that you have 1
gpu allocated, the the gpu id should correspond to the one set in the `CUDA_VISIBLE_DEVICES`
environment variable given to you.  This notebook first trains models using only the cpu, and then
switches to training on the allocated gpu so that you can compare performance between using cpu
vs. using gpu.


## Multiple gpu Allocation Example

You can allocate and use multiple gpus on the same node in a very similar manner.  For example, here we
request 5 gpus on a single node:

```
(base) user@slurmctl:~$ srun --gres=gpu:5 --pty bash
(base) user@slurm-gpu01:~$ squeue
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
             23283     debug     bash     user  R       0:05      1 slurm-gpu01
(base) user@slurm-gpu01:~$ hostname
slurm-gpu01
(base) user@slurm-gpu01:~$ echo $CUDA_VISIBLE_DEVICES
0,1,2,3,4

```

In this case the `CUDA_VISIBLE_DEVICES` should be a list of the allocated
and visible gpus that were obtained by this slurm `srun` request.

You can use the file named `multigpu-test.ipynb` for an example of a strategy to
train and use multiple gpus.  This example first trains models on 1 gpu and then
trains using all available gpus to compare performance.

## NOTE: Release Interactive Resources

Anytime you use `srun` to allocate resoures in the slurm cluster, make sure that as soon as you are
done testing things or using a Jupyter lab notebook, that you immediately close and exit out of
the bash session you obtained from the `srun` request.  Exiting the bash shell session will signal
to slurm that the resources are not longer being used and will return them to slurm to be allocated
to others.  Users who abuse cluster resources, by for example not exiting out of interactive bash
sessions when finished with them, may have limits put on their accounts in terms of time or types
of resources yu can use.

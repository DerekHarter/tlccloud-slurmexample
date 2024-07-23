#!/bin/bash
#SBATCH --job-name=randomforest
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=10G
#SBATCH --output=randomforest-%5A.out
echo "Compute node: `hostname`"
echo "Project directory: `pwd`"
echo "Start time: `date`"
start=$(date +%s)
source activate keras-tf-gpu
./randomforest-example.py
echo "End time: `date`"
end=$(date +%s)
secs=($end-$start)
echo "Elapsed time: $((secs/1)) seconds"
printf 'Elapsed time: %d:%02d:%02d\n' $((secs/3600)) $((secs%3600/60)) $((secs%60))

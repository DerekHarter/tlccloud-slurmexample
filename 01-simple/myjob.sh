#!/bin/bash
#SBATCH --partition=debug
#SBATCH --job-name=mjob
#SBATCH --mem=1G
#SBATCH --time=1-0:0
#SBATCH --output=myjob.slurm.log
hostname
date
echo 'Started myjob'
sleep 10
echo 'Finished myjob'
date

#!/bin/bash -l

#SBATCH -p debug
#SBATCH -N 64
#SBATCH -t 00:30:00
#SBATCH -J corr_north
#SBATCH -e sgc.error
#SBATCH -o north.out

echo `date`
cd $PBS_O_WORKDIR

module load gsl
srun -n 64 -c 24 /project/projectdirs/boss/npadmana/twopt/./do_smu.x /global/homes/w/wma/correlation/sgc.ini
echo `date`

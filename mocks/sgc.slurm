#!/bin/bash -l
#SBATCH -p debug
#SBATCH -N 64
#SBATCH -t 00:30:00
#SBATCH -J corr_north
#SBATCH -e sgc.error
#SBATCH -o sgc.$PBS_JOBID.out

echo `date`

cd $SLURM_SUBMIT_DIR

module load gsl
srun -n 64 -c 24 /project/projectdirs/boss/npadmana/twopt/./do_smu.x /global/homes/g/giusarma/correlation/sgc_north.ini
echo `date`
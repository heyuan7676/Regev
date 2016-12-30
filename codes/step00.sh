#!/bin/bash -l

#SBATCH --time 10:00:00
#SBATCH --nodes=2
#SBATCH --ntasks=10

cd /scratch0/battle-fs1/heyuan/train/Regiv_Glioblastoma/data/
wget -r --no-parent ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByStudy/sra/SRP/SRP042/SRP042161//SRR12953*


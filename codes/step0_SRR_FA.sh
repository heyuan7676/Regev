#!/bin/bash -l

#### 0. Transform SRR files to Regiv_Glioblastoma files

#SBATCH --time 10:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=10

REF_DIR=/scratch0/battle-fs1/heyuan/train/assembly
DATA_DIR=/scratch0/battle-fs1/heyuan/train/Regiv_Glioblastoma/fafiles
OUT_DIR=/scratch0/battle-fs1/heyuan/train/Regiv_Glioblastoma/alignments
RSEM_DIR=/scratch1/battle-fs1/tools_shared/RSEM-1.2.29
BT_DIR=/scratch1/battle-fs1/tools_shared/bowtie-1.1.2
LOGFILE=output.txt

[ -z "$DATA_DIR" ] && { echo "Need to set BASEDIR"; exit 1; }
[ -z "$BT_DIR" ] && { echo "Need to set Bowtie Dir"; exit 1;  }


#### 0. Transform SRR files to Regiv_Glioblastoma files

SRR_DIR=/scratch0/battle-fs1/heyuan/train/Regiv_Glioblastoma/data/ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByStudy/sra/SRP/SRP042/SRP042161
cd ${SRR_DIR}

mkdir ../used

for f in `ls`
do
    echo ${f}
    cd ${f}    
    fastq-dump -I --split-files -O ${DATA_DIR} ${f}
    cd ..
    mv ${f} ../used
done



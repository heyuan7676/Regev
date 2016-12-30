#!/bin/bash -l

#SBATCH --time 10:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=2


DATA_DIR=/scratch0/battle-fs1/heyuan/train/Regiv_Glioblastoma/fafiles
SRR_DIR=/scratch0/battle-fs1/heyuan/train/Regiv_Glioblastoma/data/ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByStudy/sra/SRP/SRP042

FILES=$(/bin/ls ${SRR_DIR}/SRP042161 | xargs -n1 basename)
IDS=${FILES//SRR/}

## find the maxmimum ID

max=0
for v in ${IDS[@]}; do
    if (( $v > $max )); then max=$v; fi; 
done
echo $max


## find the minimum ID

min=$max
for v in ${IDS[@]}; do
    if (( $v < $min )); then min=$v; fi;
done
echo $min

### Or you could directly define min, max and gap

min=1295360
max=1295366
gap=6


## submit the jobs for 20 datasets at one time

STARTID=${min}
while [ $STARTID -lt $max ]
do
    echo $STARTID
    sbatch step2_align_TPM.sh $STARTID $gap
    STARTID=$[$STARTID+$gap+1]
done


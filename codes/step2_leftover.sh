#!/bin/bash -l

#SBATCH --time 20:00:00
#SBATCH --nodes=2
#SBATCH --ntasks=10


FILE=$1
echo $FILE

REF_DIR=/scratch0/battle-fs1/heyuan/train/assembly
DATA_DIR=/scratch0/battle-fs1/heyuan/train/Regiv_Glioblastoma/fafiles
OUT_DIR=/scratch0/battle-fs1/heyuan/train/Regiv_Glioblastoma/alignments
RSEM_DIR=/scratch1/battle-fs1/tools_shared/RSEM-1.2.29
BT_DIR=/scratch1/battle-fs1/tools_shared/bowtie-1.1.2

[ -z "$DATA_DIR" ] && { echo "Need to set BASEDIR"; exit 1; }
[ -z "$BT_DIR" ] && { echo "Need to set Bowtie Dir"; exit 1;  }



#### 2. compute expression reads

FILES=$(/bin/ls ${DATA_DIR}/SRR1294*_1.fastq| xargs -n1 basename)
FILES=${FILES//_1.fastq/}

for F in ${FILES}
do
    echo ${F}
    start=`date +%s`

    sed -i "s:.1 : :g" ${DATA_DIR}/${F}_1.fastq
    sed -i "s:.2 : :g" ${DATA_DIR}/${F}_2.fastq

    ${RSEM_DIR}/rsem-calculate-expression -p 10 \
            --bowtie-path ${BT_DIR} \
            --bowtie-n 0 \
            --bowtie-e 99999999 \
            --fragment-length-min 25\
            --fragment-length-max 1000\
            --bowtie-m 15 \
            --estimate-rspd \
            --paired-end \
            ${DATA_DIR}/${F}_1.fastq \
            ${DATA_DIR}/${F}_2.fastq \
            ${REF_DIR}/GRCh37 \
            ${OUT_DIR}/${F} ## output

    gzip ${DATA_DIR}/${F}_1.fastq
    gzip ${DATA_DIR}/${F}_2.fastq

    end=`date +%s`
    runtime=$((end-start))
    echo "Align and computing the reads takes "${runtime}"s"

done






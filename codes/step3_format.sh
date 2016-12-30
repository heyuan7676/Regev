#!/bin/bash -l

#SBATCH --time 10:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1

ALIGN_DIR=/scratch0/battle-fs1/heyuan/train/Regiv_Glioblastoma/alignments

### paste all TPMs for all cells
### output a N_genes x N_cells matrix


## gene ID

FILES=$(/bin/ls ${ALIGN_DIR}/*genes.results | xargs -n1 basename)
echo "geneID" ${FILES//.genes.results/} > ${ALIGN_DIR}/genes_cells.txt

## tumor ID

tumorID="tumorID"
for i in $FILES
do 
    ID=${i//.genes.results/}
    tumorID=${tumorID}" "`cat /scratch0/battle-fs1/heyuan/train/Regiv_Glioblastoma/GSE57872.txt  | grep ${ID} | awk '{print $12'}`
done
echo $tumorID >> ${ALIGN_DIR}/genes_cells.txt

## paste TMP column

FILES=$(ls ${ALIGN_DIR}/*.genes.results)
paste <(awk '{print $1}' ${ALIGN_DIR}/SRR1294492.genes.results) <(awk '{ a[FNR] = (a[FNR] ? a[FNR] FS : "") $6 } END { for(i=1;i<=FNR;i++) print a[i] }' ${FILES}) >> ${ALIGN_DIR}/genes_cells.txt
sed -i "3d" ${ALIGN_DIR}/genes_cells.txt



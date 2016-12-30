#!/bin/bash -l

#### 1. build references from transcripts for GRCh37/hg19

# download gtf annotations from UCSC table browser
#     or from Ensemble: wget -O ${REF_DIR}/Homo_sapiens.GRCh37.87.gtf.gz ${REF_DIR} ftp://ftp.ensembl.org/pub/grch37/update/gtf/homo_sapiens//Homo_sapiens.GRCh37.87.gtf.gz
# download the fa file: wget -O ${REF_DIR}/hg19.fa.masked  http://hgdownload.cse.ucsc.edu/goldenPath/hg19/bigZips/chromFaMasked.tar.gz
# download transcript_to_gene_names from http://grch37.ensembl.org/biomart/martview/d316be00ea561ec0d92550f8cd2018a2?VIRTUALSCHEMANAME=default&ATTRIBUTES=hsapiens_gene_ensembl.default.feature_page.ensembl_gene_id|hsapiens_gene_ensembl.default.feature_page.ensembl_transcript_id&FILTERS=&VISIBLEPANEL=resultspanel 
# download ref for bowtie: wget ftp://ftp.ccb.jhu.edu/pub/data/bowtie_indexes/hg19.ebwt.zip

# make sure the geneID and transcriptID in gtf match with IDs in the human_ref_mapping_GRChxx.txt file (delete the .x);
# python modify_genode_gtf.py
# delete the genes that map to different chrs using the UCSC annotations (here I deleted all genes all chrY)
# cat gencode.v25.annotation_new.gtf | grep -v "chrY" > gencode.v25.annotation_new_noY.gtf
# store results using gencode.v25.annotation_new_noY.gtf to gencode.v25

# make sure the chr names in gtf match with chr names in fa file (add 'chr', watch out the "chrUN" ones!)
# python modify_ensembl_gtf.py 
# GRCh38: turns out that the chromsomes are quite different formatted, will go with UCSC annotation first. can go back to this if needed.
# GRCh37: need to modify fa file. delete "random", "chrM" to "chrMT" 
#         sed "s/chrM/chrMT/g" hg19.fa.masked  | sed "s/_random//g" > temp



#SBATCH --time 10:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=5

REF_DIR=/scratch0/battle-fs1/heyuan/train/assembly
RSEM_DIR=/scratch1/battle-fs1/tools_shared/RSEM-1.2.29
BT_DIR=/scratch1/battle-fs1/tools_shared/bowtie-1.1.2



start=`date +%s`

${RSEM_DIR}/rsem-prepare-reference -p 6\
    --gtf ${REF_DIR}/Homo_sapiens.GRCh37.87_new.gtf \
    --transcript-to-gene-map ${REF_DIR}/human_ref_mapping_GRCh37.txt \
    --bowtie \
    --bowtie-path ${BT_DIR} \
    ${REF_DIR}/hg19.fa.masked \
    ${REF_DIR}/GRCh37

end=`date +%s`
runtime=$((end-start))
echo "Construct the reference genomes takes "${runtime}"s"




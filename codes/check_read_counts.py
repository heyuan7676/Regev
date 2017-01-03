
# coding: utf-8

# In[114]:

import os
import pandas as pd
import numpy as np
import re
from itertools import chain
from scipy.spatial.distance import pdist
from collections import Counter
from matplotlib import pyplot as plt

from scipy.stats import gaussian_kde


# In[2]:

DATA_DIR = '/Users/Yuan/Documents/codes/Regev/data'
PLOT_DIR = '/Users/Yuan/Documents/codes/Regev/plot'

filename = os.path.join(DATA_DIR, 'genes_cells.txt')

true_result = pd.read_csv(os.path.join(DATA_DIR,'GSE57872_GBM_data_matrix.txt'),sep='\t',index_col=0)
IDs = [x.split('_')[0] for x in true_result.columns]
Counter(IDs)

####
## The initial dataset included 875 RNA-seq libraries:
## 576 single glioblastoma cells, 
## 96 resequenced MGH30L
## 192 single gliomasphere cells: CSC6 = GBM6, CSC8 = GBM8
## 5 tumor population controls
## 6 population libraries from GSC and DGC samples for MGH26,28,31: MGH26CSC = GSC, MGH26FCS = DGC


# In[5]:

sample_info = pd.read_csv(os.path.join(DATA_DIR, 'GSE57872.txt'),sep='\t')
sample_info.index = sample_info['Run_s']
del sample_info.index.name
Counter(sample_info['source_name_s'])


# In[6]:

reads = pd.read_csv(os.path.join(DATA_DIR,'genes_cells.txt'),sep=' ', index_col=0)
del reads.index.name
reads = reads.transpose()
genes = reads.columns


# In[24]:

data = reads.merge(sample_info[['patient_id_s','source_name_s','cell_type_s','cell_line_s']], 
                   left_index=True, right_index=True)

### drop the resuquenced MGH30 samples

temp = sample_info[sample_info['source_name_s'] == 'Single cell mRNA-seq_MGH30'].index
data = data.drop(temp[len(temp)/2:])

Counter(data['source_name_s'])


# In[102]:

### glioblastoma samples

Glioblastoma_df = data[data['cell_type_s'] == 'Glioblastoma']
info = [x for x in Glioblastoma_sig_df.columns if 'ENSG' in x] + ['patient_id_s']

### sc RNA seq 
Glioblastoma_sig_df = Glioblastoma_df[['Single' in x for x in Glioblastoma_df['source_name_s']]]
Glioblastoma_sig_df = Glioblastoma_sig_df[info]

### bulk RNA seq
Glioblastoma_pop_df = Glioblastoma_df[['Population' in x for x in Glioblastoma_df['source_name_s']]]
Glioblastoma_pop_df = Glioblastoma_pop_df[info]


# In[56]:

g = TPM_df[genes]
g = g.apply(lambda x: np.log2(x+1))
gene_mean = g.mean(axis=0)
print np.percentile(gene_mean,[90,95,100])




# In[59]:

### single cell statistics

## group by tumor ID, extract genes with average log2(TPM) > 6 in at least one tumor

good_genes = []
TPM_df = Glioblastoma_sig_df.groupby(['patient_id_s'])
for name,g in TPM_df:
    g = g[genes]
    g = g.apply(lambda x: np.log2(x+1))
    gene_mean = g.mean(axis=0)
    print name, np.percentile(gene_mean,[90,95,100])
    threshold = np.percentile(gene_mean,[90,95,100])[0]
    good_genes.append(list(np.array(genes)[np.where(gene_mean > threshold)[0]]))
    

## extract genes with average log2(TPM) > 4.5 across all cells

g = TPM_df[genes]
g = g.apply(lambda x: np.log2(x+1))
gene_mean = g.mean(axis=0)
print np.percentile(gene_mean,[90,95,100])

threshold = np.percentile(gene_mean,[90,95,100])[0]
good_genes.append(list(np.array(genes)[np.where(gene_mean > threshold)[0]]))


## pick out unique genes
good_genes = list(set(list(chain.from_iterable(good_genes))))


len(good_genes)


# In[104]:

### restrict to genes

Glioblastoma_sig_df = Glioblastoma_sig_df[np.array(good_genes)]
Glioblastoma_pop_df = Glioblastoma_pop_df[np.array(good_genes)]

### restrict to cells
good_cells = Glioblastoma_sig_df.apply(lambda x: sum(x>0), axis=1)
print np.percentile(good_cells,[30,40,50])
number_gene_threshold = np.percentile(good_cells,[30,40,50])[0]

Glioblastoma_sig_df = Glioblastoma_sig_df.loc[good_cells > number_gene_threshold]

# check the composition of remaining cells
print Counter(Glioblastoma_sig_df.merge(sample_info, left_index=True, right_index=True)['source_name_s'])


# In[111]:

### compare single cell results with the bulk cells'

TPM_sig = Glioblastoma_sig_df.merge(pd.DataFrame(sample_info['patient_id_s']), left_index=True, right_index=True)
TPM_sig_avg = TPM_sig.groupby(['patient_id_s']).mean().transpose()
TPM_sig_avg_log2 = TPM_sig_avg.apply(lambda x: np.log2(x+1))

TPM_pop = Glioblastoma_pop_df.merge(pd.DataFrame(sample_info['patient_id_s']), left_index=True, right_index=True)
TPM_pop = TPM_pop.set_index(['patient_id_s']).transpose()
TPM_pop_log2 = TPM_pop.apply(lambda x: np.log2(x+1))



X = [list(x) for x in np.array(TPM_sig_avg_log2.transpose())]
Y = [list(x) for x in np.array(TPM_pop_log2.transpose())]
Z = [[[x,y] for y in Y] for x in X]
cor = np.reshape(map(lambda x: np.corrcoef(x)[0,1], list(chain.from_iterable(Z))),[5,5])


cor - np.mean(cor)


# In[126]:

grid_max = 20
grid_min = -1

plt.figure()
plt.scatter(TPM_sig_avg_log2['MGH26'], TPM_pop_log2['MGH26'])
plt.xlabel('Population RNA-seq log2(TPM+1)')
plt.ylabel('Average of log2(TPM+1) from single cell RNA-seq of MGH26')
plt.plot([0,grid_max],[0,grid_max])
plt.title('Sup_Fig2A')
plt.xlim([grid_min,grid_max])
plt.ylim([grid_min,grid_max])
plt.savefig(os.path.join(PLOT_DIR,'Sup_Fig2A.png'))
plt.close()


# In[129]:

grid_max = 20
grid_min = -1

plt.figure()
plt.scatter(Glioblastoma_sig_df.iloc[100], Glioblastoma_sig_df.iloc[101])
plt.xlabel('Cell1 log2(TPM+1)')
plt.ylabel('Cell2 log2(TPM+1)')
plt.plot([0,grid_max],[0,grid_max])
plt.title('Sup_Fig2B')
plt.xlim([grid_min,grid_max])
plt.ylim([grid_min,grid_max])
plt.savefig(os.path.join(PLOT_DIR,'Sup_Fig2B.png'))
plt.close()


# In[175]:

df_plot = pd.DataFrame((cor[::-1] - np.mean(cor)))
df_plot.columns = list(TPM_pop_log2.columns)
df_plot.index = list(TPM_pop_log2.columns)[::-1]

plt.figure()
plt.pcolor(df_plot)
plt.yticks(np.arange(0.5, len(df_plot.index), 1), df_plot.index)
plt.xticks(np.arange(0.5, len(df_plot.columns), 1), df_plot.columns)
plt.xlabel('Population Controls')
plt.ylabel('Single Cell Average')
plt.colorbar()
plt.title('Sup_Fig2C')
plt.savefig(os.path.join(PLOT_DIR,'Sup_Fig2C.png'))
plt.close()


# In[174]:

# all_cor = np.corrcoef(np.array(Glioblastoma_sig_df[TPM_sig['patient_id_s'] == 'MGH26']))

plt.figure()

density = gaussian_kde(list(chain.from_iterable(all_cor)))
xs = np.linspace(0,1,200)
density.covariance_factor = lambda : .25
density._compute_covariance()
plt.plot(xs,density(xs))
plt.xlabel('Correlation between single cells from MGH26')
plt.title('Sup_Fig2E.png')
plt.savefig(os.path.join(PLOT_DIR,'Sup_Fig2E.png'))
plt.close()


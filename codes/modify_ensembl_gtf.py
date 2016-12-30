

def GRCh38():
    file = open("/scratch0/battle-fs1/heyuan/train/assembly/Homo_sapiens.GRCh38.86.gtf", 'r')
    f = open("/scratch0/battle-fs1/heyuan/train/assembly/Homo_sapiens.GRCh38.86_new.gtf",'w')
    
    for line in file:
        if line.startswith("#"):
            f.write(line)
        else:
            if line.startswith('KI') or line.startswith('GL'):
                f.write('chrUN_')
            else:
                f.write('chr')
            f.write(line)
    file.close()
    f.close()



def GRCh37():
    '''
    Need to transform all "GL001" to "gl001" prior to use this 
    '''
    file = open("/scratch0/battle-fs1/heyuan/train/assembly/Homo_sapiens.GRCh37.87.gtf", 'r')
    f = open("/scratch0/battle-fs1/heyuan/train/assembly/Homo_sapiens.GRCh37.87_new.gtf",'w')

    for line in file:
        if line.startswith("#"):
            f.write(line)
        else:
            if line.startswith('gl'):
                chrnumber=line.split('\t')[0]
                newline='\t'.join((chrnumber.split('.')[0],'\t'.join(line.split('\t')[1:])))
                f.write('chrUn_')
                f.write(newline)
            else:
                f.write('chr')
                f.write(line)
    file.close()
    f.close()


if __name__ == "__main__":
    GRCh37()

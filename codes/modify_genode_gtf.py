file = open("/scratch0/battle-fs1/heyuan/playaround/data/assembly/gencode.v25.annotation.gtf", 'r')
f = open("/scratch0/battle-fs1/heyuan/playaround/data/assembly/gencode.v25.annotation_new.gtf",'w')

for line in file:
    if line.startswith("#"):
        f.write(line)
    else:
        f.write('\t'.join(line.split('\t')[:8]))
        f.write('\t')
        f.write(line.split('\t')[8].split(';')[0].split(' ')[0])
        f.write(' ')
        f.write(line.split('\t')[8].split(';')[0].split(' ')[1].split('.')[0])
        f.write('"; ')
        transcript = line.split('\t')[8].split(';')[1]
        if "transcript_id" in transcript:
            f.write(line.split('\t')[8].split(';')[1].split(' ')[1])
            f.write(' ')
            f.write(line.split('\t')[8].split(';')[1].split(' ')[2].split('.')[0])
            f.write('"; ')
            f.write(';'.join(line.split('\t')[8].split(';')[2:]))
        else:
            f.write(';'.join(line.split('\t')[8].split(';')[1:]))



file.close()
f.close()

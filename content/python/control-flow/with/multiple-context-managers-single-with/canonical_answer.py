def copy_file(src, dst):
    with open(src, 'r') as fin, open(dst, 'w') as fout:
        for line in fin:
            fout.write(line)

import os
import re
import glob
import sys

cwd = os.getcwd()
m = re.search(r"(\d{3})/halos", cwd)
if m:
    iout = m.group(1)
    out = './all_'+iout+'.AHF_particles'
else:
    out = './all.AHF_particles'

print('Writing to', out)
fns = glob.glob('./*.AHF_particles')
fns.sort()

num_halo_tot = 0

for fn in fns:
    with open(fn, 'r') as f:
        line = f.readline()
        num_halo_tot += int(line.strip())

with open(out, 'w') as fout:
    fout.write(f'\t {num_halo_tot:d}\n')
    for fn in fns:
        with open(fn, 'r') as fin:
            fin.readline()  # skip first line
            for line in fin:
                fout.write(line)
        

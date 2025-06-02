import os
import glob

out_dirs = glob.glob(r'???/')
nf = len(out_dirs)
out_dirs = sorted(out_dirs)[::-1]
prefixes = []

with open('prefix_list.txt', 'w') as f:
    for out_dir in out_dirs:
        fn = glob.glob(os.path.join(out_dir, 'halos/*.AHF_particles'))
        print(fn)
        fn = fn[0]
        prefixes.append(fn.strip('_particles'))               


    for i in range(nf-1):
        f.write(f'{prefixes[i]:s}\n')

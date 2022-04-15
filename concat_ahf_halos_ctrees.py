"""
Made this because AHF outputs were produced using the entire range of
64 bits for the halo ID, where some of the bits come from the mass and
some of the bits come from the position.  This makes it impossible to
use consistent-trees as it tries to allocate max(hid) - min(hid) + 1
bytes.
"""

import os
import re
import glob
import sys
import numpy as np

def get_num_halo_tot(fns):
    num_halo_tot = 0
    for fn in fns:
        with open(fn, 'r') as f:
            line = f.readline()
            num_halo_tot += int(line.strip())

    return num_halo_tot

SNAP_STEP = 10000000   # 10 million haloes per snap

cwd = os.getcwd()
m = re.search(r"(\d{3})/halos", cwd)
if m:
    iout = m.group(1)
    out_h = './all_'+iout+'.AHF_halos'
    out_p = './all_'+iout+'.AHF_particles'
else:
    out_h = './all.AHF_halos'
    out_p = './all.AHF_particles'

print('Writing to', out_h, out_p)

h_fns = glob.glob('./*.AHF_halos')
h_fns.sort()
p_fns = glob.glob('./*.AHF_particles')
p_fns.sort()

num_halo_tot = get_num_halo_tot(p_fns)
# Read halos and get max ID
# min_id = 2**64
# max_id = 0

# Get all halo IDs for reassigning
halo_ids = np.zeros(num_halo_tot, dtype=np.int64)
cur_halo = 0
for fn in h_fns:
    x = np.loadtxt(fn, usecols=0, dtype=np.int64)
    num_halo = len(x)
    halo_ids[cur_halo:cur_halo+num_halo] = x
    cur_halo += num_halo

# Now make a dictionary mapping halo IDs to some new ID
cur_snap_step = int(iout) * SNAP_STEP
hid_conv = {hid: cur_snap_step + i for i, hid in enumerate(halo_ids)}

# Write the header first, so handle first file a bit differently
with open(out_h, 'w') as fout:
    with open(h_fns[0], 'r') as fin:
        head = fin.readline()
        fout.write(head)
        for line in fin:
            sl = line.split(None, 1)
            # Don't need \n since we keep it from the original
            fout.write(f'{hid_conv[int(sl[0])]:d}\t{sl[1]:s}')
    # Now just write the haloes out
    for fn in h_fns[1:]:
        with open(fn, 'r') as fin:
            for line in fin:
                sl = line.split(None, 1)
                fout.write(f'{hid_conv[int(sl[0])]:d}\t{sl[1]:s}')


# Now do the particles
with open(out_p, 'w') as fout:
    fout.write(f'\t {num_halo_tot:d}\n')
    for fn in p_fns:
        with open(fn, 'r') as fin:
            nh_loc = int(fin.readline())  # skip first line
            while nh_loc > 0:
                cur_halo = fin.readline().strip().split()
                cur_part = int(cur_halo[0])
                cur_hid = int(cur_halo[1])
                fout.write(f'{cur_part:d}\t{hid_conv[cur_hid]:d}\n')
                for ip in range(cur_part):
                    fout.write(fin.readline())
                nh_loc -= 1  # done with this halo

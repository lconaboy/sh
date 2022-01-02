#! /usr/bin/python3

"""Script to remove walltime dumps from ramses outputs, and restore
the number of snapshots determined by delta_aout.

BE VERY CAREFUL WITH THIS -- it directly modifies output files, if you
aren't sure don't use.

"""

import re
import os
import sys
import glob
import shutil

DRY_RUN = True
CLEANUP_BAK = False

def get_aout(aini, aend, delta_aout):
    """Returns the output expansion factors determined before the
    simulation starts. First aout corresponds to the initial expansion
    factor.

    """
    
    maxout = 1000
    nout = min([int(aend / delta_aout), maxout])
    nini = int(aini / delta_aout)
    aout = [i * delta_aout for i in range(nout + 1)
            if (i > aini) or (i == 0)]
    aout[0] = aini

    return aout

def get_aouts_nml(output_dir, nml='nml.nml'):
    # Get the first aout from output_00001/info_00001.txt
    info = os.path.join(output_dir, 'output_00001/info_00001.txt')
    with open(info, 'r') as f:
        line = ''
        while re.match('aexp', line) is None:
            line = f.readline()#.strip().split()
            
    aini = float(line.strip().split()[-1])

    with open(nml, 'r') as f:
        for line in f:
            if line[0:4] == 'aout':
                neq = line.find('=')
                aouts = [float(x) for x in line[neq+1:].split(',')]
                aouts.insert(0, aini)

                return aouts

def get_aexp(output_dir):
    """Returns the actual expansion factors of each output, lifted from
    the info_xxxxx.txt files.

    """
    aexps = []
    outs = glob.glob(os.path.join(output_dir, 'output_*'))
    info = os.path.join(output_dir, 'output_{0:05d}', 'info_{0:05d}.txt')
    
    # Do a regex to get the output numbers
    all_iouts = [int(re.search(r'output_[0-9]{5}', out).group()[-5:]) for out in outs]
    print(all_iouts)

    # Check to see if we got partway through this process and any
    # backups remain
    if os.path.isdir(os.path.join(output_dir, 'output_*.bak')):
        bak_iouts = [int(re.search(r'output_[0-9]{5}', out).group()[-5:]) for out in bak_outs]
        print('Found backups')
        print(bak_iouts)
        iouts = [x for x in all_iouts if x not in bak_iouts]
    else:
        iouts = all_iouts

    print(iouts)
    # Ignore .bak files
    # iouts = sorted([int(iout) for iout in iouts if '.bak' not in iout])

    _iouts = []
    # Open the info files to get the aexps
    for iout in iouts:
        if os.path.isfile(info.format(iout)):
            f = open(info.format(iout), 'r')
            line = f.readline()#.strip().split()

            # See if the line has aexp in it
            while re.match('aexp', line) is None:
                line = f.readline()#.strip().split()
            f.close()

            _iouts.append(iout)
            aexps.append(float(line.strip().split()[-1]))

    iouts = _iouts
    
    return iouts, aexps


def split_iouts(iouts, aouts, aexps):
    k_iouts = []

    for aout in aouts:
        diff = [abs(aexp - aout) for aexp in aexps]
        k_iouts.append(iouts[diff.index(min(diff))])

    # Now find the ones we want to remove
    r_iouts = [x for x in iouts if x not in k_iouts]
    # print(k_iouts)
    # print(r_iouts)

    return k_iouts, r_iouts

def check(msg):
    ans = input(msg +' y/n ')
    if ans != 'y':
        sys.exit(1)

    return

if len(sys.argv) > 1:
    nml = sys.argv[1]
else:
    nml = 'nml.nml'

output_dir = './' # '/cosma7/data/dp004/dc-cona1/bd/runs/halo10510/sametf'
    
aouts = get_aouts_nml(output_dir, nml)

print('WARNING check the following list of aouts carefully and make sure')
print('        they match up with what you expect')
print(aouts)
if DRY_RUN:
    print('files won\'t be modified')
else:
    print('WARNING output files will be modified')
    print('WARNING run inside a screen')
    if CLEANUP_BAK:
        print('WARNING backups will be deleted, too')
check('sure?')
check('really sure?')
if DRY_RUN:
    print('ok, doing a dry run')
else:
    print('ok, removing wallclock dumps...')

iouts, aexps = get_aexp(output_dir)
# Find largest aexp and keep aouts up to there
ma_aexp = max(aexps)
_aouts = [x for x in aouts if x < ma_aexp]
aouts = _aouts
k_iouts, r_iouts = split_iouts(iouts, aouts, aexps)


# for each aout. Then move (or delete) the unmatched directories and
# rename the others by using regex sub or replace.

for r_iout in r_iouts:
    src = os.path.join(output_dir, 'output_{0:05d}'.format(r_iout))
    dst = os.path.join(output_dir, 'output_{0:05d}.bak'.format(r_iout))

    print('moving', src, dst)
    if (not DRY_RUN):
        os.rename(src, dst)

# k_iout - keep iouts
for i, k_iout in enumerate(k_iouts):
    t_iout = i + 1 

    # t_iout - true iout (i.e. 1, 2, ..., n)
    if t_iout == k_iout:
        print('leaving output_{0:05d}'.format(t_iout))
    else:
        src = os.path.join(output_dir, 'output_{0:05d}'.format(k_iout))
        dst = os.path.join(output_dir, 'output_{0:05d}'.format(t_iout))

        print('moving', src, dst)
        if (not DRY_RUN):
            os.rename(src, dst)

        # Rename each file
        fns = glob.glob(os.path.join(dst, '*_{0:05d}.*'.format(k_iout)))
        
        for src_f in fns:
            dst_f = src_f.replace('_{0:05d}.'.format(k_iout),
                                  '_{0:05d}.'.format(t_iout))
            print(dst_f)
            if (not DRY_RUN):
                os.rename(src_f, dst_f)

# Finally clean up the backups
if ((not DRY_RUN) and CLEANUP_BAK):
    baks = glob.glob(os.path.join(output_dir, '*output_*.bak'))
    for bak in baks:
        shutil.rmtree(bak)

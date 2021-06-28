import sys

iout = int(sys.argv[1])
info_fn = 'output_{0:05d}/info_{0:05d}.txt'.format(iout)

with open(info_fn, 'r') as f:
    for l in f:
        if 'aexp' in l:
            aexp = float(l.strip().split()[-1])
            break

print('output_{0:05d} at a = {1:.3f} z = {2:.3f}'.format(iout, aexp,
                                                         1./aexp - 1.))

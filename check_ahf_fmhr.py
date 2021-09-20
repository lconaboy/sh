import glob
import numpy as np
import matplotlib.pyplot as plt

fns = glob.glob('./all*AHF_halos')
assert(len(fns) == 1), 'More than one all*AHF_halos file found'
x = np.loadtxt(fns[0], usecols=37)
m = np.loadtxt(fns[0], usecols=3)
p = np.loadtxt(fns[0], usecols=(5, 6, 7))

nh = x.shape[0]
u = np.abs(x - 1.0) < 1e-10
nu = np.sum(u)

print('-- {0}/{1} ({2:5.3f}%) of haloes uncontaminated'.format(nu, nh, 100. * nu / nh))
print('---- smallest uncontaminated halo {0:5.3e} Msol/h'.format(np.min(m[u])))
print('---- largest uncontaminated halo {0:5.3e} Msol/h'.format(np.max(m[u])))

# Are they in the centre?
# for i in range(0, nu, 100):
#     print(p[u][i, :])

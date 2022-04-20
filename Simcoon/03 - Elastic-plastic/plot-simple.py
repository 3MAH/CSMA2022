# -*- coding: utf-8 -*-

#This is a very simple matplotlib script to plot results from 'results_job.txt'

from mpl_toolkits.mplot3d import Axes3D
#from matplotlib import cm
#from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np
import os

plt.rcParams['text.usetex'] = True

fig = plt.figure()
path = os.path.dirname(os.path.realpath('__file__')) + '/results/'

PL = path + 'results_EPICP_global-0.txt'

#valid = data_path + 'valid.txt'

e11, e22, e33, e12, e13, e23, s11, s22, s33, s12, s13, s23 = np.loadtxt(PL, usecols=(8,9,10,11,12,13,14,15,16,17,18,19), unpack=True)
#time, T, Q, r, Wm, Wm_r, Wm_ir, Wm_d, Wt, Wt_r, Wt_ir = np.loadtxt(PL, usecols=(4,5,6,7,20,21,22,23,24,25,26), unpack=True)
time, T, Q, r = np.loadtxt(PL, usecols=(4,5,6,7), unpack=True)

Wm, Wm_r, Wm_ir, Wm_d = np.loadtxt(PL, usecols=(20,21,22,23), unpack=True)

ax = fig.add_subplot(1, 2, 1)
plt.grid(True)
plt.tick_params(axis='both', which='major', labelsize=15)
plt.xlabel(r'Strain $\varepsilon$', size = 15)
plt.ylabel(r'Stress $\sigma$ (MPa)', size = 15)
plt.plot(e11,s11, c='black', label='direction 1')
#plt.xlim(-0.051,0.051)
plt.legend(loc=2)

ax = fig.add_subplot(1, 2, 2)
plt.grid(True)
plt.tick_params(axis='both', which='major', labelsize=15)
plt.xlabel('time (s)', size = 15)
plt.ylabel(r'Mechanical work per unit volume $W_m$ (MPa)',size = 15)
plt.plot(time,Wm, c='black', label=r'total $W_m$')
plt.plot(time,Wm_r, c='green', label='recoverable $Wm_r$')
plt.plot(time,Wm_ir, c='blue', label='irrecoverable $Wm_{ir}$')
plt.plot(time,Wm_d, c='red', label='dissipated $Wm_d$')
plt.legend(loc=2)

plt.show()

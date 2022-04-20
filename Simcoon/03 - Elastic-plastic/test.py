import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from simcoon import simmit as sim
import os

dir = os.path.dirname(os.path.realpath('__file__'))
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

umat_name = 'EPCHA' #This is the 5 character code for the elastic-plastic subroutine
nstatev = 33 #The number of scalar variables required, only the initial temperature is stored here

#Mechancial
E = 140000
nu_A = 0.3
alphaA = 1.E-6
sigmaY = 57.860277
Q = 280.486698
b = 7.602458
C_1 = 31194.683709
D_1 = 176.124282
C_2 = 435376.840808
D_2 = 5367.404166

solver_type = 0
corate_type = 2

##local orientation
psi_rve = 0.
theta_rve = 0.
phi_rve = 0.

#Define the properties
props = np.array([E, nu_A, alphaA, sigmaY, Q, b, C_1, D_1, C_2, D_2])
path_data = 'data'
path_results = 'results'

#Run the simulation
pathfile = 'path.txt'
outputfile = 'results_EPICP.txt'
sim.solver(umat_name, props, nstatev, psi_rve, theta_rve, phi_rve, solver_type, corate_type, path_data, path_results, pathfile, outputfile)


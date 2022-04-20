import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from simcoon import simmit as sim

plt.rcParams['text.usetex'] = True

phi = np.linspace(0,2*np.pi, 128) # the angle of the projection in the xy-plane
theta = np.linspace(0, np.pi, 128).reshape(128,1) # the angle from the polar axis, ie the polar angle

n_1 = np.sin(theta)*np.cos(phi)
n_2 = np.sin(theta)*np.sin(phi)
n_3 = np.cos(theta)*np.ones(128)

n = np.array([n_1*n_1, n_2*n_2, n_3*n_3, n_1*n_2, n_1*n_3, n_2*n_3]).transpose(1,2,0).reshape(128,128,1,6)

C11 = 185000. #(MPa)
C12 = 158000. #(MPa)
C44 = 39700. #(MPa)

E1 = 13810
E2 = 678
E3 = 1311
nu12 = 0.5
nu13 = 0.460
nu23 = 0.420
G12 = 753
G13 = 1013
G23 = 255

L = sim.L_ortho(E1, E2, E3, nu12, nu13, nu23, G12, G13, G23, 'EnuG')
#L = sim.L_cubic(C11, C12, C44, 'Cii')

M = np.linalg.inv(L)

S = (n@M@n.reshape(128,128,6,1)).reshape(128,128)

print(S.shape)

E = (1./S)
x = E*n_1
y = E*n_2
z = E*n_3

#E = E/E.max()

fig = plt.figure(figsize=plt.figaspect(1))  # Square figure
ax = fig.add_subplot(111, projection='3d')
#ax.plot_surface(x, y, z, cmap='hot',c=E)

norm = colors.Normalize(vmin = np.min(E), vmax = np.max(E), clip = False)
surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, norm=norm, facecolors=cm.bone(norm(E)),linewidth=0, antialiased=False, shade=False)

#ax.set_xlim(0,20000)
#ax.set_ylim(0,20000)
#ax.set_zlim(0,20000)
ax.set_xlabel(r'$E_x$ (MPa)')
ax.set_ylabel(r'$E_y$ (MPa)')
ax.set_zlabel(r'$E_z$ (MPa)')

scalarmap = cm.ScalarMappable(cmap=plt.cm.bone, norm=norm)
#m.set_array([])
cbar = plt.colorbar(scalarmap)
#cbar.ax.set_yticklabels(['0','1','2','>3'])
cbar.set_label(r'directional stiffness $E$ (MPa)', rotation=270)

plt.show()

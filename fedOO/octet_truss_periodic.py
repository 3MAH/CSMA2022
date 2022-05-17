# -*- coding: utf-8 -*-
"""
Created on Fri May 13 17:33:59 2022

@author: Etienne
"""
from fedoo import *
import numpy as np
import pyvista as pv

#pv.set_jupyter_backend('ipygany')

#Define the Modeling Space - Here 3D problem 
Util.ProblemDimension("3D")

#Import the mesh generated with Microgen 
Mesh.ImportFromFile('data/octet_surf.msh', meshID = "Domain")

#Get the imported mesh 
mesh = Mesh.GetAll()["Domain2"]

#Get the bounding box (corners coordinates and center)
Xmin, Xmax, crd_center = mesh.GetBoundingBox(return_center = True)
# total volume of the bounding box
Volume = (Xmax-Xmin).prod()

#Nearest node to the center of the bounding box for boundary conditions
center = mesh.GetNearestNode(crd_center)

# Add 2 virtual nodes for macro strain 
StrainNodes = mesh.AddNodes(crd_center, 2)  

#Define an elastic isotropic material with E = 2e5MPa et nu = 0.3 (steel)
material = ConstitutiveLaw.ElasticIsotrop(2e5, 0.3, ID = 'ConstitutiveLaw') 

#Create the weak formulation of the mechanical equilibrium equation
wf = WeakForm.InternalForce(material, ID = "WeakForm", nlgeom=False)

# Assembly
assemb = Assembly.Create("WeakForm", "Domain2", ID="Assembly")

# Type of problem
pb = Problem.Static("Assembly", ID = 'octet truss')

# Set the desired ouputs at each time step
#pb.AddOutput('results_octet', 'Assembly', ['disp', 'cauchy', 'PKII', 'strain', 'cauchy_vm', 'statev'], output_type='Node', file_format ='vtk')
pb.AddOutput('results_octet', 'Assembly', ['disp', 'stress', 'strain'], output_type='Node', file_format ='vtk')

# Boundary conditions for the linearized strain tensor
E = [0, 0, 0, 0.1, 0, 0]  # [EXX, EYY, EZZ, EXY, EXZ, EYZ]

Homogen.DefinePeriodicBoundaryCondition('Domain2',
	    [StrainNodes[0], StrainNodes[0], StrainNodes[0],
         StrainNodes[1], StrainNodes[1], StrainNodes[1]],
        ['DispX', 'DispY', 'DispZ', 'DispX', 'DispY', 'DispZ'], dim='3D', ProblemID = 'octet truss')

#fixed point on the center to avoid rigid body motion
pb.BoundaryCondition('Dirichlet', 'Disp', 0, center)

#Enforced mean strain
pb.BoundaryCondition('Dirichlet', 'Disp', [E[0], E[1], E[2]], [
                           StrainNodes[0]])  # EpsXX, EpsYY, EpsZZ
pb.BoundaryCondition('Dirichlet', 'Disp', [E[3], E[4], E[5]], [
                           StrainNodes[1]])  # EpsXY, EpsXZ, EpsYZ

pb.ApplyBoundaryCondition()

# ---------------  Non linear solver--------------------------------------------
pb.SetSolver('cg')
pb.Solve()

# --------------- Post-Treatment -----------------------------------------------
# Get the stress and strain tensor (PG values)
#res = pb.GetResults('Assembly', ['Strain','Stress'], 'GaussPoint') 
#TensorStrain = res['Strain']
#TensorStress = res['Stress']
pb.SaveResults()
meshplot = pv.read('results_octet.vtk')
pl = pv.Plotter()
pl.set_background('White')

sargs = dict(
    interactive=True,
    title_font_size=20,
    label_font_size=16,
    color='Black',
    # n_colors= 10
)


# pl.add_mesh(meshplot.warp_by_vector(factor = 5), scalars = 'Stress', component = 2, clim = [0,10000], show_edges = True, cmap="bwr")
pl.add_mesh(meshplot.warp_by_vector(factor = 3), scalars = 'Stress', component = 2, show_edges = True, scalar_bar_args=sargs)

pl.save_graphic('test.pdf', title='PyVista Export', raster=True, painter=True)
pl.show()

#!/usr/bin/env python
import clawpack.petclaw.solution as solution
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import cantera as ct

matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['legend.fontsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 14
matplotlib.rcParams['ytick.labelsize'] = 14
matplotlib.rcParams['lines.markersize'] = 8
matplotlib.rcParams['lines.linewidth'] = 1.0
matplotlib.rcParams['figure.dpi'] = 600
matplotlib.rcParams.update({'figure.autolayout': True})


key_species = ['E','H2O']
e = 1.6*10.**(-19.)
me = 9.11*10.**(-31.)
kb = 1.38*10.**(-23.)
Qk = 102.00


#### create dictionary for species concentrations
with open('species.txt','r') as file:
	species = [line.strip() for line in file]
file.close()

spec = {key: [] for key in species}
############



##### pull in species for desired steip
#for i in xrange(time_steps):
sol = solution.Solution(50, path='./_output',file_format='petsc')
	#print np.shape(sol.state.aux[2])
for j in xrange(len(species)-1):
	for i in xrange(np.size(sol.state.aux[2])):
		spec[species[j]].append(sol.state.aux[j,i])#[j,500,20])
		
q = sol.state.q
rho = q[0,:]
rhou = q[1,:]
rhoE = q[2,:]
u = rhou/rho
E =rhoE/rho
p = 0.4*(rhoE - 0.5*rho*u*u)

gas = ct.Solution('/mnt/d/Research/Ionization_mechanism/methane_ionized.cti')
gas.X = 'H2:1.0, O2:0.5, KOH:0.00016'
MW_gas = gas.mean_molecular_weight
r_gas = 8314.0/MW_gas
T = p/(rho*r_gas)

ce = (8.0*kb*T/(3.14*me))**(0.5)

ne = np.asarray(spec['E'])
nk = np.asarray(spec['H2O'])
sigma = ne*e/(me*ce*nk*Qk)

#print spec['N2O']
#print c3h8
#print np.shape(c3h8)
x = np.linspace(0.0, 0.5, num = np.size(rho))

plt.figure()
plt.plot(x,sigma)

plt.xlabel('x [m]')
plt.ylabel('Conductivity [S/m]')
	
plt.savefig('conductivity.png')

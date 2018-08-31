#!/usr/bin/env python
import clawpack.petclaw.solution as solution
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['legend.fontsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 14
matplotlib.rcParams['ytick.labelsize'] = 14
matplotlib.rcParams['lines.markersize'] = 8
matplotlib.rcParams['lines.linewidth'] = 1.0
matplotlib.rcParams['figure.dpi'] = 600
matplotlib.rcParams.update({'figure.autolayout': True})

#key_species = ['C3H8','N2O','CO2','CO','H2O','C6H2','H2','O2','NO','C4H2']
key_species = ['CH4','CO', 'CO2','H2O', 'CH3']
#key_species = ['CH4, H, O, OH']
#key_species = ['H2','O2','H','O','H2O','OH','HO2','H2O2']
time_steps = 41
with open('species.txt','r') as file:
	species = [line.strip() for line in file]

file.close()

spec = {key: [] for key in species}

frame = 20
#for i in xrange(time_steps):
sol = solution.Solution(frame, path='./_output',file_format='petsc')
#print np.shape(sol.state.aux[2])
#if i != 0:
print np.size(sol.state.aux[2])
x = np.linspace(0.0, 0.5, num = np.size(sol.state.aux[2]))
for j in xrange(len(species)-1):
	for i in xrange(np.size(sol.state.aux[2])):
		spec[species[j]].append(sol.state.aux[j,i])#[j,500,20])

#a = spec.get('H2O') 
#print a	
#print spec['H2O']
#print c3h8
#print np.shape(H2O)

from itertools import cycle
lines = ["-","--","-.",":"]
linecycler = cycle(lines)

for i in key_species:
	 plt.plot(x, spec[i], next(linecycler), label = i )


#plt.plot(spec['H2O'])
plt.xlabel('Position x [m]')
plt.ylabel('Mole fraction')
plt.axis([0.1, 0.14, 0.0, 1.0])
plt.title('Methane Quasi-Det Species')	
plt.legend(loc = 4)	
plt.savefig('species_per_frame.png')

from ase import *
from math import asin, pi, sqrt
from gpaw import GPAW
from ase.lattice.surface import fcc111

# Define geometry of slab + BF4:
slab = fcc111('Au', size=(3, 2, 3),orthogonal=True)
slab.center(axis=2, vacuum=12)

d=0.8
tFB1 = Atoms([Atom('B', (0, 0, 0)),
            Atom('F', (d, d, d)),
            Atom('F', (-d, -d, d)),
            Atom('F', (-d, d, -d)),
            Atom('F', (d, -d, -d))])
tFB1.rotate('y',pi/4,center=(0, 0, 0))
tFB1.rotate('x',asin(1/sqrt(3))+pi,center=(0, 0, 0))
tFB1.rotate('z',pi/3,center=(0, 0, 0))
tFB1.translate(slab.positions[7]+(0.,0.,5.118))
slab += tFB1

# Fix second and third layers:
mask = [atom.tag > 1 for atom in slab]
#print mask
slab.set_constraint(constraints.FixAtoms(mask=mask))

# Initial state:
calc = GPAW(h=0.16, kpts=(4, 4, 1), txt='32.txt',parallel={'domain':8}, xc='RPBE')
slab.set_calculator(calc)
qn=optimize.QuasiNewton(slab,trajectory='32.traj',restart='32.pckl')
qn.run(fmax=0.05)
qn.attach(calc.write,1,'32.gpw')
calc.write('32.gpw')

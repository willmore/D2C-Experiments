from ase import *
from math import asin, pi, sqrt
from gpaw import GPAW
from ase.lattice.surface import fcc111

# Define geometry of slab + BF4:
slab = fcc111('Au', size=(4, 4, 3),orthogonal=True)
slab.center(axis=2, vacuum=12)

d=0.8234
tFB1 = Atoms([Atom('B', (0, 0, 0)),
            Atom('F', (d, d, d)),
            Atom('F', (-d, -d, d)),
            Atom('F', (-d, d, -d)),
            Atom('F', (d, -d, -d))])
tFB1.rotate('y',pi/4,center=(0, 0, 0))
tFB1.rotate('x',asin(1/sqrt(3))+pi,center=(0, 0, 0))
tFB1.rotate('z',pi/3,center=(0, 0, 0))
tFB1.translate(slab.positions[17]+(0.,0.,5.273))
slab += tFB1

# Fix second and third layers:
mask = [atom.tag > 1 for atom in slab]
#print mask
slab.set_constraint(constraints.FixAtoms(mask=mask))

# Initial state:
calc = GPAW(h=0.16, kpts=(4, 4, 1), txt='44.txt',parallel={'domain':32}, xc='RPBE')
slab.set_calculator(calc)
qn=optimize.QuasiNewton(slab,trajectory='44.traj',restart='44.pckl')
qn.attach(calc.write,1,'44.gpw')
qn.run(fmax=0.05)
calc.write('44.gpw')

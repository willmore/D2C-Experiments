from ase import *
from gpaw import *
from math import *
from gpaw.mpi import world

sqrt = 1.732050808

def energy(k, h, dl, da, vac, var, num):
    slab = Atoms([Atom('Bi', (0.0000, 0.0000,          -dl)),
                  Atom('Bi', (da/2,   sqrt*da/6,    0.0)),
                  Atom('Bi', (da/2,   sqrt*da/2,    -dl)),
                  Atom('Bi', (2*da,   2*sqrt*da/3,  0.0)),
                  Atom('Bi', (da,     0.0,             -dl)),
                  Atom('Bi', (3*da/2, sqrt*da/6,    0.0)),
                  Atom('Bi', (3*da/2, sqrt*da/2,    -dl)),
                  Atom('Bi', (da,     2*sqrt*da/3,  0.0))],
                  cell=((2*da,0,0), (da,sqrt*da,0), (0,0,1)),pbc=[True,True,False])
    slab.center(axis=2, vacuum=vac)
    calc = GPAW(h=h, kpts=(k, k, 1), parallel={'domain':world.size}, txt='Bi111'+var+"-"+str(num)+'.txt', xc='RPBE')
    slab.set_calculator(calc)
    e = slab.get_potential_energy()
    calc.write('Bi111'+var+"-"+str(num)+'.txt')
    return e

name = 'Bi111'

print 'Energy with respect to dl parameter'
#for dl in [1.66,1.665,1.67,1.675,1.68,1.685,1.90,1.905,1.71]:
for dl in [1.66]:   
   k = 4
   #h = 0.17
   h = 0.19
   da = 4.513
   #vac = 12
   vac = 8
   e = energy(k, h, dl, da, vac, 'dl', dl)
   print k, e

print 'Energy with respect to k value'
#for k in [2,4,6,8]:
for k in [2]:
   #h = 0.17
   h =0.19
   dl = 1.682
   da = 4.513
   #vac = 12
   vac = 8
   e = energy(k, h, dl, da, vac, 'k', k)
   print vac, e

from ase import *
from gpaw import *
from math import *

sqrt = 1.732050808

def energy(k, h, dl, da, dh, vac, var, num):
    slab = Atoms([Atom('Bi', (0.0000, 0.0000,      -dl)),
                  Atom('Bi', (da/2,   sqrt*da/6,    0.0)),
                  Atom('Bi', (da/2,   sqrt*da/2,   -dl)),
                  Atom('Bi', (2*da,   2*sqrt*da/3,  0.0)),
                  Atom('Bi', (da,     0.0,         -dl)),
                  Atom('Bi', (3*da/2, sqrt*da/6,    0.0)),
                  Atom('Bi', (3*da/2, sqrt*da/2,   -dl)),
                  Atom('Bi', (da,     2*sqrt*da/3,  0.0)),
                  Atom('Bi', (da,     sqrt*da/3,   -dl-dh)),
                  Atom('Bi', (da/2,   sqrt*da/6,   -dl*2-dh)),
                  Atom('Bi', (3*da/2, 5*sqrt*da/6, -dl-dh)),
                  Atom('Bi', (2*da,   2*sqrt*da/3, -dl*2-dh)),
                  Atom('Bi', (2*da,   sqrt*da/3,   -dl-dh)),
                  Atom('Bi', (3*da/2, sqrt*da/6,   -dl*2-dh)),
                  Atom('Bi', (5*da/2, 5*sqrt*da/6, -dl-dh)),
                  Atom('Bi', (da,     2*sqrt*da/3, -dl*2-dh))],
                  cell=((2*da,0,0), (da,sqrt*da,0), (0,0,1)),pbc=[True,True,False])
    slab.center(axis=2, vacuum=vac)
    calc = GPAW(h=h, kpts=(k, k, 1), parallel={'domain':8}, txt='Bi111'+var+"-"+str(num)+'.txt', xc='RPBE')
    slab.set_calculator(calc)
    e = slab.get_potential_energy()
    calc.write('Bi111'+var+"-"+str(num)+'.txt')
    return e

name = 'Bi111'

#f = open(name + '-dh.dat', 'w')
print 'Energy with respect to dh parameter'
for dh in [2.31,2.32,2.33,2.34,2.35,2.36,2.37,2.38,2.39,2.40,2.41,2.42]:
   k = 4
   h = 0.17
   da = 4.513
   dl = 1.65
   vac = 8
   e = energy(k, h, dl, da, dh, vac, 'dl', dl)
   print k, e
   #print >> f, k, e

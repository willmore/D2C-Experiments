from ase import *
from gpaw import *
from math import *

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
    calc = GPAW(h=h, kpts=(k, k, 1), parallel={'domain':8}, txt='Bi111'+var+"-"+str(num)+'.txt', xc='RPBE')
    slab.set_calculator(calc)
    e = slab.get_potential_energy()
    calc.write('Bi111'+var+"-"+str(num)+'.txt')
    return e

name = 'Bi111'

#f = open(name + '-da.dat', 'w')
print 'Energy with respect to da parameter'
for da in [4.5,4.505,4.51,4.515,4.52,4.525,4.53]:
   k = 4
   h = 0.17
   dk = 4.51
   vac = 12
   e = energy(k, h, dl, da, vac, 'da', da)
   print k, e
   #print >> f, k, e

#g = open(name + '-h.dat', 'w')
print 'Energy with respect to h value'
for h in [0.14,0.16,0.18,0.20]:
   k = 4
   dl = 1.682
   da = 4.513
   vac = 12
   e = energy(k, h, dl, da, vac, 'h', h)
   print vac, e
   #print >> g, vac, e


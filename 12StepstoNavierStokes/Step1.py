# Code to solve linear advection
# Linear  advection differential equation is du/dt + cdu/dx = 0
# Also known as the wave equation


import numpy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time,sys

nx = 71 #number of grid pts
#def linearconv(nx):
dx = 2/(nx-1) #distance b/w each grid pt, 2 is the domain size
nt = 1
dt = 0.25 #timestep
c = 1 #wavespeed
u = numpy.ones(nx) #numpy function ones, initializes an array of size nx filled with ones
u[int(0.5/dx):int(1/dx+1)] = 2
#plt.plot(numpy.linspace(0, 4, nx), u)
un = numpy.ones(nx)

for n in range(nt):
    un = u.copy()
    for i in range(1,nx):
        u[i] = un[i] - c*dt/dx*(un[i]-un[i-1])
    #plt.cla()
    plt.xlim(0,5)
    plt.ylim(0,3)
    plt.plot(numpy.linspace(0,5,nx),u)
    plt.draw()
    plt.pause(0.01)
plt.show()
print(u)


# Code to solve non linear convectio
# Linear  advection differential equation is du/dt + udu/dx = 0
# Also known as the a inviscid burger's equation


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time,sys
pi = 3.14
nx = 81 #number of grid pts
dx = 2*pi/(nx-1) #distance b/w each grid pt, 2 is the domain size
nt = 300
dt = 0.0030 #timestep
u = np.ones(nx) #np function ones, initializes an array of size nx filled with ones
x = np.linspace(0,2*pi,nx)
u = np.sin(x)
# plt.plot(x,u)
# plt.show()
un = np.ones(nx)
c = []
for n in range(nt):
    un = u.copy()
    for i in range(1,nx):
        c.append(un[i]*dt/dx)
        u[i] = un[i] - un[i] * dt / dx * (un[i] - un[i-1])
    plt.cla()
    #plt.xlim(0,6.28)
    #plt.ylim(1,2.1)
    plt.plot(x,u)
    plt.draw()
    plt.pause(0.000005)
print(max(c))
plt.show()

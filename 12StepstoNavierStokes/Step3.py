import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time,sys

nx = 21 #number of grid pts
dx = 2/(nx-1) #distance b/w each grid pt, 2 is the domain size
nt = 100
nu = 0.3
sigma = 0.45
dt = sigma*dx**2/nu #timestep

u = np.ones(nx) #np function ones, initializes an array of size nx filled with ones
u[int(0.5/dx):int(1/dx-1)] = 2
#plt.plot(np.linspace(0, 2, nx), u)
#plt.show()
un = np.ones(nx)
for n in range(nt):
    un = u.copy()
    for i in range(nx-1):
        u[i] = un[i] + nu*dt/dx**2*(un[i+1] - 2*un[i] + un[i-1])
    #plt.cla()
    plt.xlim(0,2)
    plt.ylim(1,2.1)
    plt.plot(np.linspace(0,2,nx),u)
    plt.draw()
    plt.pause(0.05)
plt.show()
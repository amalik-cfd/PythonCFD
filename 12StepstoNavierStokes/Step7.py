from mpl_toolkits.mplot3d import Axes3D

import numpy as np
from matplotlib import pyplot, cm


nx = 31
ny = 31
nt = 17
nu = 0.05
dx = 2 / (nx - 1)
dy = 2 / (ny - 1)
sigma = 0.25
dt = sigma*dx*dy/nu

x = np.linspace(0,2,nx)
y = np.linspace(0,2,ny)


u = np.ones((ny,nx))
un = np.ones((ny,nx))


fig = pyplot.figure(figsize=(11,7), dpi= 100)
ax = fig.add_subplot(projection='3d')
X, Y =np.meshgrid(x, y)
# surf = ax.plot_surface(X, Y, u, rstride=1, cstride=1, cmap=cm.viridis,linewidth=0, antialiased=False)


def diffuse(nt):
    u[int(.5 / dy):int(1 / dy + 1),int(.5 / dx):int(1 / dx + 1)] = 2  
    
    for n in range(nt + 1):
        un = u.copy()
        u[1:-1, 1:-1] = (un[1:-1,1:-1] + nu * dt / dx**2 * (un[1:-1, 2:] - 2 * un[1:-1, 1:-1] + un[1:-1, 0:-2]) + nu * dt / dy**2 * (un[2:,1: -1] - 2 * un[1:-1, 1:-1] + un[0:-2, 1:-1]))
        u[0, :] = 1
        u[-1, :] = 1
        u[:, 0] = 1
        u[:, -1] = 1
        pyplot.cla()
        pyplot.xlim(0,2.1)
        pyplot.ylim(0,2.1)
        ax.set_zlim(1, 2.5)
        surf = ax.plot_surface(X,Y,u,cmap = cm.viridis,rstride=2, cstride=2)
        ax.set_xlabel('$x$')
        ax.set_ylabel('$y$')
        pyplot.draw()
        pyplot.pause(0.0005)
    pyplot.show()

diffuse(50)
        

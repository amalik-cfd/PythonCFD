# Types of  PDEs 
# 1)2st order; a*du/dx+b*du/dy = K, always Hyperbolic, wave like properties
# 2) 2nd order, d2u/dt2 + c*d2u/dx2 = 0, classic wave equaition, hyperbolic
# 3) 2nd order, du/dt + d2u/dx2, unsteady heat equation, parabolic pde
# 4) 2nd order, d2u/dx2 + d2u/dy2 = 0 , steady state heat equation. elliptical diffusion also called laplacian equation


#Solving the laplace equation, also known as the steady state heat conduction equation


import numpy as np
from matplotlib import pyplot, cm
from mpl_toolkits.mplot3d import Axes3D

def plot2D(x,y,p):
    fig = pyplot.figure(figsize=(11, 7), dpi=100)
    ax = fig.add_subplot(projection='3d')
    X, Y = np.meshgrid(x, y)
    surf = ax.plot_surface(X, Y, p[:], rstride=1, cstride=1, cmap=cm.viridis, linewidth=0, antialiased=False)
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 1)
    ax.view_init(30, 225)
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    pyplot.show()

def laplace2d(p, y, dx, dy, l1norm_target):
    l1norm = 1
    pn = np.empty_like(p)
    k = []
    while l1norm > l1norm_target:
        pn = p.copy()
        p[1:-1, 1:-1] = ((dy**2 * (pn[1:-1, 2:] + pn[1:-1, 0:-2]) +
                         dx**2 * (pn[2:, 1:-1] + pn[0:-2, 1:-1])) /
                        (2 * (dx**2 + dy**2)))
            
        p[:, 0] = 0  # p = 0 @ x = 0
        p[:, -1] = y  # p = y @ x = 2
        p[0, :] = p[1, :]  # dp/dy = 0 @ y = 0
        p[-1, :] = p[-2, :]  # dp/dy = 0 @ y = 1
        l1norm = (np.sum(np.abs(p[:]) - np.abs(pn[:])) /
                np.sum(np.abs(pn[:])))
        k.append(l1norm)
    pyplot.plot(k)
    return p


nx = 31
ny = 31
c = 1
dx = 2/(nx-1)
dy = 2/(ny-1)

p = np.zeros((ny,nx))

x = np.linspace(0,2,nx)
y = np.linspace(0,1,ny)

p[:, 0] = 0  # p = 0 @ x = 0
p[:, -1] = y  # p = y @ x = 2
p[0, :] = p[1, :]  # dp/dy = 0 @ y = 0
p[-1, :] = p[-2, :]  # dp/dy = 0 @ y = 1


p = laplace2d(p, y, dx, dy, 1e-4)
plot2D(x,y,p)


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




#Using functional approach
def poisson2d(b,p, y, dx, dy, l1norm_target):
    l1norm = 1
    pn = p.copy()

    while l1norm > l1norm_target:
        pn = p.copy()
        p[1:-1, 1:-1] = ((dy**2 * (pn[1:-1, 2:] + pn[1:-1, 0:-2]) +
                         dx**2 * (pn[2:, 1:-1] + pn[0:-2, 1:-1])-(dx**2)*(dy**2)*b[1:-1,1:-1])/
                        (2 * (dx**2 + dy**2)))
            
        p[:, 0] = 0  # p = 0 @ x = 0
        p[:, -1] = 0  # p = 0 @ x = 2
        p[0, :] = 0  # p = 0 @ y = 0
        p[-1, :] = 0  # p = 0 @ y = 1
        l1norm = (np.sum(np.abs(p[:]) - np.abs(pn[:])) /
                np.sum(np.abs(pn[:])))
     
    return p

#Using within a script


nx = 50
ny = 50
dx = 2/(nx-1)
dy = 2/(ny-1)

nt = 300

p = np.zeros((ny,nx))

x = np.linspace(0,2,nx)
y = np.linspace(0,1,ny)


b = np.zeros((ny,nx))
b[int((ny+1)/4),int((nx+1)/4)] = 100
b[int((3*ny+1)/4),int((3*nx+1)/4)] = -100


# p[:, 0] = 0  # p = 0 @ x = 0
# p[:, -1] = 0  # p = 0 @ x = 2
# p[0, :] = 0  # p = 0 @ y = 0
# p[-1, :] = 0  # p = 0 @ y = 1


# laplace2d(b,p, y, dx, dy,0.001)

k = []
for it in range(nt):
    pd = p.copy()

    p[1:-1,1:-1] = (((pd[1:-1, 2:] + pd[1:-1, :-2]) * dy**2 +
                    (pd[2:, 1:-1] + pd[:-2, 1:-1]) * dx**2 -
                    b[1:-1, 1:-1] * dx**2 * dy**2) / 
                    (2 * (dx**2 + dy**2)))

    p[0, :] = 0
    p[ny-1, :] = 0
    p[:, 0] = 0
    p[:, nx-1] = 0
    l1norm = (np.sum(np.abs(p[:]) - np.abs(pd[:])) /
        np.sum(np.abs(pd[:])))
    k.append(l1norm)
pyplot.plot(k)
plot2D(x,y,p)


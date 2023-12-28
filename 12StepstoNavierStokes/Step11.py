import numpy as np
from matplotlib import pyplot, cm
from mpl_toolkits.mplot3d import Axes3D

nx = 41
ny = 41
nt = 500
nit = 50
c =1
dx = 2/(nx-1)
dy = 2/(ny-1)

rho = 1
nu = .1
dt = .001

x = np.linspace(0,2,nx)
y = np.linspace(0,2,ny)
X,Y = np.meshgrid(x,y)

u = np.zeros((ny, nx))
v = np.zeros((ny, nx))
p = np.zeros((ny, nx)) 
b = np.zeros((ny, nx))


#Creaating the  RHS of poisson equation
def build_up_b(b, rho, dt, u, v, dx, dy):
    b[1:-1, 1:-1] = (rho * (1 / dt * 
                    ((u[1:-1, 2:] - u[1:-1, 0:-2]) / 
                     (2 * dx) + (v[2:, 1:-1] - v[0:-2, 1:-1]) / (2 * dy)) -
                    ((u[1:-1, 2:] - u[1:-1, 0:-2]) / (2 * dx))**2 -
                      2 * ((u[2:, 1:-1] - u[0:-2, 1:-1]) / (2 * dy) *
                           (v[1:-1, 2:] - v[1:-1, 0:-2]) / (2 * dx))-
                          ((v[2:, 1:-1] - v[0:-2, 1:-1]) / (2 * dy))**2))
    
    
    return b

def plot2D(x,y,p):
    fig = pyplot.figure(figsize=(11, 7), dpi=100)
    ax = fig.add_subplot(projection='3d')
    X, Y = np.meshgrid(x, y)
    surf = ax.plot_surface(X, Y, p[:], rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 1)
    ax.view_init(30, 225)
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    pyplot.show()




def pressure_poisson(b,p, dx, dy):
    pn = p.copy()
    for n in range(nit):
        pn = p.copy()

        p[1:-1, 1:-1] = ((dy**2 * (pn[1:-1, 2:] + pn[1:-1, 0:-2]) +
                         dx**2 * (pn[2:, 1:-1] + pn[0:-2, 1:-1])-(dx**2)*(dy**2)*b[1:-1,1:-1])/
                        (2 * (dx**2 + dy**2)))
            
        p[:, -1] = p[0:,-2]  # dp/dx = 0 @ x = 2
        p[0,:] = p[1,:]  # dp/dy = 0 @ y = 0
        p[-1, :] = 0  # p = 0 @ y = 2
        p[:,0] = p[:,1]  # dp/dx = 0 @ x = 0
        
        return p


def cavity_flow(nt, u, v, dt, dx, dy, p, rho, nu):
    un = np.empty_like(u)
    vn =  np.empty_like(v)
    b = np.zeros((ny, nx))
    udiff = 6
    stepcount = 0

    while udiff > 10e-10:
    #for n in range(nt):
        un = u.copy()
        vn = v.copy()
        k = []
        b = build_up_b(b, rho, dt, u, v, dx, dy)
        k.append(np.max(b))
        p = pressure_poisson(b,p, dx, dy)
        print(np.max(p))
        u[1:-1, 1:-1] = (un[1:-1, 1:-1]-
                         un[1:-1, 1:-1] * dt / dx *
                        (un[1:-1, 1:-1] - un[1:-1, 0:-2]) -
                         vn[1:-1, 1:-1] * dt / dy *
                        (un[1:-1, 1:-1] - un[0:-2, 1:-1]) -
                         dt / (2 * rho * dx) * (p[1:-1, 2:] - p[1:-1, 0:-2]) +
                         nu * (dt / dx**2 *
                        (un[1:-1, 2:] - 2 * un[1:-1, 1:-1] + un[1:-1, 0:-2]) +
                         dt / dy**2 *
                        (un[2:, 1:-1] - 2 * un[1:-1, 1:-1] + un[0:-2, 1:-1])))

        v[1:-1,1:-1] = (vn[1:-1, 1:-1] -
                        un[1:-1, 1:-1] * dt / dx *
                       (vn[1:-1, 1:-1] - vn[1:-1, 0:-2]) -
                        vn[1:-1, 1:-1] * dt / dy *
                       (vn[1:-1, 1:-1] - vn[0:-2, 1:-1]) -
                        dt / (2 * rho * dy) * (p[2:, 1:-1] - p[0:-2, 1:-1]) +
                        nu * (dt / dx**2 *
                       (vn[1:-1, 2:] - 2 * vn[1:-1, 1:-1] + vn[1:-1, 0:-2]) +
                        dt / dy**2 *
                       (vn[2:, 1:-1] - 2 * vn[1:-1, 1:-1] + vn[0:-2, 1:-1])))

        u[0, :]  = 0
        u[:, 0]  = 0
        u[:, -1] = 0
        u[-1, :] = 1    # set velocity on cavity lid equal to 1
        v[0, :]  = 0
        v[-1, :] = 0
        v[:, 0]  = 0
        v[:, -1] = 0
        udiff = np.sqrt((np.sum(np.square(u - un)))/len(u))
        print(udiff)
        stepcount += 1 
    print(stepcount)       
        
    return u, v, p

nt = 100
u,v,p = cavity_flow(nt, u, v, dt, dx, dy, p, rho, nu)
#b = build_up_b(b, rho, dt, u, v, dx, dy)
#print(b)
#p = pressure_poisson(b,p, dx, dy, l1norm_target)
# fig = pyplot.figure(figsize=(11,7), dpi=100)
# # plotting the pressure field as a contour
# pyplot.contourf(X, Y, p, alpha=0.5, cmap=cm.viridis)  
# pyplot.colorbar()
# # plotting the pressure field outlines
# pyplot.contour(X, Y, p, cmap=cm.viridis)  
# # plotting velocity field
# pyplot.quiver(X[::2, ::2], Y[::2, ::2], u[::2, ::2], v[::2, ::2]) 
# pyplot.xlabel('X')
# pyplot.ylabel('Y')
# plot2D(x,y,p)
# print(np.min(p))

fig = pyplot.figure(figsize=(11, 7), dpi=100)
pyplot.contourf(X, Y, p, alpha=0.5, cmap=cm.viridis)
pyplot.colorbar()
pyplot.contour(X, Y, p, cmap=cm.viridis)
pyplot.streamplot(X, Y, u, v)
pyplot.xlabel('X')
pyplot.ylabel('Y');
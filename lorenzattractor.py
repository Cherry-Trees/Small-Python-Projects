'''Lorenz Attractor'''

import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def ode(r, t, rho, sigma, beta):
    return [sigma*(r[1]-r[0]), r[0]*(rho-r[2])-r[1], r[0]*r[1]-beta*r[2]]

dt = 0.05
deltat = np.arange(0, 60, dt)
solv = integrate.odeint(ode, [0,0.1,0], deltat, args=(28, 10, 8/3))

x_solv = [item[0] for item in solv]
y_solv = [item[1] for item in solv]
z_solv = [item[2] for item in solv]

fig = plt.figure()
ax = plt.subplot(projection="3d",
                 xlim=[-25,25], ylim=[-25,25], zlim=[-5,45],
                 xlabel="x(t)", ylabel="y(t)", zlabel="z(t)")

line, = ax.plot3D([],[],[], color="steelblue")
point, = ax.plot3D([],[],[],"o", color="steelblue")

def anim(frame):
    ax.set_title(f"t={frame*dt:.2f}")
    line.set_data_3d(x_solv[:frame], y_solv[:frame], z_solv[:frame])
    point.set_data_3d(x_solv[frame:frame+1], y_solv[frame:frame+1], z_solv[frame:frame+1])

an = FuncAnimation(fig, anim, frames=len(solv), interval=1)
plt.show()

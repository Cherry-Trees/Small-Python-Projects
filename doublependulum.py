'''
Double pendulum simulation
Assumes arms are rigid with m=0
'''
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from scipy.integrate import odeint

class Pendulum:

    def __init__(self, m, L, th0, thdot0=0, lda=0) -> None:
        self.m = m
        self.L = L
        self.th = th0
        self.thdot = thdot0
        self.lda = lda
        self.arm = None
        self.bob = None

def get_local_x(L, th):
    return L*np.sin(th)

def get_local_y(L, th):
    return -L*np.cos(th)

def ode(q, t, m1, m2, L1, L2, lda1, lda2):
    p1.th = q[0]
    p1.thdot = q[1]
    p2.th = q[2]
    p2.thdot = q[3]
    
    A = np.array([[(m1+m2)*(L1**2), m2*L1*L2*np.cos(p1.th-p2.th)], [m2*L1*L2*np.cos(p1.th-p2.th), m2*(L2**2)]])
    B = np.array([-m2*L1*L2*(p2.thdot**2)*np.sin(p1.th-p2.th)-(m1+m2)*L1*9.81*np.sin(p1.th) - p1.thdot*lda1,
                  m2*L1*L2*(p1.th**2)*np.sin(p1.th-p2.th)-m2*L2*9.81*np.sin(p2.th) - p2.thdot*lda2])
    
    angacc1, angacc2 = np.linalg.solve(A, B)
    angvel1 = p1.thdot
    angvel2 = p2.thdot
    return [angvel1, angacc1, angvel2, angacc2]

def anim(frame):
    ax.set_title(f"t={frame*dt:.2f}")

    p1.arm.set_data([0, get_local_x(p1.L, th1[frame])],[0, get_local_y(p1.L, th1[frame])])
    p2.arm.set_data([get_local_x(p1.L, th1[frame]), get_local_x(p1.L, th1[frame])+get_local_x(p2.L, th2[frame])],
                  [get_local_y(p1.L, th1[frame]), get_local_y(p1.L, th1[frame])+get_local_y(p2.L, th2[frame])])
    p1.bob.set_data(get_local_x(p1.L, th1[frame]), get_local_y(p1.L, th1[frame]))
    p2.bob.set_data(get_local_x(p1.L, th1[frame])+get_local_x(p2.L, th2[frame]), 
                  get_local_y(p1.L, th1[frame])+get_local_y(p2.L, th2[frame]))
    tracer.set_data(get_local_x(p1.L, th1[:frame])+get_local_x(p2.L, th2[:frame]),
                    get_local_y(p1.L, th1[:frame])+get_local_y(p2.L, th2[:frame]))
                  

p1 = Pendulum(1, 1, np.radians(90), lda=0.01)
p2 = Pendulum(1, 1, np.radians(60), lda=0.01)

fig = plt.figure()
ax = plt.axes(xlim=[-(p1.L+p2.L+0.2), p1.L+p2.L+0.2], ylim=[-(p1.L+p2.L+0.2), p1.L+p2.L+0.2], aspect="equal")

t = 20
dt = 0.033
deltat = np.arange(0, t, dt)

p1.arm, = ax.plot([0, get_local_x(p1.L, p1.th)],[0, get_local_y(p1.L, p1.th)], color="black")
p2.arm, = ax.plot([get_local_x(p1.L, p1.th), get_local_x(p1.L, p1.th)+get_local_x(p2.L, p2.th)],
                  [get_local_y(p1.L, p1.th), get_local_y(p1.L, p1.th)+get_local_y(p2.L, p2.th)], color="black")
p1.bob, = ax.plot(get_local_x(p1.L, p1.th), get_local_y(p1.L, p1.th),"o", color="red")
p2.bob, = ax.plot(get_local_x(p1.L, p1.th)+get_local_x(p2.L, p2.th), 
                  get_local_y(p1.L, p1.th)+get_local_y(p2.L, p2.th),"o", color="red")
tracer, = ax.plot([],[], alpha=0.33, color="red")

init_args = [p1.th, p1.thdot, p2.th, p2.thdot]
solv = odeint(ode, init_args, deltat, args=(p1.m, p2.m, p1.L, p2.L,p1.lda, p2.lda,))
th1, th2 = [], []

for i in range(len(solv)):
    th1.append(solv[i][0])
    th2.append(solv[i][2])

ani = FuncAnimation(fig, anim, frames=len(solv), interval=1)
plt.show() 

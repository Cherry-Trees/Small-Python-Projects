'''
Double pendulum simulation
Assumes arms are rigid with m=0
'''
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from scipy.integrate import odeint

class Pendulum:

    '''Pendulum odject with mass (m), length of rod (L), init-angle (th0), init-angvel (thdot0), friction coef (mu)'''
    def __init__(self, m, L, th0, thdot0=0, mu=0) -> None:
        self.m = m
        self.L = L
        self.th = th0
        self.thdot = thdot0
        self.mu = mu
        
        self.arm = None
        self.bob = None

# Returns the x value for a given L and theta
def get_local_x(L, th):
    return L*np.sin(th)

# Returns the y value for a given L and theta
def get_local_y(L, th):
    return -L*np.cos(th)


# Equations of motion for double pendulum system
def ode(q, t, m1, m2, L1, L2, mu1, mu2):
    
    # Extract q args
    p1.th = q[0]
    p1.thdot = q[1]
    p2.th = q[2]
    p2.thdot = q[3]
    
    # System of ODE's can be written in the form: Ax + B
    A = np.array([[(m1+m2)*(L1**2), m2*L1*L2*np.cos(p1.th-p2.th)], [m2*L1*L2*np.cos(p1.th-p2.th), m2*(L2**2)]])
    B = np.array([-m2*L1*L2*(p2.thdot**2)*np.sin(p1.th-p2.th)-(m1+m2)*L1*9.81*np.sin(p1.th)-p1.thdot*mu1,
                  m2*L1*L2*(p1.thdot**2)*np.sin(p1.th-p2.th)-m2*L2*9.81*np.sin(p2.th)-p2.thdot*mu2])
    
    # Solve system of equations for angacc's
    angacc1, angacc2 = np.linalg.solve(A, B)
    angvel1 = p1.thdot
    angvel2 = p2.thdot

    return [angvel1, angacc1, angvel2, angacc2]


# Updates window every frame
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
                  

# Construct Pendulum objects
p1 = Pendulum(m=1, L=1, th0=np.radians(90))
p2 = Pendulum(m=1, L=1, th0=np.radians(60))

# Window
fig = plt.figure()
ax = plt.axes(xlim=[-(p1.L+p2.L+0.2), p1.L+p2.L+0.2], ylim=[-(p1.L+p2.L+0.2), p1.L+p2.L+0.2], aspect="equal")

# Time interval and step
t = 20
dt = 0.033
deltat = np.arange(0, t, dt)

# Initialize Pendulum arms and bobs
p1.arm, = ax.plot([0, get_local_x(p1.L, p1.th)],[0, get_local_y(p1.L, p1.th)], color="black")
p2.arm, = ax.plot([get_local_x(p1.L, p1.th), get_local_x(p1.L, p1.th)+get_local_x(p2.L, p2.th)],
                  [get_local_y(p1.L, p1.th), get_local_y(p1.L, p1.th)+get_local_y(p2.L, p2.th)], color="black")
p1.bob, = ax.plot(get_local_x(p1.L, p1.th), get_local_y(p1.L, p1.th),"o", color="red")
p2.bob, = ax.plot(get_local_x(p1.L, p1.th)+get_local_x(p2.L, p2.th), 
                  get_local_y(p1.L, p1.th)+get_local_y(p2.L, p2.th),"o", color="red")
tracer, = ax.plot([],[], alpha=0.33, color="red")

# Pass p1 and p2 theta's and thetadot's into solver
init_args = [p1.th, p1.thdot, p2.th, p2.thdot]
solv = odeint(ode, init_args, deltat, args=(p1.m, p2.m, p1.L, p2.L, p1.mu, p2.mu,))
th1, th2 = [], []

# Extract thetas from solver array
for state in solv:
    th1.append(state[0])
    th2.append(state[2])

# Play animation
ani = FuncAnimation(fig, anim, frames=len(solv), interval=1)
plt.show() 

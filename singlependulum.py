'''
Demonstrates simple harmonic motion with a pendulum
Assumes pendulum arm is rigid with m=0
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from matplotlib.animation import FuncAnimation

class Space:
    
    '''World object with params: pendulum, delta-t, dt'''
    def __init__(self, pendulum, deltat=10, dt=0.02) -> None:
        self.pendulum = pendulum
        self.dt = dt
        self.deltat = np.arange(0, deltat, self.dt)
        
        self.g = 9.81
        self.x0, self.y0 = self.get_coords(self.pendulum.th0)
        
        # Evaluate the ODE numerically
        self.solv = integrate.odeint(self.ode, [self.pendulum.th0, self.pendulum.v0], self.deltat)
        
        self.fig = plt.figure(figsize=(10,8))
        self.axs = plt.subplot(3,3,1)
        self.axv = plt.subplot(3,3,2)
        self.axa = plt.subplot(3,3,3)
        self.axp = plt.subplot(3,3,(4,9))
        self.axp.set_aspect("equal")
        
        self.axs.axhline(y=0, color="black", linestyle = ':')
        self.axs.axvline(x=0, color="black", linestyle = ':')
        self.axv.axhline(y=0, color="black", linestyle = ':')
        self.axv.axvline(x=0, color="black", linestyle = ':')
        self.axa.axhline(y=0, color="black", linestyle = ':')
        self.axa.axvline(x=0, color="black", linestyle = ':')
        
        self.axp.set_xlim(-1.2*self.pendulum.L, 1.2*self.pendulum.L)
        self.axp.set_ylim(-1.2*self.pendulum.L, 1.2*self.pendulum.L)

        self.axs.set_xlim(0, len(self.solv))
        self.axs.set_ylim(-10,10)
        self.axs.set_title(r"${\theta}$(t)")
        self.axs.grid()

        self.axv.set_xlim(0, len(self.solv))
        self.axv.set_ylim(-10,10)
        self.axv.set_title(r"$\dot{\theta}$(t)")
        self.axv.grid()

        self.axa.set_xlim(0, len(self.solv))
        self.axa.set_ylim(-10,10)
        self.axa.set_title(r"$\ddot{\theta}$(t)")
        self.axa.grid()
        
        self.arm, = self.axp.plot([],[])
        self.circle, = self.axp.plot([],[],"o", markersize=self.pendulum.r)
        
        self.t_data = []
        self.s_data = []
        self.v_data = [] 
        self.a_data = []
        self.s_line, = self.axs.plot([],[])
        self.v_line, = self.axv.plot([],[])
        self.a_line, = self.axa.plot([],[])
        
    # Returns a set of x and y coordinates for the given angle theta
    def get_coords(self, th) -> tuple:
        return self.pendulum.L*np.sin(th), -self.pendulum.L*np.cos(th)
    
    # Second order ODE for equation of motion for pendulum
    # mθ''(t) + λθ'(t) + mgLsin(θ) = 0
    def ode(self, q:list, t) -> list:
        return [q[1], -(self.pendulum.l/self.pendulum.m*q[1]) - (self.g/self.pendulum.L*np.sin(q[0]))]
    
    # Initialize arm and circle
    def anim_init(self):
        self.arm.set_data([0,self.x0], [0,self.y0])
        self.circle.set_data(self.x0, self.y0)
        

    def anim(self, frame):
        
        # Pendulum
        self.x, self.y = self.get_coords(self.solv[frame][0])
        self.arm.set_data([0,self.x], [0,self.y])
        self.circle.set_data(self.x, self.y)
        
        # Graphs
        self.t_data.append(frame)
        self.s_data.append(self.solv[frame][0])
        self.v_data.append(self.solv[frame][1])
        self.a_data.append(-(self.pendulum.l/self.pendulum.m*self.solv[frame][1]) - (self.g/self.pendulum.L*np.sin(self.solv[frame][0])))
        
        self.s_line.set_data(self.t_data, self.s_data)
        self.v_line.set_data(self.t_data, self.v_data)
        self.a_line.set_data(self.t_data, self.a_data)
        
    
    def act(self):
        self.an = FuncAnimation(
            self.fig, 
            self.anim, 
            init_func=self.anim_init, 
            frames=len(self.solv), 
            repeat=False, 
            interval=1
        )
        plt.show()
        
    
class Pendulum:
    
    '''Pendulum object with params: mass, arm length, v-initial, theta-initial, coef of static friction, radius'''
    def __init__(self, m=1, L=1, v0=0, th0=np.radians(60), l=0, r=15) -> None:
        self.m = m
        self.L = L
        self.th0 = th0
        self.v0 = v0
        self.l = l
        self.r = r
    
    
pendulum = Pendulum(L=1, th0=np.radians(90), l=0.35, v0=0)
space = Space(pendulum, deltat=10, dt=0.05)
space.act()

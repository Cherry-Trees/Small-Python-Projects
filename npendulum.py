'''
n-pendulum simulation using Lagrangian formulation
Assumes pendulum arms are rigid and m=0
'''
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from scipy import integrate

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
        self.x_data = []
        self.y_data= []


class Space:

    g = 9.81
    def __init__(self, t, dt) -> None:
        self.pl = []
        self.n = 0
        self.Ltot = 0
        self.deltat = np.arange(0, t, dt)


    def add_pendulum(self, p:Pendulum):
        self.pl.append(p)
        self.n += 1
        self.Ltot += p.L
    

    def init_anim(self):
        colors = ["crimson", "chocolate", "darkgoldenrod", "seagreen", "dodgerblue", "darkviolet"]
        self.fig = plt.figure(facecolor="grey")
        self.ax = plt.axes(xlim=[-self.Ltot*1.2, self.Ltot*1.2],
                           ylim=[-self.Ltot*1.2, self.Ltot*1.2],
                           aspect="equal", facecolor="lightgrey")

        self.tracer, = self.ax.plot([],[], alpha=0.33, color=colors[self.n%6-1])
        for i in range(self.n):
            self.pl[i].arm, = self.ax.plot([],[], color="black")
        for i in range(self.n):
            self.pl[i].bob, = self.ax.plot([],[], "o", markersize=np.log(self.pl[i].m+1)*7.33, color=colors[i%6])
        
        
    def get_xy(self, th_data):
        x, y = 0, 0
        coors = []
        for i in range(len(th_data)):
            x += self.pl[i].L*np.sin(th_data[i])
            y -= self.pl[i].L*np.cos(th_data[i])
            coors.append([x, y])     
        return coors
    
    
    def solve(self):
        init_args = np.array([[p.th for p in self.pl], [p.thdot for p in self.pl]]).flatten()
        solv = integrate.odeint(func=self.ode, y0=init_args, t=self.deltat)

        for state in solv:
            coor_list = self.get_xy(state[:self.n])
            for i in range(self.n):
                self.pl[i].x_data.append(coor_list[i][0])
                self.pl[i].y_data.append(coor_list[i][1])
    

    def anim(self, frame):
        self.ax.set_title(f"t={self.deltat[frame]:.2f}")
        for i in range(self.n):
            self.pl[i].bob.set_data(self.pl[i].x_data[frame:frame+1], self.pl[i].y_data[frame:frame+1])
            self.pl[i].arm.set_data([(self.pl[i-1].x_data[frame:frame+1]) if i-1>-1 else [0], self.pl[i].x_data[frame:frame+1]], 
                                      [self.pl[i-1].y_data[frame:frame+1] if i-1>-1 else [0], self.pl[i].y_data[frame:frame+1]])
        self.tracer.set_data(self.pl[-1].x_data[:frame], self.pl[-1].y_data[:frame])
    

    def run(self):
        self.init_anim()
        self.solve()
        ani = FuncAnimation(self.fig, self.anim, frames=len(self.deltat), interval=1)
        plt.show()


    def ode(self, q, t):
        
        def A():
            A = []
            for i in range(self.n):
                row = []
                for k in range(self.n):
                    mqi = 0
                    for q in range(self.n):
                        if q>=k:
                            mqi += self.pl[q].m*int(i<=q)
                    row.append(mqi*self.pl[i].L*self.pl[k].L*np.cos(self.pl[i].th-self.pl[k].th))         
                A.append(row)
            return A
    
        def B():
            B = []
            for i in range(self.n):
                B_i = 0
                for k in range(self.n):    
                    mqi = 0
                    B_i -= (self.g*self.pl[i].L*np.sin(self.pl[i].th)*self.pl[k].m*int(i<=k))+self.pl[i].mu*self.pl[i].thdot
                    for q in range(self.n):
                        if q>=k:
                            mqi += self.pl[q].m*int(i<=q)
                    B_i -= (mqi*self.pl[i].L*self.pl[k].L*np.sin(self.pl[i].th-self.pl[k].th)*(self.pl[k].thdot**2))
                B.append(B_i)
            return B
        
        for i in range(self.n):
            self.pl[i].th = q[i]
            self.pl[i].thdot = q[i+self.n]
        
        thddot_data = np.linalg.solve(A(), B())
        thdot_data = np.array([p.thdot for p in self.pl])
        return np.array([thdot_data, thddot_data]).flatten()
            

w = Space(t=20, dt=0.033)
w.add_pendulum(Pendulum(m=1, L=1, th0=np.radians(90), thdot0=0, mu=0.0))
w.add_pendulum(Pendulum(m=1, L=1, th0=np.radians(90), thdot0=0, mu=0.0))
w.add_pendulum(Pendulum(m=1, L=1, th0=np.radians(90), thdot0=0, mu=0.0))
w.add_pendulum(Pendulum(m=1, L=1, th0=np.radians(90), thdot0=0, mu=0.0))
w.add_pendulum(Pendulum(m=1, L=1, th0=np.radians(90), thdot0=0, mu=0.0))
w.run()

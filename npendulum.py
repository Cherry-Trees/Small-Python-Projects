'''
n-pendulum simulation
Assumes pendulum arms are rigid and m=0
'''
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from scipy import integrate

class Pendulum:

    '''Pendulum odject with mass (m), length of rod (L), init-angle (th0), init-angvel (thdot0)'''
    def __init__(self, m, L, th0, thdot0=0, mu=0) -> None:
        self.m = m
        self.L = L
        self.th = th0
        self.thdot = thdot0

        self.arm = None
        self.bob = None

        self.x_data = []
        self.y_data= []


class Space:

    g = 9.81
    def __init__(self, t, dt) -> None:
        self.pl = []
        self.n = 0
        self.deltat = np.arange(0, t, dt)

    def add_pendulum(self, p:Pendulum):
        self.pl.append(p)
        self.n += 1
    
    def init_anim(self):
        self.fig = plt.figure()
        self.ax = plt.axes(xlim=[-self.n*1.2, self.n*1.2],
                           ylim=[-self.n*1.2, self.n*1.2],
                           aspect="equal")

        self.tracer, = self.ax.plot([],[], alpha=0.33, color="red")
        for p in self.pl:
            p.arm, = self.ax.plot([],[], color="black")
            p.bob, = self.ax.plot([],[], "o", color="red")
        
        
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


    def A(self):
        A = []
        col_sum_2Darr = []
        row_sum_1Darr = []
        for i in range(self.n):
            row = []
            row_sum = 0
            col_sum_1Darr = []
            for k in range(self.n):
                mqi = 0
                for q in range(self.n):
                    if q>=k:
                        mqi += self.pl[q].m*int(i<=q)
                col_sum_1Darr.append(mqi*self.pl[i].L*self.pl[k].L*np.cos(self.pl[i].th-self.pl[k].th))         
            col_sum_2Darr.append(col_sum_1Darr)
            row_sum = sum(row)
            row_sum_1Darr.append(row_sum)

        for i in range(self.n):
            A_row = []
            for j in range(self.n):
                if i==j:
                    A_row.append(col_sum_2Darr[i][j] + row_sum_1Darr[i])
                else:
                    A_row.append(col_sum_2Darr[i][j])
            A.append(A_row)
        return A
    

    def B(self):
        B = []
        for i in range(self.n):
            B_i = 0
            for k in range(self.n):    
                mqi = 0
                B_i -= (self.g*self.pl[i].L*np.sin(self.pl[i].th)*self.pl[k].m*int(i<=k))
                for q in range(self.n):
                    if q>=k:
                        mqi += self.pl[q].m*int(i<=q)
                B_i -= (mqi*self.pl[i].L*self.pl[k].L*np.sin(self.pl[i].th-self.pl[k].th)*(self.pl[k].thdot**2))
            B.append(B_i)
        
        return B


    def ode(self, q, t):
        for i in range(self.n):
            self.pl[i].th = q[i]
            self.pl[i].thdot = q[i+self.n]
        
        A = self.A()
        B = self.B()
  
        thddot_data = np.linalg.solve(A, B)
        thdot_data = np.array([p.thdot for p in self.pl])
        derivs = np.array([thdot_data, thddot_data]).flatten()
        return derivs
            

w = Space(t=15, dt=0.033)
w.add_pendulum(Pendulum(1, 1, np.radians(90)))
w.add_pendulum(Pendulum(1, 1, np.radians(90)))
w.add_pendulum(Pendulum(1, 1, np.radians(90)))
w.add_pendulum(Pendulum(1, 1, np.radians(90)))
w.add_pendulum(Pendulum(1, 1, np.radians(90)))
w.run()

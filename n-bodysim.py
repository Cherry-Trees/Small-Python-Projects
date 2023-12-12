'''Simulates the forces of gravity of an n body system in a vacuum'''

import numpy as np
import scipy as sci
from scipy import integrate
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

class Body:

    def __init__(self, m, x0, y0, z0, vx0=0, vy0=0, vz0=0, point_alpha=1, line_alpha=1, size=5.67) -> None:
        self.m = m
        self.r = np.array([x0, y0, z0])
        self.vr = np.array([vx0, vy0, vz0])

        self.point = None
        self.line = None
        self.point_alpha = point_alpha
        self.line_alpha = line_alpha
        self.size = size
        

class Space:

    G = 6.67e-11
    def __init__(self, t, dt=0.05, xlim=[-1,1], ylim=[-1,1], zlim=[-1,1]) -> None:
        self.bl = []
        self.n = 0
        self.t = t
        self.dt = dt
        self.delta_t = np.arange(0, self.t, self.dt)

        self.fig = plt.figure()
        self.ax = plt.subplot(projection="3d")
        self.ax.set_xlim(xlim)
        self.ax.set_ylim(ylim)
        self.ax.set_zlim(zlim)
        self.ax.set_xlabel("x(t)")
        self.ax.set_ylabel("y(t)")
        self.ax.set_zlabel("z(t)")

        
    def addBody(self, body:Body) -> None:
        self.bl.append(body)
        self.n += 1
        body.line, = self.ax.plot3D([],[],[], alpha=body.line_alpha)
        body.point, = self.ax.plot3D([],[],[], "o", alpha=body.point_alpha, markersize=body.size)


    def addSolarSystem(self) -> None:
        sun = Body(m=1.989e30, size=6, x0=0, y0=0, z0=0, vx0=0, vy0=0, vz0=0)
        earth = Body(m=5.97e24, size=1.4, x0=1.4959e11, y0=0, z0=0, vx0=0, vy0=30000, vz0=0)
        mercury = Body(m=3.285e23, size=1.22, x0=6.7233e10, y0=0, z0=0, vx0=0, vy0=47000, vz0=0)
        venus = Body(m=4.867e24, size=1.35, x0=1.082e11, y0=0, z0=0, vx0=0, vy0=35020, vz0=0)
        mars = Body(m=6.41693e23, size=1.42, x0=2.3142e11, y0=0, z0=0, vx0=0, vy0=24077, vz0=0)
        jupiter = Body(m=1.899e27, size=2, x0=7.4435e11, y0=0, z0=0, vx0=0, vy0=13070, vz0=0)
        saturn = Body(m=5.683e26, size=1, x0=1.4e12, y0=0, z0=0, vx0=0, vy0=9680, vz0=0)
        uranus = Body(m=8.681e25, size=1, x0=2.934e12, y0=0, z0=0, vx0=0, vy0=6810, vz0=0)
        neptune = Body(m=1.024e26, size=1, x0=4.4726e12, y0=0, z0=0, vx0=0, vy0=5400, vz0=0)
        self.addBody(sun)
        self.addBody(earth)
        self.addBody(mercury)
        self.addBody(venus)
        self.addBody(mars)
        self.addBody(jupiter)
        self.addBody(saturn)
        self.addBody(uranus)
        self.addBody(neptune)

    @staticmethod
    def getRandomBody() -> Body:
        return Body(1, random.uniform(-1,1), random.uniform(-1,1), random.uniform(-1,1))

    
    def _solve(self) -> None:
        self.x_solv = np.empty(self.n).tolist()
        self.y_solv = np.empty(self.n).tolist()
        self.z_solv = np.empty(self.n).tolist()
        
        init_args = np.array([[body.r for body in self.bl], [body.vr for body in self.bl]]).flatten()
        self.solv = integrate.odeint(func=self._ode, y0=init_args, t=self.delta_t).flatten()

        for i in range(self.n):
            self.x_solv[i] = self.solv[i*3::self.n*6]
            self.y_solv[i] = self.solv[i*3+1::self.n*6]
            self.z_solv[i] = self.solv[i*3+2::self.n*6]    
            

    def _ode(self, q, t) -> np.ndarray:
        drdt_data = np.zeros(self.n).tolist()
        dvdt_data = np.zeros(self.n).tolist()
        dvdt_sep_data = np.zeros([self.n, self.n-1]).tolist()

        for i in range(self.n):
            self.bl[i].r = q[3*i:3*(i+1)]
            self.bl[i].vr = q[3*(i+self.n):3*(i+self.n+1)]
        
        for i in range(self.n):
            for j in range(self.n-1):
                dvdt_sep_data[i][j] = (Space.G*self.bl[i-j-1].m*(self.bl[i-j-1].r - self.bl[i].r)) / (sci.linalg.norm(self.bl[i].r - self.bl[i-j-1].r)**3)

            dvdt_sep_data[i] = np.array(dvdt_sep_data[i])
            dvdt_data[i] = dvdt_sep_data[i].sum(axis=0)
            drdt_data[i] = self.bl[i].vr
            
        return np.array([drdt_data, dvdt_data]).flatten()
            

    def _anim(self, frame) -> None:
        self.ax.set_title("t=%.2fs" % (frame*self.dt))
        for i in range(self.n):
            self.bl[i].point.set_data_3d(self.x_solv[i][frame:frame+1], self.y_solv[i][frame:frame+1], self.z_solv[i][frame:frame+1])
            self.bl[i].line.set_data_3d(self.x_solv[i][:frame], self.y_solv[i][:frame], self.z_solv[i][:frame])
    

    def run(self) -> None:
        self._solve()
        ani = FuncAnimation(self.fig, self._anim, frames=int(self.t/self.dt), interval=1)
        plt.show()


space = Space(t=20, dt=0.05)
space.addBody(Body(5e9, -0.1, -0.9, -0.5))
space.addBody(Body(5e9, 0.7, 0.1, 0.4, -0.0, 0.0, 0.1))
space.addBody(Body(5e9, -1.2, 0.6, 0, -0.0, -0.0, -0.1))
space.run()

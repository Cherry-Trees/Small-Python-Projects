'''Simulates the forces of gravity of an n body system in a vacuum'''

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from random import uniform

class Body:

    def __init__(self, m, x0, y0, z0, vx0=0, vy0=0, vz0=0, point_alpha=1, line_alpha=1, size=5.67) -> None:
        self.m = m

        # Construct arrays that serve as position and velocity vectors containing x, y, and z components
        self.r = np.array([x0, y0, z0])
        self.vr = np.array([vx0, vy0, vz0])
        
        self.point = None
        self.line = None
        self.point_alpha = point_alpha
        self.line_alpha = line_alpha
        self.size = size
        

class Space:
    
    def __init__(self, t, dt=0.05, G=6.67e-11, xlim=[-1,1], ylim=[-1,1], zlim=[-1,1]) -> None:

        # Construct empty list to hold Body objects
        self.bl = []
        self.n = 0
        self.tf = t
        self.dt = dt
        self.t = np.arange(0, t, dt)
        self.G = G

        
    def addBody(self, body:Body) -> None:
        '''Add a Body object to the system.'''
        self.bl.append(body)
        self.n += 1


    def addSolarSystem(self) -> None:
        '''Experimental. Increase xlim, ylim, zlim values.'''
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
        '''Return a Body object with random parameters'''
        return Body(1, uniform(-1,1), uniform(-1,1), uniform(-1,1))

    
    def _solve(self) -> None:
        
        # Construct empty lists to contain lists of x, y, and z coordinates for each Body for each frame
        self.x_state = np.empty(self.n).tolist()
        self.y_state = np.empty(self.n).tolist()
        self.z_state = np.empty(self.n).tolist()
        
        # Initial state
        state0 = np.array([[body.r for body in self.bl], [body.vr for body in self.bl]]).flatten()

        # Solve ODE system numerically over the given time interval t
        states = odeint(func=self._ode, y0=state0, t=self.t).flatten()

        # Extract x, y, and z coordinates from states array
        for i in range(self.n):
            self.x_state[i] = states[i*3::self.n*6]
            self.y_state[i] = states[i*3+1::self.n*6]
            self.z_state[i] = states[i*3+2::self.n*6]    
            
    # Iterates over a time interval t and returns an array S containing the current position and velocity vectors of the system.
    def _ode(self, S, t) -> np.ndarray:
        drdt_data = np.zeros(self.n).tolist()
        dvdt_data = np.zeros(self.n).tolist()

        # dvdt_sep_data holds each of the values for the forces between any two Bodies.
        # There are n x n-1 relationships for any given system.
        dvdt_sep_data = np.zeros([self.n, self.n-1]).tolist()


        # Update each Body's position and velocity vectors to the newest state
        for i in range(self.n):
            self.bl[i].r = S[3*i:3*(i+1)]
            self.bl[i].vr = S[3*(i+self.n):3*(i+self.n+1)]
        
        # Iterate through each Body for each Body, i and j cannot be equal.
        for i in range(self.n):
            for j in range(self.n-1):
                dvdt_sep_data[i][j] = (self.G*self.bl[i-j-1].m*(self.bl[i-j-1].r - self.bl[i].r)) / (np.linalg.norm(self.bl[i].r - self.bl[i-j-1].r)**3)

            # Convert to array, then sum up all the forces on each Body
            dvdt_sep_data[i] = np.array(dvdt_sep_data[i])
            dvdt_data[i] = dvdt_sep_data[i].sum(axis=0)
            drdt_data[i] = self.bl[i].vr
        
        # Return the next state
        return np.array([drdt_data, dvdt_data]).flatten()
    
    
    def _init_anim(self, xlim, ylim, zlim) -> None:

        # 3D plot
        self.fig = plt.figure()
        self.ax = plt.subplot(projection="3d")
        self.ax.set_xlim(xlim)
        self.ax.set_ylim(ylim)
        self.ax.set_zlim(zlim)
        self.ax.set_xlabel("x(t)")
        self.ax.set_ylabel("y(t)")
        self.ax.set_zlabel("z(t)")

        # Construct Line3DCollection objects and initialize them to line and point attributes
        for body in self.bl:
            body.line, = self.ax.plot3D([],[],[], alpha=body.line_alpha)
            body.point, = self.ax.plot3D([],[],[], "o", alpha=body.point_alpha, markersize=body.size)

    
    def _init_plot(self, xlim, ylim, zlim) -> None:

        # Axes and 3D plot
        fig = plt.figure(figsize=(12,8))
        x_ax = plt.subplot(3,3,1)
        y_ax = plt.subplot(3,3,2)
        z_ax = plt.subplot(3,3,3)
        param_ax = plt.subplot(3,3,(4,9), projection="3d")

        # x(t) plot
        x_ax.set_xlim(0, self.tf)
        x_ax.set_ylim(xlim)
        x_ax.grid()
        x_ax.set_xlabel("t")
        x_ax.set_ylabel("x(t)")
        x_ax.set_title("x(t)")

        # y(t) plot
        y_ax.set_xlim(0, self.tf)
        y_ax.set_ylim(ylim)
        y_ax.grid()
        y_ax.set_xlabel("t")
        y_ax.set_ylabel("y(t)")
        y_ax.set_title("y(t)")

        # z(t) plot
        z_ax.set_xlim(0, self.tf)
        z_ax.set_ylim(zlim)
        z_ax.grid()
        z_ax.set_xlabel("t")
        z_ax.set_ylabel("z(t)")
        z_ax.set_title("z(t)")

        # 3D plot
        param_ax.set_xlim(xlim)
        param_ax.set_ylim(ylim)
        param_ax.set_zlim(zlim)
        param_ax.grid()
        param_ax.set_xlabel("x(t)")
        param_ax.set_ylabel("y(t)")
        param_ax.set_zlabel("z(t)")

        # Plot data
        for i in range(self.n):
            x_ax.plot(self.t, self.x_state[i][:])
            y_ax.plot(self.t, self.y_state[i][:])
            z_ax.plot(self.t, self.z_state[i][:])
            param_ax.plot3D(self.x_state[i][:], 
                       self.y_state[i][:], 
                       self.z_state[i][:])
            

    # Update window every frame
    def _update(self, frame) -> None:
        self.ax.set_title("t=%.2fs" % (frame*self.dt))
        for i in range(self.n):
            self.bl[i].point.set_data_3d(self.x_state[i][frame:frame+1], self.y_state[i][frame:frame+1], self.z_state[i][frame:frame+1])
            self.bl[i].line.set_data_3d(self.x_state[i][:frame], self.y_state[i][:frame], self.z_state[i][:frame])
    

    def run(self, mode="animate", xlim=(-1,1), ylim=(-1,1), zlim=(-1,1)) -> None:
        
        '''
        Run simulation based on mode selected:\n
        mode="animate": Animates the bodies\n
        mode="plot": Plots each of the body's coordinates over time
        '''
        
        self._solve()
        
        if mode == "animate":
            self._init_anim(xlim, ylim, zlim)
            ani = FuncAnimation(self.fig, self._update, frames=int(self.tf/self.dt), interval=1)
        
        elif mode == "plot":
            self._init_plot(xlim, ylim, zlim)
        
        else:
            raise NameError(f"{mode} is not an option.")

        plt.show()


def main():
    space = Space(t=20, dt=0.05, G=6.67e-11)
    space.addBody(Body(m=5e9, x0=-0.1, y0=-0.9, z0=-0.5, vx0=0.0, vy0=0.0, vz0=0.0))
    space.addBody(Body(m=5e9, x0=0.7, y0=0.1, z0=0.4, vx0=-0.0, vy0=0.0, vz0=0.1))
    space.addBody(Body(m=5e9, x0=-1.2, y0=0.6, z0=0, vx0=-0.0, vy0=-0.0, vz0=-0.1))
    space.run(mode="animate", xlim=(-1,1), ylim=(-1,1), zlim=(-1,1))

if __name__ == "__main__":
    main()

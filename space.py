import numpy as np
import scipy as sci
from scipy import integrate
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from random import uniform

class Space:

    def __init__(self, bodyList, deltat, dt=0.05, epsilon=0.0, xplotview=[-1,1], yplotview=[-1,1], zplotview=[-1,1]) -> None:
    
        # Create 3D figure
        self.fig = plt.figure()
        self.ax = plt.subplot(projection="3d")
        self.ax.set_xlim(xplotview[0], xplotview[1])
        self.ax.set_ylim(yplotview[0], yplotview[1])
        self.ax.set_zlim(zplotview[0], zplotview[1])
        self.ax.set_xlabel("x(t)")
        self.ax.set_ylabel("y(t)")
        self.ax.set_zlabel("z(t)")
        
        self.line_data = []
        self.point_data = []

        self.bodyList = bodyList
        self.dt = dt
        self.deltat = np.arange(0, deltat, self.dt)
        self.G = 0.1
        self.epsilon = epsilon

        self.m_data = []
        self.r_data, self.dr_data = [],[]
        self.dvdt_data = []
        self.drdt_data = []
        self.t_data = []

        self.dvdt_sep_data = []
        self.x_solv, self.y_solv, self.z_solv = [],[],[]

        # Extract starting positions and velocities from each Body
        for body in bodyList:
            self.m_data.append(body.m)
            self.r_data.append([body.x0, body.y0, body.z0])
            self.dr_data.append([body.dx0, body.dy0, body.dz0])

            self.dvdt_data.append(0)
            self.dvdt_sep_data.append([])
            self.drdt_data.append(0)

            body.line, = self.ax.plot3D([],[],[])
            body.point, = self.ax.plot3D([],[],[],"o")
            self.line_data.append(body.line,)
            self.point_data.append(body.point,)

            self.x_solv.append([])
            self.y_solv.append([])
            self.z_solv.append([])

        # Add n-1 zeros to each dvdt_separate list (number of relationships per Body = n-1)
        for i in range(len(self.bodyList)):
            for j in range(len(self.bodyList)-1):
                self.dvdt_sep_data[i].append(0)
                
        # Prepare arrays for ODE solver
        self.r_data = np.array(self.r_data, float)
        self.dr_data = np.array(self.dr_data, float)

        self.init_params = np.array([self.r_data, self.dr_data])
        self.init_params = self.init_params.flatten()
        
        # Scipy ODE solver
        self.solv = integrate.odeint(self.ode, y0=self.init_params, t=self.deltat, args=(self.m_data,))
        self.r_solv = []
        
        # Extract position data from ODE return data
        for i in range(len(self.solv)):
            self.r_solv.append(self.solv[i][:len(bodyList)*3])
    
        # Extract x,y,z data from r_data
        for i in range(len(self.r_solv)):
            for j in range(len(self.bodyList)):
                self.x_solv[j].append(self.r_solv[i][j*3])
                self.y_solv[j].append(self.r_solv[i][j*3+1])
                self.z_solv[j].append(self.r_solv[i][j*3+2])

        
        
    # Solves a set of 3 Second order Differential Equations per Body object
    # Return all of the Body objects' x,y,z coordinates over the given time interval deltat
    def ode(self, q, t, m_data):
        
        # Extract input data y0
        for i in range(len(self.bodyList)):
            self.r_data[i] = q[3*i:3*(i+1)]
            self.dr_data[i] = q[3*(i+len(self.bodyList)):3*(i+len(self.bodyList)+1)]
        
        # dvdt_sep_data holds pieces of each ODE corresponding to the relationships to each Body
        # I.e., turns the set of 3*n ODE's into a (3*n x n-1) matrix of ODE's
        for i in range(len(self.bodyList)):
            for j in range(len(self.bodyList)-1):
                if sci.linalg.norm(self.r_data[i] - self.r_data[i-j-1]) > self.epsilon:
                    self.dvdt_sep_data[i][j] = ((0.2*m_data[i-j-1]*(self.r_data[i-j-1] - self.r_data[i])) / sci.linalg.norm(self.r_data[i] - self.r_data[i-j-1])**3)
                
                else:
                    self.dvdt_sep_data[i][j] = self.r_data[i]
                    
            # Turn each Body's corresponding dvdt_sep_data into a numPy array for matrix addition
            # Set Body's dvdt to the sum of all x,y,z component vectors in its corresponding dvdt_sep
            self.dvdt_sep_data[i] = np.array(self.dvdt_sep_data[i])
            self.dvdt_data[i] = self.dvdt_sep_data[i].sum(axis=0)
            
            # Variable substitution to make this a set of 6 First order Differential Equations per Body
            self.drdt_data[i] = 7.24*self.dr_data[i]
        
        # Package drdt and dvdt data for all Bodies to be sent back through as y0
        self.derivs = np.array([self.drdt_data, self.dvdt_data])
        self.derivs = self.derivs.flatten()
        return self.derivs
    
    
    # Update visuals per frame
    # Points and Lines animate the data from ODE's
    def anim(self, frame):
        self.t_data.append(frame)
        self.ax.set_title(f"t={frame*self.dt:.2f}")

        self.ax.view_init(30, (360/750)*frame)

        for i in range(len(self.bodyList)):
            self.line_data[i].set_data_3d(self.x_solv[i][:frame], self.y_solv[i][:frame], self.z_solv[i][:frame])
            self.point_data[i].set_data_3d(self.x_solv[i][frame:frame+1], self.y_solv[i][frame:frame+1], self.z_solv[i][frame:frame+1])

            
    # Run animation
    def act(self):
        self.an = FuncAnimation(self.fig, self.anim, frames=len(self.solv), interval=1)
        plt.show()



class Body:

    def __init__(self, m, x0, y0, z0, dx0=0, dy0=0, dz0=0) -> None:
        self.m = m
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.dx0 = dx0
        self.dy0 = dy0
        self.dz0 = dz0

        self.line = None
        self.point = None

        
def getRandomBodies(n,m=[10,10],x=[-5,5],y=[-5,5],z=[-5,5],dx=[-0.05,0.05],dy=[-0.05,0.05],dz=[-0.05,0.05]):
    bList = []

    for _ in range(n):
        b = Body(uniform(m[0],m[1]),uniform(x[0],x[1]),uniform(y[0],y[1]),uniform(z[0],z[1]),uniform(dx[0],dx[1]),uniform(dy[0],dy[1]),uniform(dz[0],dz[1]))
        bList.append(b)
    
    return bList

bList = [Body(1.1, -0.5, 0, 0, 0.05, 0.01, 0.1), Body(0.907, 0.5, 0, 0, -0.05, 0, -0.1), Body(1, 0, 1, 0, 0, -0.01, 0), Body(.9, 0.1, -1, 0.1, 0, 0.02, 0)]
#n = 3
#bList = getRandomBodies(n, m=[1,1], x=[-1,1], y=[-1,1], z=[-1,1])
space = Space(bodyList=bList, deltat=15, dt=0.05, epsilon=0.0)
space.act()  


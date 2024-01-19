'''
n-pendulum simulation using Lagrangian formulation
Assumes pendulum arms are rigid and m=0
'''
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.animation import FuncAnimation
import numpy as np
from scipy.integrate import odeint


class PendulumSystem:

    g = 9.81
    FIGSIZE = (6.4, 6.4)
    TRAIL_DENSITY = 20
    TRAIL_LENGTH = 2
    TRAIL_COLOR_SENSITIVITY = 2.33
    TRAIL_COLORS = [
                "firebrick",
                "red",
                "orangered",
                "orange",
                "gold",
                "yellow",
                "lightyellow",
                "white"
                ]
    
    class _Pendulum:

        def __init__(self, m, L, th0, thdot0=0, fric=0, experienceGravity=True, showTrail=True) -> None:
            self.m = m
            self.L = L
            self.th = th0
            self.thdot = thdot0
            self.fric = fric
            self.experienceGravity = experienceGravity
            
            self.showTrail = showTrail
            self.trail = None
            self.rod_sprite = None
            self.bob_sprite = None

            self.th_data = []
            self.thdot_data = []
            self.x_data = []
            self.y_data= []


    def __init__(self, t, dt) -> None:
        self.pl = []
        self.n = 0
        self.L_tot = 0
        self.tf = t
        self.dt = dt
        self.t_int = np.arange(0, t, dt)


    def addPendulum(self, m, L, th0, **kwargs) -> None:
        '''Add a Pendulum object to the system'''
        defaultKwargs = {
            "thdot0": 0, 
            "fric": 0,
            "experienceGravity": True,
            "showTrail": True
        }
        kwargs = {**defaultKwargs, **kwargs}
        self.pl.append(self._Pendulum(m=m, L=L, th0=th0, thdot0=kwargs["thdot0"], fric=kwargs["fric"], 
                                      experienceGravity=kwargs["experienceGravity"], showTrail=kwargs["showTrail"]))
        self.n += 1
        self.L_tot += L
    

    def _ode_system(self, q, t) -> np.ndarray:
        
        def A():
            A = []
            for i in range(self.n):
                row = []
                for k in range(self.n):
                    mqi = 0
                    for q in range(self.n):
                        if q>=k and i<=q:
                            mqi += self.pl[q].m
                    row.append(mqi*self.pl[i].L*self.pl[k].L*np.cos(self.pl[i].th - self.pl[k].th))
                A.append(row)
            return A
            
        def B():
            B = []
            for i in range(self.n):
                B_i = 0
                for k in range(self.n):
                    mqi = 0
                    B_i -= (
                        self.g*self.pl[i].L*np.sin(self.pl[i].th)*self.pl[k].m*
                        int(i<=k)*int(self.pl[k].experienceGravity)
                    ) + self.pl[i].fric*self.pl[i].thdot
                    for q in range(self.n):
                        if q>=k and i<=q:
                            mqi += self.pl[q].m
                    B_i -= (
                        mqi*self.pl[i].L*self.pl[k].L*np.sin(self.pl[i].th - self.pl[k].th)*
                        (self.pl[k].thdot**2)
                    )
                B.append(B_i)
            return B

        for i in range(self.n):
            self.pl[i].th = q[i]
            self.pl[i].thdot = q[i+self.n]

        thddot_data = np.linalg.solve(A(), B()).tolist()
        thdot_data = [p.thdot for p in self.pl]
        return thdot_data + thddot_data
    

    def _integrate_system(self) -> None:
        state0 = np.array([[p.th for p in self.pl], [p.thdot for p in self.pl]]).flatten()
        states = odeint(func=self._ode_system, y0=state0, t=self.t_int)

        x = lambda index: self.pl[index].L*np.sin(self.pl[index].th_data) + x(index-1) if index>=0 else 0
        y = lambda index: -self.pl[index].L*np.cos(self.pl[index].th_data) + y(index-1) if index>=0 else 0

        for i in range(self.n):
            self.pl[i].th_data = states.T[i]
            self.pl[i].thdot_data = states.T[i+self.n]
            self.pl[i].x_data = x(i)
            self.pl[i].y_data = y(i)


    def _init_anim(self) -> None:
        rcParams["toolbar"] = "None"
        self.fig = plt.figure(figsize=PendulumSystem.FIGSIZE, facecolor="black")
        ax = self.fig.add_axes((0, 0, 1, 1), facecolor="black")
        ax.set_xlim(-self.L_tot*1.2, self.L_tot*1.2)
        ax.set_ylim(-self.L_tot*1.2, self.L_tot*1.2)

        for p in self.pl:
            if p.showTrail:
                p.trail = [ax.plot([], [], lw=1, c='white', alpha=0, solid_capstyle='butt')[0]
                            for _ in range(PendulumSystem.TRAIL_DENSITY)]

        for p in self.pl:
            p.rod_sprite, = ax.plot([],[], linewidth=0.5, color="white")
            p.bob_sprite, = ax.plot([],[], "o", markersize=np.log(p.m+2)*(13.66/np.sqrt(self.L_tot)), color="white")
            

    def _init_plot(self) -> None:
        fig = plt.figure(figsize=(10, 7.5))
        ax = fig.add_axes((0.1, 0.1, 0.75, 0.8))
        for i in range(self.n):
            ax.plot(self.t_int, self.pl[i].th_data, label=f"P{i+1}")

        ax.set_title(f"n={self.n}")
        ax.legend(bbox_to_anchor=(1.135, 1), ncol=1)
        ax.set_xlabel("t")
        ax.set_ylabel(r"${\theta}$(t)")
    

    def _update(self, frame) -> None:

        obj_array = []
        for i in range(self.n):
            
            self.pl[i].bob_sprite.set_data(self.pl[i].x_data[frame:frame+1], self.pl[i].y_data[frame:frame+1])
            self.pl[i].rod_sprite.set_data([(self.pl[i-1].x_data[frame:frame+1]) if i-1>-1 else [0], self.pl[i].x_data[frame:frame+1]],
                                      [self.pl[i-1].y_data[frame:frame+1] if i-1>-1 else [0], self.pl[i].y_data[frame:frame+1]])

            if self.pl[i].showTrail:
                for segment in range(PendulumSystem.TRAIL_DENSITY):
                    obj_array.append(self.pl[i].trail[segment])
                    frame_min = max(frame - (PendulumSystem.TRAIL_DENSITY-segment)*PendulumSystem.TRAIL_LENGTH, 0)
                    frame_max = frame_min + PendulumSystem.TRAIL_LENGTH + 1
                    segment_alpha = (segment/PendulumSystem.TRAIL_DENSITY)**3

                    self.pl[i].trail[segment].set_data(self.pl[i].x_data[frame_min:frame_max], self.pl[i].y_data[frame_min:frame_max])
                    self.pl[i].trail[segment].set_alpha(segment_alpha)
                    self.pl[i].trail[segment].set_color(PendulumSystem.TRAIL_COLORS[int(min(abs(self.pl[i].thdot_data[frame_min])/PendulumSystem.TRAIL_COLOR_SENSITIVITY,
                                                                     len(PendulumSystem.TRAIL_COLORS)-1))])
            
            obj_array.append(self.pl[i].bob_sprite)
            obj_array.append(self.pl[i].rod_sprite)

        return obj_array


    def run(self, mode="animate") -> None:
        '''
        Run simulation based on mode selected:\n
        mode="animate": Animates the pendulums\n
        mode="plot": Plots each of the pendulum's angles over time
        '''
        self._integrate_system()

        if mode == "animate":
            self._init_anim()
            ANIMATOR = FuncAnimation(self.fig, self._update, frames=len(self.t_int), interval=1, blit=True)

        elif mode == "plot":
            self._init_plot()
        
        else:
           raise NameError(f"{mode} is not an option.")
            
        plt.show()

    
def main():
    ps = PendulumSystem(t=20, dt=0.025)
    ps.addPendulum(1, 1, np.radians(90), showTrail=False)
    ps.addPendulum(1, 0.75, np.radians(90))
    ps.addPendulum(1, 0.5, np.radians(90))

    ps.run(mode="animate")

if __name__ == "__main__":
    main()

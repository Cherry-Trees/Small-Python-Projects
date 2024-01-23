'''Quick proof of concept of dynamic response to input'''
import numpy as np

class DynamicResponse:

    def __init__(self, initPosition, f, zeta, rho, initVelocity=np.array([0, 0])) -> None:
        self.r = np.array(initPosition, float)
        self.r_d = np.array(initVelocity, float)
        self.vr = np.array([0, 0], float)
        self.input_prev = np.array(initPosition, float)

        self.u1 = zeta / (np.pi * f)
        self.u2 = 1 / (2 * np.pi * f)**2
        self.u3 = (rho * zeta) / (2 * np.pi * f)
    
    def update(self, input_pos, step_size, input_pos_d=None):
        input_pos = np.array(input_pos, float)

        if input_pos_d == None:
            input_pos_d = (input_pos - self.input_prev) / step_size
            self.input_prev = input_pos
        
        else:
            input_pos_d = np.array(input_pos_d, float)
        
        self.r_d += step_size * (input_pos + self.u3*input_pos_d - self.r - self.u1*self.r_d) / self.u2
        self.r += step_size * self.r_d
        return self.r


def main():
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    def x(t):
        return 4*np.cos(t) + 5
    
    def y(t):
        if t < 1:
            return 0
        if t >= 1 and t < 3:
            return 8
        if t >= 3 and t < 6:
            return t + 3
        if t >= 6 and t < 8:
            return -t + 9
        if t >= 8:
            return 5

    tf = 10
    dt = 0.01
    t = np.arange(0, tf, dt)

    init_pos = [x(0), y(0)]
    response_pos = init_pos

    input_data = []
    response_data = []

    DR = DynamicResponse(init_pos, 1.2, 0.35, 2)
    for step in t:
        response_pos = DR.update([x(step), y(step)], dt)
        response_data.append(response_pos.copy())
        input_data.append(np.array([x(step), y(step)]))
    
    response_data = np.array(response_data)
    input_data = np.array(input_data)

    fig, ax = plt.subplots()
    ax.set_xlim(0, 10)
    ax.set_ylim(-2, 12)
    input_line, = ax.plot([],[],"--", c="steelblue")
    input_marker, = ax.plot([],[],"o", c="steelblue")
    output_line, = ax.plot([],[], c="orangered")
    output_marker, = ax.plot([],[],"o", c="orangered")

    def animate(frame):
        input_line.set_data(input_data.T[0][:frame], input_data.T[1][:frame])
        input_marker.set_data(input_data.T[0][frame:frame+1], input_data.T[1][frame:frame+1])
        output_line.set_data(response_data.T[0][:frame], response_data.T[1][:frame])
        output_marker.set_data(response_data.T[0][frame:frame+1], response_data.T[1][frame:frame+1])
        return input_line,input_marker,output_line,output_marker,

    anim = FuncAnimation(fig, animate, len(t), interval=1, blit=True)
    plt.show()


if __name__ == "__main__":
    main()

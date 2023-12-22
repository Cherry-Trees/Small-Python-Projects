'''A program that animates a user drawing using epicycles'''
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
import numpy as np


class Fourier(object):

    @staticmethod
    def DFT(x_data, y_data):
        F, f, A, phi = [],[],[],[]
        N = len(y_data)

        for i in range(N):
            F_i = 0 + 0j
            for j in range(N):
                F_i += complex(x_data[j], y_data[j]) * np.exp(-1j*2*np.pi*i*j / N)
           
            F_i /= N
            F.append(F_i)
            f.append(i)
            A.append(abs(F_i))
            phi.append(np.arctan2(F_i.imag, F_i.real))

        return F, f, A, phi
   
    @staticmethod
    def calculate_circles(F, f, A, phi):
        circle_x_data = [[] for _ in range(len(F))]
        circle_y_data = [[] for _ in range(len(F))]
        connector_x_data = [[] for _ in range(len(F))]
        connector_y_data = [[] for _ in range(len(F))]
        drawing_path_x_data = []
        drawing_path_y_data = []

        for frame in range(len(F)):
            time_step = frame*(2*np.pi / len(F))
            x, y = 0, 0
            for i in range(len(F)):
                temp_x = x
                temp_y = y
                x += A[i] * np.cos(f[i]*time_step + phi[i])
                y += A[i] * np.sin(f[i]*time_step + phi[i])

                circle_x_data[i].append(temp_x + A[i]*np.cos(np.linspace(0, 2*np.pi, 100)))
                circle_y_data[i].append(temp_y + A[i]*np.sin(np.linspace(0, 2*np.pi, 100)))
                connector_x_data[i].append([temp_x, x])
                connector_y_data[i].append([temp_y, y])
                       
            drawing_path_x_data.append(x)
            drawing_path_y_data.append(y)

        return [
            circle_x_data,
            circle_y_data,
            connector_x_data,
            connector_y_data,
            drawing_path_x_data,
            drawing_path_y_data,
        ]
       

class FourierDrawingCanvas(object):    

    def __init__(self) -> None:
        self.mouse_x_data = []
        self.mouse_y_data = []
        self.num_drawing_paths = 0  
        self.drawn_pixel_memory = 0
        self.drawn_pixel_memory_list = []
        self.user_drawing_object_list = []

    def create_drawing_canvas(self):
        root = tk.Tk()
        root.wm_title("The World is Your Canvas!")
        self.fig = Figure(figsize=(8,8))
        self.ax = self.fig.add_axes((0,0,1,1),xlim=[-1,1],ylim=[-1,1],fc="black")

        canvas = FigureCanvasTkAgg(self.fig, master=root)
        canvas.get_tk_widget().pack(side=tk.BOTTOM, expand=0)
        self.button = tk.Button(master=root, text="Finished!", command=self._on_button_press)
        self.button.pack(side=tk.BOTTOM)
        canvas.mpl_connect("motion_notify_event", self._on_mouse_hold)
        canvas.mpl_connect("button_press_event", self._on_mouse_press)
        tk.mainloop()

    def _on_mouse_hold(self, event):
        if event.inaxes and event.button and self.button.cget("text") == "Finished!":
            self.mouse_x_data.append(event.xdata)
            self.mouse_y_data.append(event.ydata)
            self.user_drawing_object_list[self.num_drawing_paths-1] = self.ax.plot(self.mouse_x_data[self.drawn_pixel_memory:],
                                                                                   self.mouse_y_data[self.drawn_pixel_memory:],
                                                                                   color="purple")
            self.ax.figure.canvas.draw()
   
    def _on_mouse_press(self, event):
        if self.button.cget("text") == "Finished!":
            self.num_drawing_paths += 1
            self.user_drawing_object_list.append(None)
            self.drawn_pixel_memory = len(self.mouse_x_data)
            self.drawn_pixel_memory_list.append(len(self.mouse_x_data))

    def _on_button_press(self):
        self.ax.clear()
        self.ax.set_xlim(-1,1)
        self.ax.set_ylim(-1,1)
        self.ax.figure.canvas.draw()
        self._animate_user_drawing()

        if self.button.cget("text") == "Finished!":
            self.button.config(text="Reset")
       
        else:
            self.button.config(text="Finished!")
            self.mouse_x_data.clear()
            self.mouse_y_data.clear()
            self.num_drawing_paths = 0
            self.user_drawing_object_list.clear()
            self.drawn_pixel_memory = 0
            self.drawn_pixel_memory_list.clear()

    def _animate_user_drawing(self):
        F, f, A, phi = Fourier.DFT(self.mouse_x_data, self.mouse_y_data)
        A, F, f, phi = (list(i) for i in zip(*sorted(zip(A, F, f, phi), reverse=True)))
        circle_x_data, circle_y_data, connector_x_data, connector_y_data, drawing_path_x_data, drawing_path_y_data = Fourier.calculate_circles(F, f, A, phi)

        circle_object_list = [self.ax.plot([],[], color="darkgrey", linewidth=0.1)[0] for _ in range(len(F))]
        connector_object_list = [self.ax.plot([],[], color="white", linewidth=0.75)[0] for _ in range(len(F))]
        drawing_path_object_list = [self.ax.plot([],[], color="purple")[0] for _ in range(self.num_drawing_paths)]
        self.drawing_path_object_index = 0

        def _animation_func(frame):
           
            if frame in self.drawn_pixel_memory_list and frame != 0:
                self.drawing_path_object_index += 1
           
            if frame == 0:
                self.drawing_path_object_index = 0
                for drawing_path_object in drawing_path_object_list:
                    drawing_path_object.set_data([],[])
           
            drawing_path_object_list[self.drawing_path_object_index].set_data(drawing_path_x_data[self.drawn_pixel_memory_list[self.drawing_path_object_index]:frame],
                                                                        drawing_path_y_data[self.drawn_pixel_memory_list[self.drawing_path_object_index]:frame])
            for i in range(len(F)):
                circle_object_list[i].set_data(circle_x_data[i][frame], circle_y_data[i][frame])
                connector_object_list[i].set_data(connector_x_data[i][frame], connector_y_data[i][frame])
           
            self.ax.figure.canvas.draw()
            return circle_object_list + connector_object_list + drawing_path_object_list
       
        ANIMATION = FuncAnimation(self.fig, _animation_func, len(F), interval=1, blit=True)


fdc = FourierDrawingCanvas()
fdc.create_drawing_canvas()

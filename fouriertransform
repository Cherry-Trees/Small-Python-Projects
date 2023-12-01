'''Fourier Transform visualized'''

from numpy import *
from matplotlib import pyplot as plt
import cmath
import math
from matplotlib.animation import FuncAnimation
from matplotlib.patches import ConnectionPatch

# Line density for Fourier Transform
DENSITY = 6


# Function
def f(t):
    return cos(2*pi*t) + cos(4*pi*t) + cos(8*pi*t)


# Fourier Transform
def g(t,omega):
    return f(t)*exp(-2*pi*omega*1j*t)


##############################
##############################


fig,(ax1,ax2,ax3) = plt.subplots(
    ncols=3,
    sharey=True,
    figsize=(9, 3),
    gridspec_kw=dict(width_ratios=[2,2,2], wspace=0),
)
ax1.grid()
ax2.grid()
ax3.grid()

ax1.set_xlim(0,5)
ax1.set_ylim(-3,3)
ax2.set_xlim(-3,3)
ax3.set_xlim(0,5)

ax1.axhline(y=0, color="black", linestyle = ':')
ax1.axvline(x=0, color="black", linestyle = ':')
ax2.axhline(y=0, color="black", linestyle = ':')
ax2.axvline(x=0, color="black", linestyle = ':')
ax3.axhline(y=0, color="black", linestyle = ':')
ax3.axvline(x=0, color="black", linestyle = ':')

ax1.set_title("Signal f(t)")
ax2.set_title("f(t) Unwinding")
ax3.set_title("Fourier Transform f(v)")

line1, = ax1.plot([],[])
line2, = ax1.plot([],[],color="orange",alpha=0.0)
wrapline, = ax2.plot([],[],color="orange",alpha=1)
point, = ax2.plot([],[],"o")
pointline, = ax3.plot([],[])

xdata, ydata = [[],[],[]],[[],[],[]]

point_x = 0
point_y = 0

point_xdata = []
point_ydata = []

# Connection
con = ConnectionPatch(
    (1, 0),
    (0, 0),
    "data",
    "data",
    axesA=ax2,
    axesB=ax3,
    color="C0",
    ls="dotted",
)
fig.add_artist(con)



def init():
    line1.set_data([],[])
    line2.set_data([],[])
    wrapline.set_data([],[])
    point.set_data([],[])
    pointline.set_data([],[])
    return line1,line2,wrapline,point,pointline,




def anim(frame):
   
    t = 0.01*frame
    freq = t

    delta_t = linspace(0.0001,DENSITY,1000)
    x = g(delta_t,freq).real
    y = g(delta_t,freq).imag
    wrapline.set_data(y,x)

    # Graph 1
    xdata[0].append(t)
    xdata[1].append(t)
    ydata[0].append(f(t))
    ydata[1].append(g(t,freq))


    # Graph 2
    xdata[2].append(g(t,freq).real)
    ydata[2].append(g(t,freq).imag)

    point_x = average(x)
    point_y = average(y)


    # Graph 3
    point_xdata.append(t)
    point_ydata.append(point_x)


    line1.set_data(xdata[0], ydata[0])
    line2.set_data(xdata[1], ydata[1])
    point.set_data(point_y, point_x)
    pointline.set_data(point_xdata, point_ydata)
    
    con.xy1 = point_y, point_x
    con.xy2 = t, point_x

    return line1,line2,wrapline,point,pointline,


an = FuncAnimation(fig, anim, init_func = init, frames = 510, interval = 1, blit = True, repeat = False)
plt.show()

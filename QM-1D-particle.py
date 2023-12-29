'''Simulation of a particle in 1D'''
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


class WaveFunction:

    def __init__(self, psi, m, hbar, V=None, x0=-10, xf=10, n_points=2000):
        self.x0 = x0
        self.xf = xf
        self.range = xf - x0
        self.n_points = n_points

        self.m = m
        self.hbar = hbar
        self.V = lambda x: V(x) if V != None else 0

        self.domain = np.linspace(x0, xf, n_points)
        self.dx = self.domain[1] - self.domain[0]
        self.funcImage = psi(self.domain)

    def __call__(self):
        return self.funcImage.copy()
        
    def discreteNormalize(self):
        self.funcImage /= np.sqrt(sum(abs(self.funcImage)**2) * self.dx)
    
    def discreteLaplacian(self, funcImage):
        diff = np.zeros_like(funcImage)
        diff[1:-1] = (funcImage[2:] - 2*funcImage[1:-1] + funcImage[:-2])
        return diff
    
    def schrodinger(self, funcImage):
        return 1j*self.hbar/2*self.m * self.discreteLaplacian(funcImage) - 1j*self.V(self.domain)*funcImage
    

class WaveFunctionIntegrator:

    def __init__(self, initWaveFunc):
        self.waveFunc = initWaveFunc
        self.waveFuncStates = [initWaveFunc()]

    def euler_step(self, dt):
        self.waveFunc.funcImage += self.waveFunc.schrodinger(self.waveFunc()) * dt
    
    def RK4_step(self, dt):
        k1 = dt * self.waveFunc.schrodinger(self.waveFunc())
        k2 = dt * self.waveFunc.schrodinger(self.waveFunc() + k1/2)
        k3 = dt * self.waveFunc.schrodinger(self.waveFunc() + k2/2)
        k4 = dt * self.waveFunc.schrodinger(self.waveFunc() + k3)
        self.waveFunc.funcImage += 1/6 * (k1 + 2*k2 + 2*k3 + k4)
    
    def integrate(self, steps, dt, append_every=10, method="RK4"):
        if method == "RK4":
            for t in range(steps):
                self.RK4_step(dt)
                self.waveFunc.discreteNormalize()

                if t%append_every == 0:
                    self.waveFuncStates.append(self.waveFunc())
        
        if method == "euler":
            for t in range(steps):
                self.euler_step(dt)
                self.waveFunc.discreteNormalize()

                if t%append_every == 0:
                    self.waveFuncStates.append(self.waveFunc())
        
        return self.waveFuncStates
    

class WaveFunctionAnimator:

    def animate(waveFuncStates, interval, **kwargs):
        fig, ax = plt.subplots()
        ax.set_xlim(kwargs["xlim"])
        ax.set_ylim(kwargs["ylim"])

        psi_abs, = ax.plot([],[],label="|Ψ|")
        real, = ax.plot([],[],label="Ψ Re")
        imag, = ax.plot([],[],label="Ψ Im")
        ax.legend()

        def _animation_func(frame):
            psi_abs.set_data(interval, abs(waveFuncStates[frame]))
            real.set_data(interval, waveFuncStates[frame].real)
            imag.set_data(interval, waveFuncStates[frame].imag)
            return psi_abs,real,imag,

        anim = FuncAnimation(fig, _animation_func, len(waveFuncStates), interval=1, blit=True)
        plt.show()
    

m = 10
p = 25
hbar = 1
mu = 0
sigma = 0.5

psi = WaveFunction(lambda x: np.exp(-(x-mu)**2 / (2*sigma**2), dtype=complex) * np.exp(1j*p*x),
                   m, hbar, lambda x: x**2)

solver = WaveFunctionIntegrator(psi)
states = solver.integrate(15000, 0.01, method="RK4")
WaveFunctionAnimator.animate(states, psi.domain, xlim=(-2,2), ylim=(-2,2))

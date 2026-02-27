import librosa
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np
import pyaudio
import time

class Visualiser():

    def __init__(self):
        #Config
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.chunk = int(self.rate/20)
        self.n_fft = 2048
        self.x = np.arange(0, 100, self.chunk)
        self.y = 0

        #initialise pyaudio
        p = pyaudio.PyAudio()
        self.stream = p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )

        #plot data
        self.fig, ax = plt.subplots()
        self.line, = ax.plot(self.x[0], self.y)

    def update(self, frame):
        self.data = np.frombuffer(self.stream.read(self.chunk), dtype=np.int16)
        self.line.set_ydata(self.data)
        self.line.set_xdata(self.x[:frame])
        return self.line
         
    
    def animate(self):
        ani = anim.FuncAnimation(fig=self.fig, func=self.update, frames=50, interval=10)
        plt.show()


if __name__ == "__main__":
        v = Visualiser()
        v.animate()
        

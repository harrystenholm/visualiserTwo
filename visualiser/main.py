import librosa
import matplotlib.pyplot as plt
import numpy as np
import pyaudio
from pyparsing import line

class Visualiser(object):
    def __init__(self):
        #Config
        self.chunk = 1024
        self.format = pyaudio.paFloat32
        self.channels = 1
        self.rate = 44100
        self.n_fft = 2048

        #initialise pyaudio
        p = pyaudio.PyAudio()
        self.stream = p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )

        #Setup plot
        fig, ax = plt.subplots(figsize = (12, 6))
        x = np.linspace(0, self.rate/2, self.n_fft // 2 + 1)
        line, = ax.plot(x, np.random.rand(self.n_fft // 2 + 1))
        ax.set_xlim(20, 20000)
        ax.set_xlim(0, 1)
        ax.set_xscale('log')

    def update(self):
        for i in range(10):
            data = self.stream.read(self.chunk)
            print(data)

if __name__ == "__main__":
        v = Visualiser()
        v.update()

import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np
import time
import sounddevice as sd

#Config
format = np.int16
channels = 2
samplerate = 48000
chunk = 1024 * channels
inputIndex = 6
audioData = np.zeros((chunk, channels))

#Plot config
fig, ax = plt.subplots()
ax.set(xlim=[0, chunk], ylim=[-38000, 38000])
x = np.arange(0, chunk * channels, 1)
y = np.zeros_like(x)
line, = ax.plot(x, y, '-', lw=1)
plt.show(block=False)

def callback(indata, frames, time, status):
    global audioData
    audioData = indata.copy()

with sd.InputStream(dtype='int16', callback=callback, 
                    blocksize=chunk, device=inputIndex, 
                    samplerate=samplerate, channels=channels):
    while plt.fignum_exists(fig.number):
        print(audioData[:, 0])
        line.set_ydata(audioData),
        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.pause(0.01)
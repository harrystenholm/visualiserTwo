import librosa
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np
import sounddevice as sd

#Config
format = np.float32
channels = 2
samplerate = 48000
chunk = 1024 * channels
inputIndex = 6
audioData = np.zeros((chunk, channels))

#Plot config
fig, (ax1, ax2) = plt.subplots(2)
ax1.set(xlim=[0, chunk], ylim=[-1, 1])
ax2.set(xlim=[0, chunk], ylim=[-1, 1])
x = np.arange(0, chunk, 1)
y = np.zeros_like(x)
channelOne, = ax1.plot(x, y, '-', lw=1)
channelTwo, = ax2.plot(x, y, '-', lw=1)
plt.show(block=False)

def callback(indata, frames, time, status):
    global audioData
    audioData = indata.copy()

with sd.InputStream(dtype='float32', callback=callback, 
                    blocksize=chunk, device=inputIndex, 
                    samplerate=samplerate, channels=channels):
    while plt.fignum_exists(fig.number):
        print(audioData[:, 0])
        channelOne.set_ydata(audioData[:, 0])
        channelTwo.set_ydata(audioData[:, 1])
        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.pause(0.01)

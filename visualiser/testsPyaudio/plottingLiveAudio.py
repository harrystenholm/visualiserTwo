import librosa
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np
import pyaudio
import time

#Config
format = pyaudio.paInt16
channels = 1
rate = 44100
chunk = 2048
inputIndex = 8

#define plot
fig, ax = plt.subplots()
x = np.arange(0, chunk * channels, 1)
y = np.zeros_like(x)
line, = ax.plot(x, y, '-', lw=1)

ax.set_ylim(-32768, 32768)
ax.set_xlim(0, chunk * channels)
plt.setp(ax, xticks=[0, chunk], yticks=[-32768, 0, 32768])
plt.show(block=False)

if __name__ == "__main__":
    p = pyaudio.PyAudio()
    stream = p.open(
        format = format,
        channels = channels,
        rate = rate,
        input = True,
        input_device_index=inputIndex,
        frames_per_buffer = chunk
    )

    while plt.fignum_exists(fig.number):
        data = np.frombuffer(stream.read(chunk), dtype = np.int16)
        line.set_ydata(data)
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.01)

stream.stop_stream()
stream.close()
p.terminate()
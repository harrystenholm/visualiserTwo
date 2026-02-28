import librosa
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np
import time
import pyaudio

data = {
    'x': np.arange(0, 100, 1),
    'y': np.arange(0, 100, 1)
}

cmap = plt.cm.viridis

fig, ax = plt.subplots()

line = ax.plot(0, 0)[0]
ax.set(xlim=[0,100], ylim=[0,100])

def update(frame):
    a = data['x'][:frame]
    b = data['y'][:frame]
    color = (np.random.randint(0, 1),np.random.randint(0, 1),np.random.randint(0, 1))
    line.set_xdata(a)
    line.set_ydata(b)
    line.set_color(color)
    return line

ani = anim.FuncAnimation(fig=fig, func=update, frames = max(data['x']), interval = 10 )
plt.show()



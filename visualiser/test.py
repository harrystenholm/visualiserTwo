import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import matplotlib.colors as col

fig,ax = plt.subplots()

np.random.seed(19680801)
x = np.random.rand(50)*5
y = np.random.rand(50)*5
c = np.random.rand(50,4)

cmap = plt.cm.viridis
norm = col.Normalize(vmin=0, vmax=5)

line = ax.plot(x[0], y[0], c=c[0])[0]
ax.set(xlim=[0, 5], ylim=[0, 5])

def update(frame):
    a = x[:frame]
    b = y[:frame]
    color = cmap(norm(x[frame]))
    line.set_xdata(a)
    line.set_ydata(b)
    line.set_color(color)
    return line

ani = anim.FuncAnimation(fig=fig, func=update,frames=50,interval=10)
plt.show()
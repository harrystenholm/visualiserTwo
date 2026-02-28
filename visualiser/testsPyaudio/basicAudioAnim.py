import librosa
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np
import time
import pyaudio

#Config
format = pyaudio.paInt16
channels = 1
rate = 44100
chunk = 512 * channels
inputIndex = 9
audioData = np.zeros(chunk * channels)

#Plot config
fig, ax = plt.subplots()
ax.set(xlim=[0, chunk], ylim=[-20, 20])
x = np.arange(0, chunk * channels, 1)
y = np.zeros_like(x)
line, = ax.plot(x, y, '-', lw=1)

plt.show(block=False)

#initilaiase pyaudio
p = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    global audioData
    audioData = np.frombuffer(in_data, dtype=np.int16)
    return (in_data, pyaudio.paContinue)

stream = p.open(
    format = format,
    channels = channels,
    rate = rate,
    input = True,
    input_device_index=inputIndex,
    frames_per_buffer = chunk,
    stream_callback = callback
)

stream.start_stream()

while plt.fignum_exists(fig.number):
    print(audioData)
    line.set_ydata(audioData)
    fig.canvas.draw()
    fig.canvas.flush_events()
    time.sleep(0.1)
 
stream.stop_stream()
stream.close()
p.terminate()
import librosa
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np
import pyaudio
import time

#Config
format = pyaudio.paInt16
channels = 2
rate = 44100
chunk = int(rate/20)
n_fft = 2048
index = 9

#initialise pyaudio
p = pyaudio.PyAudio()
stream = p.open(
    format = format,
    channels = channels,
    rate = rate,
    input = True,
    input_device_index=index,
    frames_per_buffer = chunk
)

for i in range(100):
    data = np.frombuffer(stream.read(chunk), dtype = np.int16)
    print(data)



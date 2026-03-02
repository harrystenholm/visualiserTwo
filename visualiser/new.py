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
audioData = np.zeros(chunk)


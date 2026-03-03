import sounddevice as sd
import numpy as np
import librosa

class InputStream():

    def __init__(self, line):
    
        #Config
        format = np.float32
        channels = 2
        samplerate = 48000
        chunk = 1024 * channels
        audioData = np.zeros(chunk)
        inputIndex = 6
        audioData = np.zeros((chunk, channels))

        #callback from input stream
        def callback(indata, frames, time, status):
            global audioData
            audioData = indata.copy()
            line.setData(audioData[:, 0])

        #start stream
        stream = sd.InputStream(dtype='float32', callback = callback, 
                    blocksize=chunk, device=inputIndex, 
                    samplerate=samplerate, channels=channels)
        stream.start()
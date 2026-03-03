from PyQt5.QtCore import QObject, pyqtSignal
import sounddevice as sd
import numpy as np
import librosa

class InputStream(QObject):
    volumeChanged = pyqtSignal(int)

    def __init__(self, parent = None):
        super().__init__(parent)

        #Config
        format = np.float32
        channels = 2
        samplerate = 48000
        chunk = 1024 * channels
        inputIndex = 6

        #callback from input stream
        def callback(indata, frames, time, status):
            global audioData
            audioData = indata.copy()
            rms = np.sqrt(np.mean(audioData**2))
            volume = int(rms * 100)
            self.volumeChanged.emit(volume)

        #start stream
        stream = sd.InputStream(dtype='float32', callback = callback, 
                    blocksize=chunk, device=inputIndex, 
                    samplerate=samplerate, channels=channels)
        stream.start()
from PyQt5.QtCore import QObject, pyqtSignal
import sounddevice as sd
import numpy as np
import librosa

class InputStream(QObject):
    waveForm = pyqtSignal(np.ndarray)
    dB = pyqtSignal(int)

    def __init__(self, mode, parent = None):
        super().__init__(parent)
        self.plotType = mode
        
        #Config
        format = np.float32
        self.channels = 2
        self.samplerate = 48000
        self.chunk = 1024 * self.channels
        self.inputIndex = 6

        #start stream
        self.stream = sd.InputStream(dtype='float32', callback = self.callback, 
                    blocksize=self.chunk, device=self.inputIndex, 
                    samplerate=self.samplerate, channels=self.channels)
        self.stream.start()
        
    def set_mode(self, mode):
        self.plotType = mode

        #callback from input stream
    def callback(self, indata, frames, time, status):
        audioData = indata.copy()
        if self.plotType == "waveform":
            self.waveForm.emit(audioData[:,0])
        elif self.plotType == "dB":
            rms = np.sqrt(np.mean(audioData**2))
            volume = int(rms * 100)
            self.dB.emit(volume)
        elif self.plotType == "graphics":
            rms = np.sqrt(np.mean(audioData**2))
            volume = int(rms * 100)
            self.dB.emit(volume)
            self.waveForm.emit(audioData[:,0])


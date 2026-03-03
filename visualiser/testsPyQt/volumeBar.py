import librosa
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np
import pyqtgraph as pg
import inputStream 
from PyQt5 import QtWidgets

#initiliase pyQt window
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visualiser")

        #initialise dB plot
        volumeBar = pg.QtWidgets.QProgressBar()
        volumeBar.setRange(0, 100)
        volumeBar.setTextVisible(False)
        self.setCentralWidget(volumeBar)

        #call input stream to update waveform plot
        stream = inputStream.InputStream(self)
        stream.volumeChanged.connect(volumeBar.setValue)

    
app = QtWidgets.QApplication([])
main = MainWindow()
main.show()
app.exec()

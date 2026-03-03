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

        #initialise toolbar
        toolbar = QtWidgets.QToolBar("Main")
        self.addToolBar(toolbar)

        self.waveform = QtWidgets.QAction("Waveform", self)
        self.waveform.triggered.connect(self.waveFormActive)
        self.waveform.setCheckable(True)
        self.waveform.setChecked(True)
        
        self.dB = QtWidgets.QAction("dB", self)
        self.dB.triggered.connect(self.dBActive)
        self.dB.setCheckable(True)

        toolbar.addAction(self.waveform)
        toolbar.addSeparator()
        toolbar.addAction(self.dB)

        #initialise waveform plot
        self.plot = pg.PlotWidget()
        self.setCentralWidget(self.plot)
        self.line = self.plot.plot(pen = 'y')

        x = np.arange(0, 1024, 1)
        self.plot.setXRange(0, max(x))
        self.plot.setYRange(-1, 1)
        line = self.plot.plot(
            x = np.arange(0, 1024, 1),
            y = np.zeros_like(x)
        )

        #call input stream to update waveform plot
        inputStream.InputStream(line)

    def waveFormActive(self, s):
        self.dB.setChecked(False)
        print("waveform active", s)

    def dBActive(self, s):
        self.waveform.setChecked(False)
        print("dB active", s)

    
app = QtWidgets.QApplication([])
main = MainWindow()
main.show()
app.exec()

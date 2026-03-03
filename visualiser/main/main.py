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

        #Set up stacked container
        self.container = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.container)

        #initiliase widgets
        self.init_plots()
        self.init_toolbar()

        self.stream = inputStream.InputStream("waveform", self)
        self.stream.waveForm.connect(self.line.setData)
        self.stream.dB.connect(self.volumeBar.setValue)

    def init_plots(self):
        #initialise waveform plot
        self.plot = pg.PlotWidget()

        x = np.arange(0, 1024, 1)
        self.plot.setXRange(0, max(x))
        self.plot.setYRange(-1, 1)
        self.line = self.plot.plot(
            x = np.arange(0, 1024, 1),
            y = np.zeros_like(x),
            pen = 'y'
        )

        #initialise dB plot
        self.volumeBar = pg.QtWidgets.QProgressBar()
        self.volumeBar.setRange(0, 100)
        self.volumeBar.setTextVisible(False)

        #Add to stacked widget
        self.container.addWidget(self.plot)
        self.container.addWidget(self.volumeBar)

    def init_toolbar(self):  
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

    def waveFormActive(self, s):
        self.dB.setChecked(False)
        self.stream.set_mode("waveform")
        self.container.setCurrentIndex(0)
        print("waveform active", s)

    def dBActive(self, s):
        self.waveform.setChecked(False)
        self.stream.set_mode("dB")
        self.container.setCurrentIndex(1)
        print("dB active", s)

    
app = QtWidgets.QApplication([])
main = MainWindow()
main.show()
app.exec()

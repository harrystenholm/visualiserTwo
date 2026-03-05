import librosa
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np
import pyqtgraph as pg
import inputStream
from PyQt5.QtCore import Qt, QPointF
from PyQt5 import QtWidgets, QtOpenGL
from PyQt5.QtGui import QBrush, QPainter, QPen, QColor, QPainterPath, QPolygonF

#initiliase pyQt window
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visualiser")

        #initiliase variables
        self.currentSize = 100
        self.frameCounter = 0
        self.updateLock = False
        self.numSpikes = 60
        self.smoothed_amplitudes = np.zeros(self.numSpikes)
        self.spike_height = np.zeros(self.numSpikes)

        self.angles = np.linspace(0, 2 * np.pi, self.numSpikes)
        self.cos_angles = np.cos(self.angles)
        self.sin_angles = np.sin(self.angles)

        #Set up stacked container
        self.container = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.container)

        #initiliase widgets
        self.init_plots()
        self.init_toolbar()
        self.init_graphics()

        self.stream = inputStream.InputStream("waveform", self)
        self.stream.waveForm.connect(self.line.setData, Qt.QueuedConnection)
        self.stream.waveForm.connect(self.updateOutline, Qt.QueuedConnection)
        self.stream.dB.connect(self.volumeBar.setValue, Qt.QueuedConnection)
        self.stream.dB.connect(self.ellipseAnim, Qt.QueuedConnection)

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

        self.graphics = QtWidgets.QAction("graphics", self)
        self.graphics.triggered.connect(self.graphicsACtive)
        self.graphics.setCheckable(True)

        toolbar.addAction(self.waveform)
        toolbar.addSeparator()
        toolbar.addAction(self.dB)
        toolbar.addSeparator()
        toolbar.addAction(self.graphics)

    def init_graphics(self):
        self.scene = QtWidgets.QGraphicsScene(-200, -200, 400, 400)
        self.scene.setBackgroundBrush(QBrush(Qt.black))
        self.scene.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)
        # Define a large coordinate system (e.g., -5000 to 5000)
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.setViewport(QtOpenGL.QGLWidget())
        self.view.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setAlignment(Qt.AlignCenter)

        #initialise ellipse shape
        self.ellipse = QtWidgets.QGraphicsEllipseItem(-50, -50, 100, 100)
        self.ellipse.setPos(0, 0)
        self.ellipse.setOpacity(0.67)
        brush = QBrush(Qt.blue)
        self.ellipse.setBrush(brush)
        pen = QPen(Qt.transparent)
        self.ellipse.setPen(pen)

        #initiliase main outline
        self.outline = QtWidgets.QGraphicsPathItem(parent=self.ellipse)
        self.outline.setPen(QPen(Qt.green, 4))
        self.outline.setPos(0, 0)

        #initialise outline trails
        self.trailCount = 3
        self.trailItems = []
        for i in range(self.trailCount):
            item = QtWidgets.QGraphicsPathItem(parent=self.ellipse)
            item.setPos(0, 0)
            opacity = 1 - ((i + 1) / (self.trailCount + 1))
            item.setOpacity(opacity)
            item.setPen(QPen(Qt.green, 2))
            self.trailItems.append(item)

        self.scene.addItem(self.ellipse)
        self.container.addWidget(self.view)

    def resizeEvent(self, event):
        #ensures the window handles resize event first
        super().resizeEvent(event)

        # calculate center and update item pos
        if hasattr(self, 'view') and self.scene:
            viewSize = self.view.viewport().rect()
            self.scene.setSceneRect(-150, -150, 300, 300)

            self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
            
            # Moving the parent moves all children automatically
            self.ellipse.setPos(0, 0)

    def ellipseAnim(self, value):
        #target diameter of ellipse
        targetSize = (value * 2.5)
        #add linear interpolation to input
        lerp = 0.35
        self.currentSize += (targetSize - self.currentSize) * lerp
        # set to half to keep in center
        radius = self.currentSize / 2

        #calculate hue for gradient
        hue = 0.6 - ((value / 80) * 0.6)
        color = QColor.fromHsvF(hue, 0.8, 1)

        self.outline.setPen(QPen(color))
        self.ellipse.setBrush(QBrush(color))
        self.ellipse.setPen(QPen(color))
        self.ellipse.setRect(-radius, -radius, self.currentSize, self.currentSize)

    def updateOutline(self, value):
        
        self.frameCounter += 1
        if self.frameCounter % 2 != 0 or self.updateLock:
            return
        
        try:
            self.updateLock = True
            #shift the trails
            for i in range(len(self.trailItems) -1, 0, -1):
                self.trailItems[i].setPath(self.trailItems[i-1].path())
                self.trailItems[i].setPen(self.trailItems[i-1].pen())

            #make first trail take shapoe of main outline
            if len(self.trailItems) > 0:
                self.trailItems[0].setPath(self.outline.path())
                self.trailItems[0].setPen(QPen(self.ellipse.brush().color(), 2))

            step = len(value) // self.numSpikes
            path = QPainterPath()
            radius = self.ellipse.rect().width() / 2
            amplitudes = np.abs(value[::step][:self.numSpikes]) * 80

            lerp = 0.35
            self.smoothed_amplitudes = (self.smoothed_amplitudes * (1 - lerp)) + (amplitudes * lerp)

            gravity = 2.5
            fallSpeed = 0.85

            for i in range(self.numSpikes):
                height = self.smoothed_amplitudes[i]

                if height > self.spike_height[i]:
                    self.spike_height[i] = height
                else:
                    self.spike_height[i] -= gravity
                    if self.spike_height[i] < 0:
                        self.spike_height[i] = 0

            r = radius + self.spike_height

            path.moveTo(r[0] * self.cos_angles[0], r[0] * self.sin_angles[0])
            for i in range(1, self.numSpikes):
                path.lineTo(r[i] * self.cos_angles[i], r[i] * self.sin_angles[i])

            path.closeSubpath()
            self.outline.setPath(path)

        finally:
            self.updateLock = False

    def waveFormActive(self, s):
        self.dB.setChecked(False)
        self.graphics.setChecked(False)
        self.stream.set_mode("waveform")
        self.container.setCurrentIndex(0)
        print("waveform active", s)

    def dBActive(self, s):
        self.waveform.setChecked(False)
        self.graphics.setChecked(False)
        self.stream.set_mode("dB")
        self.container.setCurrentIndex(1)
        print("dB active", s)

    def graphicsACtive(self, s):
        self.dB.setChecked(False)
        self.waveform.setChecked(False)
        self.stream.set_mode("graphics")
        self.container.setCurrentIndex(2)
        print("graphics active", s)

    
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main = MainWindow()
    main.show()
    app.exec()

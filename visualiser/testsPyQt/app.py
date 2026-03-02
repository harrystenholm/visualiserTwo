from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

class main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.buttonToggled = False

        self.setWindowTitle("App")

        self.button = QPushButton("Button")
        self.button.setCheckable(True)
        self.button.clicked.connect(self.buttonClick)
        self.button.clicked.connect(self.buttonToggle)

        self.setCentralWidget(self.button)

    def buttonClick(self):
        self.button.setText("I've been clicked!")
        self.button.setEnabled(False)

        self.setWindowTitle("The button has been clicked!")

        print("Clicked!")
        
    def buttonToggle(self, toggled):
        self.buttonToggled = toggled

        print("Toggled?", self.buttonToggled)

app = QApplication([])

window = main()
window.show() 

# Start the event loop.
app.exec()
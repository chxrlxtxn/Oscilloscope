# importing libraries needed
import sys
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt
import subprocess

range = 5
# Graphical User Interface Setup
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Oscilloscope Rolling Settings')
        self.resize(400,50)
        layout = QVBoxLayout()

        # mode label
        self.modeLabel = QLabel()
        self.modeLabel.setText('Set Y Range (0 - 25)')
        self.modeLabel.setFont(QFont('Aptos', 10))
        self.modeLabel.setAlignment(Qt.Alignment())
        layout.addWidget(self.modeLabel)

        # range spin box
        self.spinBox = QDoubleSpinBox()
        self.spinBox.setMaximum(25)
        self.spinBox.setMinimum(0)
        self.spinBox.setValue(range)
        self.spinBox.setFont(QFont('Aptos', 10))
        layout.addWidget(self.spinBox)

        # mode button
        self.modeButton = QPushButton()
        self.modeButton.setText('Start Oscilloscope')
        self.modeButton.setFont(QFont('Aptos', 10))
        layout.addWidget(self.modeButton)
        self.modeButton.clicked.connect(self.button_clicked)

        # setting widget
        self.widget = QWidget()
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)

    # interrupt for when button is clicked
    def button_clicked(self):
        global range
        range = self.spinBox.value()
        self.hide()
        subprocess.run(['python', 'public/rolling/rolling.py', str(range)])
        exit()
        
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

# Author: Sri Tirumalaraju
# importing libraries needed
import sys
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt
import subprocess

rangeX = 5
rangeY = 25
# Graphical User Interface Setup
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Oscilloscope XY-Mode Settings')
        self.resize(400,50)
        layout = QVBoxLayout()

        # mode label
        self.modeLabelX = QLabel()
        self.modeLabelX.setText('Set Channel 1 Range (0 - 25)')
        self.modeLabelX.setFont(QFont('Aptos', 10))
        self.modeLabelX.setAlignment(Qt.Alignment())
        layout.addWidget(self.modeLabelX)

        # x spin box
        self.spinBoxX = QDoubleSpinBox()
        self.spinBoxX.setMaximum(25)
        self.spinBoxX.setMinimum(0)
        self.spinBoxX.setValue(rangeX)
        self.spinBoxX.setFont(QFont('Aptos', 10))
        layout.addWidget(self.spinBoxX)

        # mode label
        self.modeLabelY = QLabel()
        self.modeLabelY.setText('Set Channel 2 Range (0 - 25)')
        self.modeLabelY.setFont(QFont('Aptos', 10))
        self.modeLabelY.setAlignment(Qt.Alignment())
        layout.addWidget(self.modeLabelY)

        # y spin box
        self.spinBoxY = QDoubleSpinBox()
        self.spinBoxY.setMaximum(25)
        self.spinBoxY.setMinimum(0)
        self.spinBoxY.setValue(rangeY)
        self.spinBoxY.setFont(QFont('Aptos', 10))
        layout.addWidget(self.spinBoxY)

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
        global rangeX, rangeY
        rangeX = self.spinBoxX.value()
        rangeY = self.spinBoxY.value()
        self.hide()
        subprocess.run(['python', 'public/xy mode/xy_mode.py', str(rangeX), str(rangeY)])
        exit()
        
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

# Author: Sri Tirumalaraju
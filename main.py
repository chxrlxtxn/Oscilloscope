# importing libraries needed
import sys
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt
import subprocess

# Graphical User Interface Setup
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Arduino Oscilloscope')
        self.resize(300,50)
        layout = QVBoxLayout()

        # mode label
        self.modeLabel = QLabel()
        self.modeLabel.setText('Set Oscilloscope Mode')
        self.modeLabel.setFont(QFont('Aptos', 10))
        self.modeLabel.setAlignment(Qt.Alignment())
        layout.addWidget(self.modeLabel)

        # mode drop down
        self.modeCombo = QComboBox()
        self.modeCombo.addItems(['Rolling', 'Triggering', 'XY-Mode'])
        self.modeCombo.setFont(QFont('Aptos', 10))
        layout.addWidget(self.modeCombo)
        

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
        mode = self.modeCombo.currentText()
        self.hide()
        
        if mode == 'Rolling':
            subprocess.run(['python', 'public/rolling/settings.py'])
        elif mode == 'XY-Mode':
            subprocess.run(['python', 'public/xy mode/settings.py'])
        elif mode == 'Triggering':
            subprocess.run(['python', 'public/triggering/settings.py'])
        
        self.show()
        
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()


# Author: Sri Tirumalaraju
# importing libraries needed
import sys
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt
import subprocess

trigger = 3.3
range = 5

# Graphical User Interface Setup
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Oscilloscope Triggering Settings')
        self.resize(400,50)
        layout = QVBoxLayout()

        # mode label
        self.modeLabel = QLabel()
        self.modeLabel.setText('Set Triggering Mode')
        self.modeLabel.setFont(QFont('Aptos', 10))
        self.modeLabel.setAlignment(Qt.Alignment())
        layout.addWidget(self.modeLabel)

        # mode drop down
        self.modeCombo = QComboBox()
        self.modeCombo.addItems(['Auto', 'Normal', 'Single'])
        self.modeCombo.setFont(QFont('Aptos', 10))
        layout.addWidget(self.modeCombo)
        
        # trigger drop down
        self.edgeCombo = QComboBox()
        self.edgeCombo.addItems(['Rising-Edge', 'Falling-Edge', 'Level'])
        self.edgeCombo.setFont(QFont('Aptos', 10))
        layout.addWidget(self.edgeCombo)

        # trigger label
        self.triggerLabel = QLabel()
        self.triggerLabel.setText('Set Trigger Voltage')
        self.triggerLabel.setFont(QFont('Aptos', 10))
        self.triggerLabel.setAlignment(Qt.Alignment())
        layout.addWidget(self.triggerLabel)

        # trigger spin box
        self.spinBox = QDoubleSpinBox()
        self.spinBox.setMaximum(25)
        self.spinBox.setMinimum(0)
        self.spinBox.setValue(trigger)
        self.spinBox.setFont(QFont('Aptos', 10))
        layout.addWidget(self.spinBox)

        # channel drop down
        self.channelCombo = QComboBox()
        self.channelCombo.addItems(['Channel 1', 'Channel 2'])
        self.channelCombo.setFont(QFont('Aptos', 10))
        layout.addWidget(self.channelCombo)

        # range label
        self.rangeLabel = QLabel()
        self.rangeLabel.setText('Set Y Range (0 - 25)')
        self.rangeLabel.setFont(QFont('Aptos', 10))
        self.rangeLabel.setAlignment(Qt.Alignment())
        layout.addWidget(self.rangeLabel)

        # range spin box
        self.spinBoxY = QDoubleSpinBox()
        self.spinBoxY.setMaximum(25)
        self.spinBoxY.setMinimum(0)
        self.spinBoxY.setValue(range)
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
        global trigger, range
        mode = self.modeCombo.currentText()
        edge = self.edgeCombo.currentText()
        trigger = self.spinBox.value()
        channel = self.channelCombo.currentText()
        range = self.spinBoxY.value()
        self.hide()

        if mode == 'Auto':
            subprocess.run(['python', 'public/triggering/auto.py', edge, str(trigger), channel, str(range)])
        elif mode == 'Normal':
            subprocess.run(['python', 'public/triggering/normal.py', edge, str(trigger), channel, str(range)])
        elif mode == 'Single':
            subprocess.run(['python', 'public/triggering/single.py', edge, str(trigger), channel, str(range)])
        
        exit()
        
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

# Author: Sri Tirumalaraju
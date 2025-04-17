import serial
import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets, QtGui
import sys

# Setup serial connection
serialArduino = serial.Serial('COM3', 230400, timeout=0.02)  # Short timeout for non-blocking reads

# Wait for Arduino to initialize
if not serialArduino.is_open:
    serialArduino.open()

A0 = [0.00] * 50
A1 = [0.00] * 50

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # voltage vs time plot
        self.setWindowTitle("Arduino Oscilloscope - ROLLING MODE")
        self.plot_graph = pg.PlotWidget()
        self.setCentralWidget(self.plot_graph)
        self.plot_graph.setBackground("k")

        # pen style
        pen0 = pg.mkPen(color=(255, 255, 0), width=2, style=QtCore.Qt.SolidLine)
        pen1 = pg.mkPen(color=(0, 255, 0), width=2, style=QtCore.Qt.SolidLine)

        # axis styles
        styles = {"color": "white", "font-size": "12px"}
        self.plot_graph.setLabel("left", "Voltage", **styles)
        self.plot_graph.setLabel("bottom", "Time", **styles)
        self.plot_graph.showGrid(x=True, y=True)
        self.plot_graph.setYRange(0, float(sys.argv[1]))

        # initialization
        self.time = list(range(500))
        self.voltage0 = [0.00] * 500
        self.voltage1 = [0.00] * 500

        self.line0 = self.plot_graph.plot(self.time, self.voltage0, pen=pen0)
        self.line1 = self.plot_graph.plot(self.time, self.voltage1, pen=pen1)

        # timer setup
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

        # mouse coordinate label
        self.coordLabel = QtWidgets.QLabel("Y: __", self)
        self.coordLabel.setStyleSheet("color: white; font-size: 10px;")
        self.coordLabel.setGeometry(10,10,200,30)
        self.plot_graph.scene().sigMouseMoved.connect(self.mouse_move)

    def update_plot(self):
        global A0, A1

        if serialArduino.in_waiting > 0:
            try:
                serial_bytes = serialArduino.readline().decode().strip()
                analogpin = serial_bytes.split(", ")
                if len(analogpin) >= 100:
                    list_A0 = list(map(float, analogpin[0:50]))
                    A0 = [i * (5.00 / 4.00) for i in list_A0]
                    list_A1 = list(map(float, analogpin[50:100]))
                    A1 = [i * (30.00 / 5.00) for i in list_A1]

            except (IndexError, ValueError) as e:
                print(f"Error parsing serial data: {e}")

        # Update the plot data
        self.voltage0 = self.voltage0[50:] + A0
        self.voltage1 = self.voltage1[50:] + A1
        self.time = list(range(len(self.voltage0)))  # Adjust the time axis

        # Plot data
        self.line0.setData(self.time, self.voltage0)
        self.line1.setData(self.time, self.voltage1)

    def mouse_move(self, pos):
        if self.plot_graph.sceneBoundingRect().contains(pos):
            coord = self.plot_graph.plotItem.vb.mapSceneToView(pos)
            y = coord.y()
            self.coordLabel.setText(f"Y: {y:.2f}")

app = QtWidgets.QApplication([])
main = MainWindow()
main.show()
app.exec()

serialArduino.close()

# Author: Sri Tirumalaraju
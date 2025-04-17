import serial
import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets
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

        # voltage vs voltage plot
        self.setWindowTitle("Arduino Oscilloscope -  XY-MODE")
        self.plot_graph = pg.PlotWidget()
        self.setCentralWidget(self.plot_graph)
        self.plot_graph.setBackground("k")

        # pen style
        pen = pg.mkPen(color=(255, 255, 0), width=2, style=QtCore.Qt.SolidLine)

        # axis styles
        styles = {"color": "white", "font-size": "12px"}
        self.plot_graph.setLabel("bottom", "Channel 1 Voltage", **styles)
        self.plot_graph.setLabel("left", "Channel 2 Voltage", **styles)
        self.plot_graph.showGrid(x=True, y=True)
        self.plot_graph.setXRange(0, float(sys.argv[1]))
        self.plot_graph.setYRange(0, float(sys.argv[2]))

        # initialization
        self.voltage0 = [0.00] * 500
        self.voltage1 = [0.00] * 500

        # You need all the symbol info for when voltage is stable there is no line to draw
        self.xy = self.plot_graph.plot(self.voltage0, self.voltage1, pen=pen, symbol="o", symbolSize=1, symbolBrush='y', symbolPen=None)
        
        # timer setup
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

        # mouse coordinate label
        self.coordLabel = QtWidgets.QLabel("X:__, Y:__", self)
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

        # Plot data
        self.xy.setData(self.voltage0, self.voltage1)
    
    def mouse_move(self, pos):
        if self.plot_graph.sceneBoundingRect().contains(pos):
            coord = self.plot_graph.plotItem.vb.mapSceneToView(pos)
            x = coord.y()
            y = coord.y()
            self.coordLabel.setText(f"X:{x:.2f}, Y:{y:.2f}")

app = QtWidgets.QApplication([])
main = MainWindow()
main.show()
app.exec()

serialArduino.close()

# Author: Sri Tirumalaraju
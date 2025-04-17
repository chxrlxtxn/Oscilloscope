import serial
import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets, QtGui
import sys
import time

# Setup serial connection
serialArduino = serial.Serial('COM3', 230400, timeout=0.02)  # Short timeout for non-blocking reads

# Wait for Arduino to initialize
if not serialArduino.is_open:
    serialArduino.open()

voltage = [0.00] * 50

# triggering variable
trigger = float(sys.argv[2])
mode = sys.argv[1]

# check variables
trigger_hit = False # has the value been hit
low = False
high = False
count = 0

# runtime
total = 0

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # voltage vs time plot
        self.setWindowTitle("Arduino Oscilloscope - TRIGGERING MODE")
        self.plot_graph = pg.PlotWidget()
        self.setCentralWidget(self.plot_graph)
        self.plot_graph.setBackground("k")

        # pen style
        pen = pg.mkPen(color=(255, 255, 0), width=2, style=QtCore.Qt.SolidLine)

        # axis styles
        styles = {"color": "white", "font-size": "12px"}
        self.plot_graph.setLabel("left", "Voltage", **styles)
        self.plot_graph.setLabel("bottom", "Time", **styles)
        self.plot_graph.showGrid(x=True, y=True)
        self.plot_graph.setYRange(0, float(sys.argv[4]))

        # initialization
        self.time = list(range(500))
        self.voltage = [0.00] * 500

        # plotting data
        self.line = self.plot_graph.plot(self.time, self.voltage, pen=pen)

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
        global voltage, trigger, trigger_hit, high, low, count, mode, total

        if count < 9:
            if serialArduino.in_waiting > 0:
                try:
                    serial_bytes = serialArduino.readline().decode().strip()
                    analogpin = serial_bytes.split(", ")
                    if len(analogpin) >= 100:
                        if sys.argv[3] == 'Channel 1':
                            list_A0 = list(map(float, analogpin[0:50]))
                            voltage = [i * (5.00 / 4.00) for i in list_A0]
                        else:
                            list_A1 = list(map(float, analogpin[50:100]))
                            voltage = [i * (30.00 / 5.00) for i in list_A1]
                except (IndexError, ValueError) as e:
                    print(f"Error parsing serial data: {e}")

            # Update the plot data
            self.voltage = self.voltage[50:] + voltage
            self.time = list(range(len(self.voltage))) # Adjust the time axis

            self.line.setData(self.time, self.voltage)

            # triggering data
            if total > 10:
                if not trigger_hit:
                    if all(x > trigger for x in voltage):
                        if low and mode == 'Rising-Edge': # crossed trigger upwards
                            trigger_hit = True
                            count += 1
                        elif low and mode == 'Level': # crossed trigger for level
                            trigger_hit = True
                            count += 1

                        high = True
                        low = False
                    elif all(x < trigger for x in voltage):
                        if high and mode == 'Falling-Edge': # crossed trigger downwards
                            trigger_hit = True
                            count += 1
                        elif high and mode == 'Level': # crossed trigger for level
                            trigger_hit = True
                            count += 1

                        low = True
                        high = False
                    elif all(x == trigger for x in voltage):
                        if mode == 'Rising-Edge':
                            if low:
                                high = True
                                low = False
                                trigger_hit = True
                                count += 1

                        elif mode == 'Falling-Edge':
                            if high:
                                high = False
                                low = True
                                trigger_hit = True
                                count += 1

                        elif mode == 'Level':
                            trigger_hit = True
                            count += 1

                else:
                    count += 1                      

        else:
            # finalized plot
            self.plot_graph.setXRange(0,500)
            data = self.voltage
            self.line.setData(list(range(500)), data)
        
        total += 1

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
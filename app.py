from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
from matplotlib.gridspec import GridSpec
import merge_sensor_data as merge_sensor_data


class MainWindow(QtWidgets.QMainWindow):
    # send_fig = QtCore.pyqtSignal(str)

    def __init__(self):
        super(MainWindow, self).__init__()

        self.df = pd.read_csv(r'C:\Users\le\Desktop\Drone-Pallas2022/latest_merged.csv')
        self.df['datetime'] = pd.to_datetime(self.df['datetime'])

        self.main_widget = QtWidgets.QWidget(self)

        self.fig = Figure(figsize=(12, 9))
        self.gs = GridSpec(8, 12)
        self.ax1 = self.fig.add_subplot(self.gs[:-2, :])
        self.ax1_twin = self.ax1.twiny()
        self.ax2 = self.fig.add_subplot(self.gs[-1:, ::])
        self.ax2_twin = self.ax2.twinx()

        # self.ax1 = self.fig.add_subplot(121)
        # self.ax2 = self.fig.add_subplot(122, sharex=self.ax1, sharey=self.ax1)

        self.canvas = FigureCanvas(self.fig)

        self.canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                  QtWidgets.QSizePolicy.Expanding)
        self.canvas.updateGeometry()
        self.df_colnames = self.df.select_dtypes(include=np.number).columns.tolist()
        self.dropdownvar1 = QtWidgets.QComboBox()
        self.dropdownvar1.addItems(self.df_colnames)
        self.dropdownvar1.setCurrentIndex(
            [i for i, xx in enumerate(self.df_colnames)
             if 'temp' in xx][0])
        self.dropdownvar2 = QtWidgets.QComboBox()
        self.dropdownvar2.addItems(self.df_colnames)
        self.dropdownvar2.setCurrentIndex(
            [i for i, xx in enumerate(self.df_colnames)
             if 'rh' in xx][0])
        self.dropdownvary = QtWidgets.QComboBox()
        self.dropdownvary.addItems(self.df_colnames)
        self.dropdownvary.setCurrentIndex(
            [i for i, xx in enumerate(self.df_colnames)
             if 'press' in xx][0])

        self.dropdownvar1.currentIndexChanged.connect(self.update)
        self.dropdownvar2.currentIndexChanged.connect(self.update)
        self.dropdownvary.currentIndexChanged.connect(self.update)
        self.label = QtWidgets.QLabel("A plot:")

        self.layout = QtWidgets.QGridLayout(self.main_widget)
        self.layout.addWidget(QtWidgets.QLabel("Select category for var_1"))
        self.layout.addWidget(self.dropdownvar1)
        self.layout.addWidget(QtWidgets.QLabel("Select category for var_2"))
        self.layout.addWidget(self.dropdownvar2)
        self.layout.addWidget(QtWidgets.QLabel("Select category for var_y"))
        self.layout.addWidget(self.dropdownvary)

        self.layout.addWidget(self.canvas)

        self.setCentralWidget(self.main_widget)
        self.show()
        self.update()

        self.timer = QtCore.QTimer()
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        self.df = pd.read_csv(r'C:\Users\le\Desktop\Drone-Pallas2022/latest_merged.csv')
        self.df['datetime'] = pd.to_datetime(self.df['datetime'])
        # colors = ["b", "r", "g", "y", "k", "c"]
        for ax_ in [self.ax1, self.ax1_twin, self.ax2, self.ax2_twin]:
            ax_.clear()
            ax_.grid()

        self.var1 = self.dropdownvar1.currentText()
        self.var2 = self.dropdownvar2.currentText()
        self.vary = self.dropdownvary.currentText()

        self.ax1.set_ylabel(self.vary)
        self.ax1.set_xlabel(self.var1)
        self.ax1_twin.set_xlabel(self.var2)
        self.ax2.set_ylabel(self.var1)
        self.ax2_twin.set_ylabel(self.var2)

        self.ax1.plot(self.df[self.var1], self.df[self.vary], c='blue')
        self.ax1.xaxis.label.set_color('blue')
        self.ax1.tick_params(axis='x', colors='blue')

        self.ax1_twin.plot(self.df[self.var2], self.df[self.vary], c='red')
        self.ax1_twin.xaxis.label.set_color('red')
        self.ax1_twin.tick_params(axis='x', colors='red')

        self.ax2.plot(self.df['datetime'], self.df[self.var1], c='blue')
        self.ax2.yaxis.label.set_color('blue')
        self.ax2.tick_params(axis='y', colors='blue')
        self.ax2.set_xlabel('Time')

        self.ax2_twin.plot(self.df['datetime'], self.df[self.var2], c='red')
        self.ax2_twin.yaxis.label.set_color('red')
        self.ax2_twin.tick_params(axis='y', colors='red')

        self.fig.canvas.draw_idle()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())

# https://www.pythonguis.com/tutorials/plotting-matplotlib/

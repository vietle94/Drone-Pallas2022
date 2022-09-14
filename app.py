from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
from matplotlib.gridspec import GridSpec
import argparse
from PyQt5.QtWidgets import QSlider

opc_lab = ['b0_OPC-BP5',
           'b1_OPC-BP5', 'b2_OPC-BP5', 'b3_OPC-BP5', 'b4_OPC-BP5', 'b5_OPC-BP5',
           'b6_OPC-BP5', 'b7_OPC-BP5', 'b8_OPC-BP5', 'b9_OPC-BP5', 'b10_OPC-BP5',
           'b11_OPC-BP5', 'b12_OPC-BP5', 'b13_OPC-BP5', 'b14_OPC-BP5',
           'b15_OPC-BP5', 'b16_OPC-BP5', 'b17_OPC-BP5', 'b18_OPC-BP5',
           'b19_OPC-BP5', 'b20_OPC-BP5', 'b21_OPC-BP5', 'b22_OPC-BP5',
           'b23_OPC-BP5']


class MainWindow(QtWidgets.QMainWindow,):
    # send_fig = QtCore.pyqtSignal(str)

    def __init__(self, path_in):
        super(MainWindow, self).__init__()
        self.path_in = path_in

        # * means all if need specific format then *.csv
        self.list_of_files = glob.glob(self.path_in + '/*.csv')
        self.latest_file = max(self.list_of_files, key=os.path.getmtime)

        self.df = pd.read_csv(self.latest_file)
        self.df['datetime'] = pd.to_datetime(self.df['datetime'])
        total_volume = self.df['FlowRate_OPC-BP5']/60

        self.df['total_concentration_OPC-BP5'] = self.df.loc[:, opc_lab].sum(
            axis=1, min_count=1) / (total_volume)

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

        self.dropdownpath = QtWidgets.QComboBox()
        self.dropdownpath.addItems(self.list_of_files)
        self.dropdownpath.setCurrentText(self.latest_file)

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

        self.slider = QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(5000)
        self.slider.setMaximum(25000)
        self.slider.setValue(5000)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(5000)
        self.slider.setSingleStep(5000)

        self.dropdownvar1.currentIndexChanged.connect(self.update)
        self.dropdownvar2.currentIndexChanged.connect(self.update)
        self.dropdownvary.currentIndexChanged.connect(self.update)
        self.slider.valueChanged.connect(self.update_interval)

        # self.label = QtWidgets.QLabel("A plot:")

        self.layout = QtWidgets.QGridLayout(self.main_widget)
        self.layout.addWidget(QtWidgets.QLabel("Select file path"), 0, 0, 1, 2)
        self.layout.addWidget(self.dropdownpath, 1, 0, 1, 2)
        self.layout.addWidget(QtWidgets.QLabel("Select category for var_1"), 2, 0, 1, 1)
        self.layout.addWidget(self.dropdownvar1, 3, 0, 1, 1)
        self.layout.addWidget(QtWidgets.QLabel("Select category for var_2"), 2, 1, 1, 1)
        self.layout.addWidget(self.dropdownvar2, 3, 1, 1, 1)
        self.layout.addWidget(QtWidgets.QLabel("Select category for var_y"), 4, 0, 1, 1)
        self.layout.addWidget(self.dropdownvary, 5, 0, 1, 1)
        self.layout.addWidget(QtWidgets.QLabel("Update time (5000s to 25000s)"), 4, 1, 1, 1)
        self.layout.addWidget(self.slider, 5, 1, 1, 1)

        self.layout.addWidget(self.canvas, 6, 0, 1, 2)

        self.setCentralWidget(self.main_widget)
        self.show()
        self.update()
        self.update_interval()

        # self.timer = QtCore.QTimer()
        # self.timer.setInterval(5000)
        # self.timer.timeout.connect(self.update_plot)
        # self.timer.start()

    def update_interval(self):
        print('current update time is ', self.slider.value(), 's')
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.slider.value())
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        # * means all if need specific format then *.csv
        self.list_of_files = glob.glob(self.path_in + '/*.csv')
        self.latest_file = max(self.list_of_files, key=os.path.getmtime)
        print(self.latest_file)
        self.df = pd.read_csv(self.dropdownpath.currentText())
        self.df['datetime'] = pd.to_datetime(self.df['datetime'])
        total_volume = self.df['FlowRate_OPC-BP5']/60
        self.df['total_concentration_OPC-BP5'] = self.df.loc[:, opc_lab].sum(
            axis=1, min_count=1) / (total_volume)

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

        self.ax1.plot(self.df[self.var1], self.df[self.vary], '.', c='blue')
        self.ax1.xaxis.label.set_color('blue')
        self.ax1.tick_params(axis='x', colors='blue')

        self.ax1_twin.plot(self.df[self.var2], self.df[self.vary], '.', c='red')
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
    parser = argparse.ArgumentParser(description="Description for arguments")
    parser.add_argument("path_in", help="Input file", type=str)
    argument = parser.parse_args()
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow(argument.path_in)
    sys.exit(app.exec_())

# https://www.pythonguis.com/tutorials/plotting-matplotlib/
[(i, j) for i in range(5) for j in range(4)]

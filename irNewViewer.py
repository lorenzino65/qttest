import sys

import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.image import AxesImage
from matplotlib import cm
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout,
                               QHeaderView, QLabel, QMainWindow, QSlider,
                               QTableWidget, QTableWidgetItem, QVBoxLayout,
                               QLineEdit, QPushButton, QDialog, QWidget)
from ui_components.video import VideoPanel
from ui_components.menu import TopBarMenu


class ApplicationWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        # Central widget
        self._main = QWidget()
        self.setCentralWidget(self._main)

        # Main menu bar
        self.top_menu = TopBarMenu()
        self.setMenuBar(self.top_menu)

        # Main layout
        layout = QHBoxLayout(self._main)
        self.video_panel = VideoPanel()
        layout.addLayout(self.video_panel)

        # Signal and Slots connections
        # self.slider.valueChanged.connect(self.rotate_azim)
        # Initial setup
        # self._ax.view_init(30, 30)
        # self.slider_azim.setValue(30)
        # self.slider_elev.setValue(30)
        # self.fig.canvas.mpl_connect("button_release_event", self.on_click)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ApplicationWindow()
    w.setFixedSize(1280, 720)
    w.show()
    app.exec()

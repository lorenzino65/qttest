from PySide6.QtGui import QAction
from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import (QLabel, QHBoxLayout, QVBoxLayout, QMenuBar,
                               QLineEdit, QMenu, QPushButton, QDialog,
                               QMessageBox, QComboBox)
from .submenu.color_menu import ColorMapMenu
from .submenu.norm_menu import NormMenu


class MenuView(QMenu):

    def __init__(self, parent):
        QMenu.__init__(self, title="&View", parent=parent)

        self.color_norm_menu = NormMenu()
        self.addMenu(self.color_norm_menu)

        self.color_map_menu = ColorMapMenu()
        self.addMenu(self.color_map_menu)

        self.orientation_menu = self.addMenu("Orientation")
        self.orientation_menu.reverseX_action
        self.orientation_menu.reverseY_action
        self.orientation_menu.transpose_action
        self.orientation_menu.addAction(self.orientation_menu.reverseX_action)
        self.orientation_menu.addAction(self.orientation_menu.reverseY_action)
        self.orientation_menu.addAction(self.orientation_menu.transpose_action)
        self.percentile_action
        self.addAction(self.percentile_action)
        self.subtract_background_action
        self.addAction(self.subtract_background_action)

    def get_defaults(self):
        return {
            'map_type': 'Sequential (2)',
            'map_color': 'gray',
            'norm_type': "Linear"
        }

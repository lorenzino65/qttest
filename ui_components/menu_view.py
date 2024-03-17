from PySide6.QtGui import QAction
from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import (QLabel, QHBoxLayout, QVBoxLayout, QMenuBar,
                               QLineEdit, QMenu, QPushButton, QDialog,
                               QMessageBox, QComboBox)
from .submenu.color_menu import ColorMapMenu
from .submenu.norm_menu import NormMenu


class MenuView(QMenu):

    # Passing the function here is terrible, I cannot find a better solution, maybe make the video open the dialog itself (seems clunky)
    def __init__(self, parent, get_percentile_function):
        QMenu.__init__(self, title="&View", parent=parent)

        self.color_norm_menu = NormMenu()
        self.addMenu(self.color_norm_menu)

        self.color_map_menu = ColorMapMenu()
        self.addMenu(self.color_map_menu)

        self.orientation_menu = self.addMenu("Orientation")
        self.orientation_menu.orientation_changed = Signal(str, bool)
        self.orientation_menu.reverseX_action = QAction('Reverse X',
                                                        self.orientation_menu,
                                                        checkable=True)
        self.orientation_menu.reverseY_action = QAction('Reverse Y',
                                                        self.orientation_menu,
                                                        checkable=True)
        self.orientation_menu.transpose_action = QAction('Transpose',
                                                         self.orientation_menu,
                                                         checkable=True)
        self.orientation_menu.addAction(self.orientation_menu.reverseX_action)
        self.orientation_menu.addAction(self.orientation_menu.reverseY_action)
        self.orientation_menu.addAction(self.orientation_menu.transpose_action)

        self.percentile_changed = Signal(float, float)
        self.addAction(
            QAction(self,
                    "Change Percentile",
                    triggered=lambda: self.open_percentile_dialog(
                        self.percentile_changed)))
        self.subtract_background_action = QAction('Subtract background',
                                                  self,
                                                  checkable=True)
        self.addAction(self.subtract_background_action)

    def get_defaults(self):
        return {
            'map_type': 'Sequential (2)',
            'map_color': 'gray',
            'norm_type': "Linear",
            'reverse_x': False,
            'reverse_y': False,
            'transpose': False,
            'subtract_background': False,
        }

    def open_percentile_dialog(self, get_percentile_function):
        dialog = ChoosePercentDialog(self, get_percentile_function())
        if dialog.exec():
            self.percentile_changed.emit(dialog.get_selection())
            print("Percentile changed")


class ChoosePercentDialog(QDialog):

    def __init__(self, min, max, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Set Percentile")
        layout = QVBoxLayout()

        upper_layout = QHBoxLayout()
        upper_layout.addWidget(QLabel("Upper:"))
        self.upper_value = QLineEdit()
        self.upper_value.setText(str(max))
        upper_layout.addWidget(self.upper_value)
        layout.addLayout(self.upper_layout)

        lower_layout = QHBoxLayout()
        lower_layout.addWidget(QLabel("Lower:"))
        self.lower_value = QLineEdit()
        self.lower_value.setText(str(min))
        lower_layout.addWidget(self.lower_value)
        layout.addLayout(self.lower_layout)

        self.current_vmin = min
        self.current_vmax = max
        button_ok = QPushButton("OK")
        button_ok.clicked.connect(self.check_selection)
        layout.addWidget(button_ok)

        self.setLayout(layout)

        @Slot()
        def check_selection(self):
            try:
                vmin, vmax = float(self.gamma_value.text())
                if vmin > 1 or vmin < 0 or vmax > 1 or vmax < 0 or vmax < vmin:
                    button = QMessageBox.critical(
                        self,
                        "Out Of Range",
                        "Lower and Upper must stay between 0 and 1",
                        buttons=QMessageBox.Ok,
                        defaultButton=QMessageBox.Ok,
                    )
                    if button == QMessageBox.Ok:
                        self.lower_value.setText(self.current_vmin)
                        self.upper_value.setText(self.current_vmax)
                else:
                    self.accept()
            except Exception:
                button = QMessageBox.critical(
                    self,
                    "Wrong Input",
                    "Lower and Upeer must be float between 0 and 1",
                    buttons=QMessageBox.Ok,
                    defaultButton=QMessageBox.Ok)
                if button == QMessageBox.Ok:
                    self.lower_value.setText(self.current_vmin)
                    self.upper_value.setText(self.current_vmax)

    def get_selection(self):
        return float(self.upper_value.text()), float(self.lower_value.text())

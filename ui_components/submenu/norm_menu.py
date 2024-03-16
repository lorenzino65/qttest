from PySide6.QtGui import QAction
from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import (QLabel, QHBoxLayout, QVBoxLayout, QMenuBar,
                               QLineEdit, QMenu, QPushButton, QDialog,
                               QMessageBox, QComboBox)
import matplotlib.colors as colors


class NormMenu(QMenu):

    def __init__(self):
        QMenu.__init__(self, "Color Normalization")
        self.current_gamma = 0
        self.norm_chosen = Signal(str, float)  # type and gamma if necessary
        self.addAction(
            QAction(self.color_norm_menu,
                    'Linear',
                    triggered=lambda: self.call_color_map_signal('Linear')))
        self.addAction(
            QAction(self.color_norm_menu,
                    'Log',
                    triggered=lambda: self.call_color_map_signal('Log')))
        self.addAction(
            QAction(self.color_norm_menu,
                    'Power',
                    triggered=lambda: self.call_color_map_signal('Power')))
        # Signal
        self.norm_chosen.connect(self.update_gamma)

    def call_color_map_signal(self, norm_type):
        if norm_type == "Power":
            dialog = ChooseGammaNorm(self, self.current_gamma)
            if dialog.exec():
                self.norm_chosen.emit(norm_type, float(dialog.get_gamma()))
                print("gamma chosen")

        self.norm_chosen.emit(norm_type, 0)  # 0 is unused for this types

    @Slot()
    def update_gamma(self, norm_type, gamma):
        if norm_type == "Power":
            self.current_gamma = gamma


class ChooseGammaNorm(QDialog):

    def __init__(self, parent, current_gamma):
        super().__init__(parent)

        self.setWindowTitle("Choose Gamma")
        gamma_layout = QHBoxLayout()
        gamma_layout.addWidget(QLabel("Enter Gamma:"))
        self.current_gamma = str(current_gamma)
        self.gamma_value = QLineEdit()
        self.gamma_value.setText(self.current_gamma)
        gamma_layout.addWidget(self.gamma_value)
        button_ok = QPushButton("OK")
        button_ok.clicked.connect(self.check_gamma)
        gamma_layout.addWidget(button_ok)

        self.setLayout(gamma_layout)

        @Slot()
        def check_gamma(self):
            try:
                gamma = float(self.gamma_value.text())
                if gamma > 1 or gamma < 0:
                    button = QMessageBox.critical(
                        self,
                        "Out Of Range",
                        "Gamma must stay between 0 and 1",
                        buttons=QMessageBox.Ok,
                        defaultButton=QMessageBox.Ok,
                    )
                    if button == QMessageBox.Ok:
                        self.gamma_value.setText(self.current_gamma)
                else:
                    self.accept()
            except Exception:
                button = QMessageBox.critical(
                    self,
                    "Wrong Input",
                    "Gamma must be a float between 0 and 1",
                    buttons=QMessageBox.Ok,
                    defaultButton=QMessageBox.Ok)
                if button == QMessageBox.Ok:
                    self.gamma_value.setText(self.current_gamma)

        def get_gamma(self):
            return self.gamma_value.text()

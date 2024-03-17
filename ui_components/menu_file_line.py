from PySide6.QtGui import QAction
from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import (QLabel, QHBoxLayout, QVBoxLayout, QLineEdit,
                               QMenu, QPushButton, QDialog, QComboBox)
import Sektor7Unten
import Sektor7Oben
import Sektor9Tauchrohr
import Sektor9Zeile


class MenuFileAndLine(QMenu):

    def __init__(self, parent=None):
        QMenu.__init__(self, title="&File", parent=parent)

        self.open_action = OpenAction(self)
        self.open_action.setShortcut("Ctrl+o")
        self.addAction(self.open_action)

        self.line_signal = Signal(str)
        create_line_action = LineAction(self, self.line_signal, "Create")
        create_line_action.setShortcut("Ctrl+l")
        self.addAction(create_line_action)
        save_line_action = LineAction(self, self.line_signal, "Save")
        save_line_action.setShortcut("Ctrl+s")
        self.addAction(save_line_action)


class LineAction(QAction):

    def __init__(self, parent, signal, reason):
        QAction.__init__(self,
                         reason + " Line",
                         parent,
                         triggered=self.call_line_signal)
        self.clicked = signal
        self.reason = reason

    def call_line_signal(self):
        self.clicked.emit(self.reason)


class OpenAction(QAction):

    def __init__(self, parent):
        QAction.__init__(self,
                         "Open",
                         parent,
                         triggered=self.open_experiment_dialog)
        self.success = Signal(str, int)

    def open_experiment_dialog(self):
        dialog = ChooseExperimentDialog(self)
        if dialog.exec():
            self.success.emit(dialog.get_selection())
            print("file chosen")


class ChooseExperimentDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Choose Experiment")
        layout = QVBoxLayout()

        self.combo_camera = QComboBox()
        self.cameras = {
            'Sektor 7 Unten': Sektor7Unten.pulseList,
            'Sektor 9 Tauchrohr': Sektor9Tauchrohr.pulseList,
            'Sektor 9 Zeile': Sektor9Zeile.pulseList,
            'Sektor 7 Oben': Sektor7Oben.pulseList,
        }
        self.combo_camera.addItems(self.cameras.keys())
        self.combo_camera.currentTextChanged.connect(self.on_camera_select)
        layout.addWidget(self.combo_camera)

        self.number_layout = QHBoxLayout()
        self.number_layout.addWidget(QLabel("Enter the number:"))
        self.combo_experiment = QComboBox()
        self.combo_experiment.setLineEdit(QLineEdit())
        self.number_layout.addWidget(self.combo_experiment)

        layout.addLayout(self.number_layout)

        self.button_ok = QPushButton("OK")
        self.button_ok.clicked.connect(self.accept)
        layout.addWidget(self.button_ok)

        self.setLayout(layout)

    @Slot()
    def on_camera_select(self, camera):
        self.combo_experiment.clear()
        self.combo_experiment.insertItems(
            [str(el) for el in self.cameras[camera]()])

    def get_selection(self):
        if self.combo_experiment.currentText():
            return self.combo_camera.currentText(), int(
                self.combo_experiment.currentText())

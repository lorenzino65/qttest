from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import (QLabel, QHBoxLayout, QVBoxLayout, QMenuBar,
                               QLineEdit, QMenu, QPushButton, QDialog,
                               QComboBox)
import testVideo
import JadeIII
import IRCam
import IRCam2
import Sektor7Unten
import Sektor7Oben
import Sektor9Tauchrohr
import Sektor9Zeile
import IRLab


class TopBarMenu(QMenuBar):

    def __init__(self, parent=None):
        QMenuBar.__init__(self, parent)

        self.menu_file = self.addMenu("&File")
        self.menu_file.open_action = OpenAction(self)
        self.menu_file.open_action.setShortcut("Ctrl+o")
        self.menu_file.addAction(self.menu_file.open_action)
        self.menu_file.line_signal = Signal(bool)
        self.menu_file.line_action = CreateLineAction(
            self, self.menu_file.line_signal)
        self.menu_file.line_action.setShortcut("Ctrl+l")
        self.menu_file.addAction(self.menu_view.line_action)
        self.menu_file.save_line_action
        self.menu_file.addAction(self.menu_view.save_line_action)

        self.menu_view = MenuView(self)
        self.addMenu(self.menu_view)


class MenuView(QMenu):

    def __init__(self, parent=None):
        QMenu.__init__(self, title="&File", parent=parent)

        self.color_map_menu = self.addMenu("Color Map")
        self.orientation_menu = self.addMenu("Orientation")
        self.orientation_menu.reverseX_action
        self.orientation_menu.reverseY_action
        self.orientation_menu.transpose_action
        self.orientation_menu.addAction(self.orientation_menu.reverseX_action)
        self.orientation_menu.addAction(self.orientation_menu.reverseY_action)
        self.orientation_menu.addAction(self.orientation_menu.transpose_action)
        self.gamma_action
        self.addAction(self.gamma_action)
        self.percentile_action
        self.addAction(self.percentile_action)
        self.subtract_background_action
        self.addAction(self.subtract_background_action)


class CreateLineAction(QAction):

    def __init__(self, parent, signal):
        QAction.__init__(self,
                         "Create Line",
                         parent,
                         triggered=self.start_line_creation)
        self.clicked = signal

    def start_line_creation(self):
        self.clicked.emit(True)


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
            self.success.emit(dialog.getSelection())
            print("file chosen")


class ChooseExperimentDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Choose Experiment")
        self.layout = QVBoxLayout()

        self.combo_camera = QComboBox()
        self.cameras = {
            'Jade III': JadeIII.pulseList,
            'IRCam': IRCam.pulseList,
            'Test Video': testVideo.pulseList,
            'IRCam2': IRCam2.pulseList,
            'Sektor 7 Unten': Sektor7Unten.pulseList,
            'Sektor 9 Tauchrohr': Sektor9Tauchrohr.pulseList,
            'Sektor 9 Zeile': Sektor9Zeile.pulseList,
            'Sektor 7 Oben': Sektor7Oben.pulseList,
            'IRLab': IRLab.pulseList,
        }
        self.combo_camera.addItems(self.cameras.keys())
        self.combo_camera.currentTextChanged.connect(self.onCameraSelect)
        self.layout.addWidget(self.combo_camera)

        self.number_layout = QHBoxLayout()
        self.number_layout.addWidget(QLabel("Enter the number:"))
        self.combo_experiment = QComboBox()
        self.combo_experiment.setLineEdit(QLineEdit())
        self.number_layout.addWidget(self.combo_experiment)

        self.layout.addLayout(self.number_layout)

        self.button_ok = QPushButton("OK")
        self.button_ok.clicked.connect(self.accept)
        self.layout.addWidget(self.button_ok)

        self.setLayout(self.layout)

    @Slot()
    def onCameraSelect(self, camera):
        self.combo_experiment.clear()
        self.combo_experiment.insertItems(
            [str(el) for el in self.cameras[camera]()])

    def getSelection(self):
        if self.combo_experiment.currentText():
            return self.combo_camera.currentText(), int(
                self.combo_experiment.currentText())

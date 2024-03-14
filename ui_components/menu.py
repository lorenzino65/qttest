from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtCore import Slot
from PySide6.QtWidgets import (QLabel, QHBoxLayout, QVBoxLayout, QMenuBar,
                               QLineEdit, QPushButton, QDialog, QComboBox)
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
        openAction = QAction("Open",
                             self,
                             triggered=self.open_experiment_dialog)
        openAction.setShortcut("Ctrl+O")
        self.menu_file.addAction(openAction)
        colorMapMenu = self.menu_file.addMenu("Color Map")

    def open_experiment_dialog(self):
        dialog = ChooseExperimentDialog(self)
        if dialog.exec():
            camera, pulseNumber = dialog.getSelection()
            print(pulseNumber)


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

from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QSlider,
    QLineEdit,
    QPushButton,
)


class VideoCommands(QHBoxLayout):

    def __init__(self, parent=None):
        QHBoxLayout.__init__(self)
        # Sliders (Left)
        min = 0
        max = 360
        self.slider = QSlider(minimum=min,
                              maximum=max,
                              orientation=Qt.Horizontal)
        self.slider_button_back = QPushButton("<")
        self.slider_button_back.setFixedSize(30, 25)
        self.slider_button_next = QPushButton(">")
        self.slider_button_next.setFixedSize(30, 25)
        self.frame_counter = QLineEdit()
        self.frame_counter.setText(str(self.currentFrame))

        self.addWidget(self.slider_button_back, 1)
        self.addWidget(self.slider, 88)
        self.addWidget(self.slider_button_next, 1)
        self.addWidget(self.frame_counter, 5)

        self.updateFrame = Signal(int)
        self.updateTime = Signal(float)  # dont know why exist, but it's there

        self.slider_button_back.clicked.connect(
            lambda: self.update(self.slider.value() - 1))
        self.slider.valueChanged.connect(self.update)
        self.slider_button_next.clicked.connect(
            lambda: self.update(self.slider.value() + 1))
        self.frame_counter.textEdited.connect(self.update_float)

    @Slot()
    def update(self, value):
        self.updateFrame.emit(value)

    @Slot()
    def update_float(self, value):
        self.updateTime.emit(float(value))

    def setAll(self, value):
        self.slider.setValue(value)
        self.frame_counter.setText(str(value))

    def reset(self):
        self.setAll(0)

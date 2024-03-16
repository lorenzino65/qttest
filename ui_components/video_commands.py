from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QSlider,
    QLineEdit,
    QPushButton,
)


class VideoCommands(QHBoxLayout):

    def __init__(self):
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
        self.time_counter = QLineEdit()
        self.time_counter.setText(0)

        self.addWidget(self.slider_button_back, 1)
        self.addWidget(self.slider, 88)
        self.addWidget(self.slider_button_next, 1)
        self.addWidget(self.time_counter, 5)

        self.updateFrame = Signal(int)
        self.updateTime = Signal(float)  # dont know why exist, but it's there

        self.slider_button_back.clicked.connect(
            lambda: self.update(self.slider.value() - 1))
        self.slider.valueChanged.connect(self.update)
        self.slider_button_next.clicked.connect(
            lambda: self.update(self.slider.value() + 1))
        self.time_counter.textEdited.connect(self.update_float)

    @Slot()
    def update(self, value):
        self.updateFrame.emit(value)

    @Slot()
    def update_float(self, value):
        self.updateTime.emit(float(value))

    def set_range(self, min, max):
        self.slider.setRange(min, max)

    def set_all(self, index, time):
        self.slider.setValue(index)
        self.time_counter.setText(str(time))

    def reset(self):
        self.set_all(0, 0)

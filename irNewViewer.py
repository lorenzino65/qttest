import sys

from PySide6.QtWidgets import (QApplication, QWidget, QHBoxLayout, QMainWindow)
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

        # Signals
        self.top_menu.menu_file.open_action.success.connect(
            self.video_panel.openVideo)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ApplicationWindow()
    w.setFixedSize(1280, 720)
    w.show()
    app.exec()

import sys

from PySide6.QtCore import Slot
from PySide6.QtWidgets import (QApplication, QWidget, QHBoxLayout, QMenuBar,
                               QMainWindow)
from ui_components.video import VideoPanel
from ui_components.menu_file_line import MenuFileAndLine
from ui_components.menu_view import MenuView
from configparser import ConfigParser


class ApplicationWindow(QMainWindow):

    def __init__(self, config_path):
        QMainWindow.__init__(self, None)
        self.config = ConfigParser()
        self.config.read(config_path)
        self.config_path = config_path

        # Central widget
        self._main = QWidget()
        self.setCentralWidget(self._main)

        # Main menu bar
        self.top_menu = self.setMenuBar(QMenuBar(self))
        self.menu_file = MenuFileAndLine(self)
        self.top_menu.addMenu(self.menu_file)
        self.menu_view = MenuView(self)

        self.top_menu.addMenu(self.menu_view)

        # Main layout
        layout = QHBoxLayout(self._main)
        self.video_panel = VideoPanel()
        layout.addLayout(self.video_panel)

        # Signals
        self.menu_file.open_action.success.connect(self.video_panel.open_video)
        self.menu_file.line_signal.connect(self.video_panel.line_control)
        self.menu_view.color_map_menu.color_chosen.connect(
            self.video_panel.set_color_map)
        self.menu_view.color_map_menu.color_chosen.connect(
            self.save_color_map_config)
        self.menu_view.color_norm_menu.norm_chosen.connect(
            self.video_panel.set_norm)
        self.menu_view.color_norm_menu.norm_chosen.connect(
            self.save_color_norm_config)

        if 'view' not in self.config.sections():
            self.save_config('view', self.menu_view.get_default())

        self.color_map_menu.color_chosen.emit(
            self.config.get('view', 'map_type'),
            self.config.get('view', 'map_color'))
        norm_type = self.config.get('view', 'norm_type')
        if norm_type == "Power":
            self.colornorm_menu.norm_chosen.emit(
                norm_type, self.config.get('view', 'gamma'))
        else:
            self.colornorm_menu.norm_chosen.emit(norm_type, 0)

    def save_config(self, category, configs):
        for name in configs.keys():
            self.config.set(category, name, configs[name])
        with open(self.config_path, 'w') as f:
            self.config.write(f)

    @Slot()
    def save_color_map_config(self, map_type, map_color):
        self.save_config('view', {
            'map_type': map_type,
            'map_color': map_color
        })

    @Slot()
    def save_color_norm_config(self, norm_type, gamma):
        configs = {'norm_type': norm_type}
        if norm_type == "Power":
            configs.gamma = gamma
        self.save_config('view', configs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ApplicationWindow('config/config.ini')
    w.setFixedSize(1280, 720)
    w.show()
    app.exec()

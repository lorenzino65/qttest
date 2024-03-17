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

        # Main layout
        layout = QHBoxLayout(self._main)
        self.video_panel = VideoPanel()
        layout.addLayout(self.video_panel)

        # Main menu bar
        self.top_menu = self.setMenuBar(QMenuBar(self))
        self.menu_file = MenuFileAndLine(self)
        self.top_menu.addMenu(self.menu_file)
        self.menu_view = MenuView(
            self,
            self.video_panel.get_percentile_vmin_vmax)  # the bad function
        self.top_menu.addMenu(self.menu_view)

        # Signals
        self.menu_file.open_action.success.connect(self.video_panel.open_video)
        self.menu_file.line_signal.connect(self.video_panel.line_control)
        self.menu_view.color_map_menu.color_chosen.connect(
            self.video_panel.set_color_map)
        self.menu_view.color_norm_menu.norm_chosen.connect(
            self.video_panel.set_norm)
        self.menu_view.orientation_menu.reverseX_action.toggled.connect(
            self.video_panel.set_reverseX)
        self.menu_view.orientation_menu.reverseY_action.toggled.connect(
            self.video_panel.set_reverseY)
        self.menu_view.orientation_menu.transpose_action.toggled.connect(
            self.video_panel.set_transpose)
        self.menu_view.remove_background_action.toggled.connect(
            self.video_panel.set_remove_background)
        self.menu_view.percentile_changed.connect(
            self.video_panel.set_percentile_vmin_vmax)

        # Config
        self.menu_view.color_map_menu.color_chosen.connect(
            self.save_color_map_config)
        self.menu_view.color_norm_menu.norm_chosen.connect(
            self.save_color_norm_config)
        self.menu_view.orientation_menu.reverseX_action.toggled.connect(
            self.save_reverseX_config)
        self.menu_view.orientation_menu.reverseY_action.toggled.connect(
            self.save_reverseY_config)
        self.menu_view.orientation_menu.transpose_action.toggled.connect(
            self.save_transpose_config)
        self.menu_view.remove_background_action.toggled.connect(
            self.save_remove_background_config)

        self.view_title = "View"
        if self.view_title not in self.config.sections():
            self.save_config(self.view_title, self.menu_view.get_default())

        norm_type = self.config.get(self.view_title, 'norm_type')
        if norm_type == "Power":
            self.menu_view.color_norm_menu.norm_chosen.emit(
                norm_type, self.config.get(self.view_title, 'gamma'))
        else:
            self.menu_view.color_norm_menu.norm_chosen.emit(norm_type, 0)
        self.menu_view.color_map_menu.color_chosen.emit(
            self.config.get(self.view_title, 'map_type'),
            self.config.get(self.view_title, 'map_color'))
        self.menu_view.orientation_menu.reverseX_action.setChecked(
            self.config.get(self.view_title, 'reverse_x'))
        self.menu_view.orientation_menu.reverseY_action.setChecked(
            self.config.get(self.view_title, 'reverse_y'))
        self.menu_view.orientation_menu.transpose_action.setChecked(
            self.config.get(self.view_title, 'transpose'))
        self.menu_view.remove_background_action.setChecked(
            self.config.get(self.view_title, 'remove_background'))

    def save_config(self, category, configs):
        for name in configs.keys():
            self.config.set(category, name, configs[name])
        with open(self.config_path, 'w') as f:
            self.config.write(f)

    @Slot()
    def save_color_map_config(self, map_type, map_color):
        self.save_config(self.view_title, {
            'map_type': map_type,
            'map_color': map_color
        })

    @Slot()
    def save_color_norm_config(self, norm_type, gamma):
        configs = {'norm_type': norm_type}
        if norm_type == "Power":
            configs.gamma = gamma
        self.save_config(self.view_title, configs)

    def save_checkable_options_config(self, checkable_type, checked):
        if self.config.get(self.view_title, checkable_type) != checked:
            configs = {checkable_type: checked}
            self.save_config(self.view_title, configs)

    @Slot()
    def save_reverseX_config(self, checked):
        self.save_checkable_options_config('reverse_x', checked)

    @Slot()
    def save_reverseY_config(self, checked):
        self.save_checkable_options_config('reverse_y', checked)

    @Slot()
    def save_transpose_config(self, checked):
        self.save_checkable_options_config('transpose', checked)

    @Slot()
    def save_remove_background_config(self, checked):
        self.save_checkable_options_config("remove_background", checked)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ApplicationWindow('config/config.ini')
    w.setFixedSize(1280, 720)
    w.show()
    app.exec()

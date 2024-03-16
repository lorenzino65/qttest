from PySide6.QtGui import QAction
from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QMenu


class ColorMapMenu(QMenu):

    def __init__(self, parent):
        QMenu.__init__(self, title="&File", parent=parent)
        self.current_color = ''
        self.current_type = ''
        maps = {
            'Perceptually Uniform Sequential':
            ['viridis', 'plasma', 'inferno', 'magma', 'cividis'],
            'Sequential': [
                'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
                'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu',
                'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn'
            ],
            'Sequential (2)': [
                'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
                'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
                'hot', 'afmhot', 'gist_heat', 'copper'
            ],
            'Miscellaneous': [
                'flag', 'prism', 'ocean', 'gist_earth', 'terrain',
                'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix',
                'brg', 'gist_rainbow', 'rainbow', 'jet', 'turbo',
                'nipy_spectral', 'gist_ncar'
            ]
        }

        self.color_chosen = Signal(str, str)
        for type in maps.keys():
            menu_type = QMenu(title=type, parent=self)
            for col in maps:
                menu_type[col] = ColorMapAction(self, self.color_chosen,
                                                menu_type.title, col)
                menu_type.addAction(menu_type[col])
            self[type] = menu_type

        # Signal
        self.color_chosen.connect(self.disable_color)

    @Slot()
    def disable_color(self, map_type, map_color):
        if self.current_color != map_color:
            self[self.current_type][self.current_color].setDisable(False)
            self[map_type][map_color].setDisable(True)
            self.current_color = map_color
            self.current_type = map_type


class ColorMapAction(QAction):

    def __init__(self, parent, signal, map_type, color):
        QAction.__init__(self,
                         color,
                         parent,
                         triggered=self.call_color_map_signal)
        self.clicked = signal
        self.color = color
        self.map_type = map_type

    def call_color_map_signal(self):
        self.clicked.emit(self.map_type, self.color)

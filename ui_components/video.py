import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure
import matplotlib.colors as colors
from matplotlib import colormaps
from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
)
import ir
import Sektor7Unten
import Sektor7Oben
import Sektor9Tauchrohr
import Sektor9Zeile
from .video_commands import VideoCommands
from .line import Line


class VideoPanel(QVBoxLayout):

    def __init__(self, parent=None):
        QVBoxLayout.__init__(self)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.figure.set_canvas(self.canvas)
        # self.axes = self.canvas.figure.add_subplot(111)
        self.axes = self.canvas.figure.add_axes([0, 0, 1, 1])
        self.image = self.axes.imshow(np.zeros((640, 512)),
                                      cmap='gray',
                                      vmin=0.1,
                                      vmax=0.99)
        # for tick in self.axes.get_xticklabels():
        #     tick.set_visible(False)
        # for tick in self.axes.get_yticklabels():
        #     tick.set_visible(False)
        self.axes.set_axis_off()
        self.axes.set_xlim(0, 511)
        self.axes.set_ylim(0, 511)
        self.axes.set_aspect(1)

        self.cmap = colormaps['gray']
        self.vmin = 0.1
        self.vmax = 0.99
        self.norm = colors.Normalize()
        self.reverseX = 1
        self.reverseY = 1
        self.transpose = False
        self.remove_background = False

        self.is_video_loaded = False
        self.current_frame = 0
        self.canvas.draw()

        # Layout
        # self.addWidget(self.title,)
        self.addWidget(self.canvas, 90)
        self.commands = VideoCommands()
        self.addLayout(self.commands, 7)

        # Signals
        self.commands.updateFrame.connect(self.set_frame)
        self.commands.updateTime.connect(self.set_time)  # Still dont know

    def get_video(camera, experiment_number):
        videos = {
            'Sektor 7 Unten': Sektor7Unten.video,
            'Sektor 9 Tauchrohr': Sektor9Tauchrohr.video,
            'Sektor 9 Zeile': Sektor9Zeile.video,
            'Sektor 7 Oben': Sektor7Oben.video,
        }
        return videos[camera](experiment_number)

    def get_movement(camera, experiment_number):
        movement = {
            'Sektor 7 Unten': Sektor7Unten.movement,
            'Sektor 9 Tauchrohr': Sektor9Tauchrohr.movement,
            'Sektor 9 Zeile': Sektor9Zeile.movement,
            'Sektor 7 Oben': Sektor7Oben.movement,
        }
        return movement[camera](experiment_number)

    def get_movement_now(self):
        return self.movement(self.video.time[self.current_frame])

    @Slot()
    def open_video(self, camera, experiment_number):
        self.video = self.get_video(camera, experiment_number)
        self.movement = self.get_movement(camera, experiment_number)
        self.name = camera
        self.is_video_loaded = True

        self.image.set_norm(self.norm)
        self.image.set_cmap(self.cmap)
        self.commands.set_range(0, self.video.header.nFrames - 1)
        self.commands.reset()
        self.set_frame(0)

    def remove_line(self):
        try:
            del self.line
        except Exception as Error:
            print(Error)

    def add_line(self):
        self.remove_line()
        line, = self.axes.plot([0], [0], 'r')
        self.line = Line(self, line)

    @Slot()
    def line_control(self, reason):
        match reason:
            case "Create":
                self.add_line()
            case "Save":
                if not self.line or not self.line.isValid:
                    raise Exception('Line not valid')
                self.line.save_line()
            case _:
                print("Something broke")

    @Slot()
    def set_norm(self, norm_type, gamma):
        match norm_type:
            case "Linear":
                self.norm = colors.Normalize()
            case "Log":
                self.norm = colors.LogNorm()
            case "Power":
                self.norm = colors.PowerNorm(gamma=gamma)
            case _:
                print("Something broke with norms")

        if self.is_video_loaded:
            self.image.set_norm(self.norm)
            self.canvas.draw()

    @Slot()
    def set_color_map(self, _, color):
        self.cmap = colormaps[color]
        if self.is_video_loaded:
            self.image.set_cmap(self.cmap)
            self.canvas.draw()

    @Slot()
    def set_reverseX(self, checked):
        if checked:
            self.reverseX = -1
        else:
            self.reverseX = 1
        if self.is_video_loaded:
            self.set_frame(self.current_frame)

    @Slot()
    def set_reverseY(self, checked):
        if checked:
            self.reverseY = -1
        else:
            self.reverseY = 1
        if self.is_video_loaded:
            self.set_frame(self.current_frame)

    @Slot()
    def set_transpose(self, checked):
        self.transpose = checked
        if self.is_video_loaded:
            self.set_frame(self.current_frame)

    def get_percentile_vmin_vmax(self):
        return self.vmin, self.vmax

    @Slot()
    def set_percentile_vmin_vmax(self, vmin, vmax):
        self.vmax = vmax
        self.vmin = vmin
        if self.is_video_loaded:
            self.set_frame(self.current_frame)

    @Slot()
    def set_remove_background(self, checked):
        self.remove_background = checked
        if self.is_video_loaded:
            self.set_frame(self.current_frame)

    @Slot()
    def set_time(self, time):
        index = np.abs(self.video.time - time).argmin()
        self.set_frame(index)

    @Slot()
    def set_frame(self, index):
        if index != self.current_frame:
            try:
                if index >= 0 and index < self.video.header.nFrames:
                    self.commands.set_all(index, self.video.time[index])
                    if self.remove_background:
                        temp = self.video[index] - self.video[0]
                    else:
                        temp = self.video[index]
                    if self.transpose:
                        temp = temp[::self.reverseX, ::self.reverseY].T
                    else:
                        temp = temp[::self.reverseX, ::self.reverseY]
                    temp[temp < 0] = 0
                    temp[temp >= 0x7FFF] = 0x7FFF - 1
                    self.image.set_data(temp)
                    self.axes.set_xlim(0, temp.shape[1] - 1)
                    self.axes.set_ylim(0, temp.shape[0] - 1)
                    # try:
                    #     hist = histogram(65535)
                    #     hist.add(temp.astype(np.uint32).ravel().tolist())
                    #     vmin = hist.get_percentile(self.vmin)
                    #     vmax = hist.get_percentile(self.vmax)
                    #     del hist
                    #     self.image.set_clim(vmin, vmax)
                    # except Exception as Error:
                    #     print(Error)
                    #     self.image.autoscale()
                    self.vmin = temp.min()
                    self.vmax = temp.max()
                    self.image.set(clim=(self.vmin,
                                         self.vmax))  # till histogram
                    self.current_frame = index
                    try:
                        y, x = self.movement(self.video.time[index])
                        self.line.move(-x, -y)  # TO-DO: check if - necessary
                        self.Parent.m_editMenuSaveLineProfile.Enable(
                            self.line.isValid)
                    except Exception:
                        self.Parent.m_editMenuSaveLineProfile.Enable(False)
                    self.canvas.draw()
            except Exception as Error:
                print(Error)

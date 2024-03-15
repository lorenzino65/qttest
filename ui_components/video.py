import numpy as np

import matplotlib
from matplotlib.backend_bases import FigureCanvas
from matplotlib.figure import Figure
from matplotlib import cm
from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
)
import ir
import testVideo
import JadeIII
import IRCam
import IRCam2
import Sektor7Unten
import Sektor7Oben
import Sektor9Tauchrohr
import Sektor9Zeile
import IRLab
from video_commands import VideoCommands
from line import Line

matplotlib.use('qtagg')


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
        for tick in self.axes.get_xticklabels():
            tick.set_visible(False)
        for tick in self.axes.get_yticklabels():
            tick.set_visible(False)
        self.axes.set_xlim(0, 511)
        self.axes.set_ylim(0, 511)
        self.axes.set_aspect(1)

        self.cmap = cm.gray
        self.reverseX = 1
        self.reverseY = 1
        self.transpose = False
        self.removeBackground = False

        self.currentFrame = 0
        self.canvas.draw()

        # Layout
        # self.addWidget(self.title,)
        self.addWidget(self.canvas, 90)
        self.commands = VideoCommands()
        self.addLayout(self.commands, 7)

        # Signals
        self.commands.updateFrame.connect(self.setFrame)
        self.commands.updateTime.connect(self.setTime)  # Still dont know

    def get_video(camera, experiment_number):
        videos = {
            'Jade III': JadeIII.video,
            'IRCam': IRCam.video,
            'Test Video': testVideo.video,
            'IRCam2': IRCam2.video,
            'Sektor 7 Unten': Sektor7Unten.video,
            'Sektor 9 Tauchrohr': Sektor9Tauchrohr.video,
            'Sektor 9 Zeile': Sektor9Zeile.video,
            'Sektor 7 Oben': Sektor7Oben.video,
            'IRLab': IRLab.video,
        }
        return videos[camera](experiment_number)

    def get_movement(camera, experiment_number):
        movement = {
            'Jade III': lambda i: ir.movement(),  #JadeIII.movement,
            'IRCam': IRCam.movement,
            'Test Video': lambda i: ir.movement(),
            'IRCam2': lambda i: ir.movement(),
            'Sektor 7 Unten': Sektor7Unten.movement,
            'Sektor 9 Tauchrohr': Sektor9Tauchrohr.movement,
            'Sektor 9 Zeile': Sektor9Zeile.movement,
            'Sektor 7 Oben': Sektor7Oben.movement,
            'IRLab': lambda i: ir.movement()
        }
        return movement[camera](experiment_number)

    def get_movement_now(self):
        return self.movement(self.video.time[self.currentFrame])

    @Slot()
    def open_video(self, camera, experiment_number):
        self.setVideo(self.get_video(),
                      self.get_movement(),
                      name=self.getName())
        self.video = self.get_video(camera, experiment_number)
        self.movement = self.get_movement(camera, experiment_number)
        self.name = camera

        self.commands.setRange(0, self.video.header.nFrames - 1)
        self.commands.reset()
        self.setFrame(0)

    @Slot()
    def add_line(self):
        self.remove_line()
        line, = self.axes.plot([0], [0], 'r')
        self.line = Line(self, line)

    def setGamma(self, gamma):
        self.cmap.set_gamma(gamma)
        self.image.autoscale()
        self.canvas.draw()

    def getGamma(self):
        return float(self.cmap._gamma)

    def setRemoveBackground(self, state):
        self.removeBackground = state
        self.setFrame(self.currentFrame)

    def setColorMap(self, cmap):
        cmap.set_gamma(self.getGamma())
        self.cmap = cmap
        self.image.set_cmap(self.cmap)
        self.canvas.draw()

    @Slot()
    def setTime(self, time):
        index = np.abs(self.video.time - time).argmin()
        self.setFrame(index)

    @Slot()
    def setFrame(self, index):
        if index != self.currentFrame:
            try:
                if index >= 0 and index < self.video.header.nFrames:
                    self.commands.setAll(index)
                    if self.removeBackground:
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
                    self.image.autoscale()
                    self.currentFrame = index
                    self.m_currentTime.Value = '%f' % self.video.time[index]
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

    def setAutoScale(self, value):
        self.autoScale = value
        if self.autoScale:
            self.image.autoscale()

    def OnScroll(self, event):
        self.setFrame(self.slider.GetValue())

    def set_cmap(self, cmap):
        self.image.set_cmap(cmap)
        self.canvas.draw()

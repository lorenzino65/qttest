class Line(object):

    def __init__(self, parent, line):
        self.parent = parent
        self.line = line
        self.xs = [0]
        self.ys = [0]
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)
        self.start = True

    def __del__(self):
        self.line.remove()

    def __call__(self, event):
        print("click", event)
        if event.inaxes != self.line.axes or len(self.xs) == 2: return
        x_mov, y_mov = self.parent.get_movement_now()
        if self.start:
            self.start = False
            self.xs = [event.xdata - x_mov]
            self.ys = [event.ydata - y_mov]
        else:
            self.xs.append(event.xdata - x_mov)
            self.ys.append(event.ydata - y_mov)
        self.line.set_data(self.xs + x_mov, self.ys + y_mov)
        self.line.figure.canvas.draw()
        if len(self.xs) == 2:
            self.line.figure.canvas.mpl_disconnect(self.cid)

    def move(self, x, y):
        self.line.set_data(self.xs + x, self.ys + y)

    @property
    def isValid(self):
        return len(self.xs) == 2 and len(self.ys) == 2

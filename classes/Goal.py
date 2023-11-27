from cmu_graphics import *
from .BB import BB


class Goal:
    def __init__(self, app, x, y):
        self.app = app
        self.x = x
        self.y = y
        self.BB = BB(app, x, -1000, 100, 2000)
        self.debug = True

    def draw(self):
        x = self.x - self.app.camera.getOffset()
        drawRect(x, self.y, 100, 100, fill="gainsboro")
        drawRect(x + 40, self.y - 500, 20, 500, fill="dimGray")
        drawPolygon(x + 60, 300, x + 260, 350, x + 60, 400, fill="crimson")

        if self.debug:
            self.BB.draw()

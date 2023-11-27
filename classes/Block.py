from cmu_graphics import *
from .BB import BB


class Block:
    def __init__(self, app, x, y, width=100, height=100, fill="gray"):
        self.app = app
        self.debug = False

        self.width = width
        self.height = height
        self.x = x
        self.y = y

        self.fill = fill

        # boundary boxes
        self.BB = BB(self.app, x, y, width, height)
        self.topBB = BB(self.app, x, y, width, height / 2)
        self.rightBB = BB(self.app, x + width / 2, y, width / 2, height)
        self.bottomBB = BB(self.app, x, y + height / 2, width, height / 2)
        self.leftBB = BB(self.app, x, y, width / 2, height)

    def draw(self):
        drawRect(
            self.x - self.app.camera.getOffset(),
            self.y,
            self.width,
            self.height,
            fill=self.fill,
            border="black",
            borderWidth=4,
        )

        if self.debug:
            self.topBB.draw()
            self.rightBB.draw()
            self.bottomBB.draw()
            self.leftBB.draw()

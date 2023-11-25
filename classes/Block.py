from cmu_graphics import *
from .BB import BB


class Block:
    def __init__(self, app, x, y, width=100, height=100):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.debug = False

        # boundary boxes
        self.BB = BB(app, x, y, width, height)
        self.topBB = BB(app, x, y, width, height / 2)
        self.rightBB = BB(app, x + width / 2, y, width / 2, height)
        self.bottomBB = BB(app, x, y + height / 2, width, height / 2)
        self.leftBB = BB(app, x, y, width / 2, height)

    def draw(self):
        drawRect(
            self.x - app.camera.getOffset(),
            self.y,
            self.width,
            self.height,
            fill="gray",
            border="black",
            borderWidth=4,
        )

        if self.debug:
            self.topBB.draw()
            self.rightBB.draw()
            self.bottomBB.draw()
            self.leftBB.draw()

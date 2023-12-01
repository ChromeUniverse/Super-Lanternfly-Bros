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

        self.BB = BB(self.app, x, y, width, height)

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
            # main hitbox
            self.BB.draw()

            # vertical centerline
            x = (
                self.BB.getLeft() + self.BB.getRight()
            ) / 2 - self.app.camera.getOffset()
            drawLine(x, self.BB.getBottom(), x, self.BB.getTop(), fill="red")

            # horizontal centerline
            y = (self.BB.getBottom() + self.BB.getTop()) / 2
            drawLine(
                self.BB.getLeft() - self.app.camera.getOffset(),
                y,
                self.BB.getRight() - self.app.camera.getOffset(),
                y,
                fill="red",
            )

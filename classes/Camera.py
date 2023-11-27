from cmu_graphics import *
from .BB import BB


class Camera(BB):
    def __init__(self, app, x, y, width, height):
        super().__init__(app, x, y, width, height)
        self.debug = True

    def getOffset(self):
        offset = self.x - 700
        return offset

    def draw(self):
        if not self.debug:
            return
        drawRect(
            self.x - self.getOffset(),
            self.y,
            self.width,
            self.height,
            fill=None,
            border="red",
        )
        drawLabel(
            f"{self.x}",
            self.x + self.width / 2 - self.getOffset(),
            self.y + 20,
            size=20,
            fill="red",
        )

    def step(self):
        levelWidth = len(self.app.level[0]) * 100

        # dragging to the left
        if self.app.player.BB.getLeft() < self.getLeft() and self.getLeft() > 700:
            self.x = self.app.player.x

        # dragging to the right
        if (
            self.app.player.BB.getRight() > self.getRight()
            and self.getRight() < levelWidth - 1000
        ):
            self.x = self.app.player.BB.getRight() - self.width

from cmu_graphics import *
from .BB import BB


class Coin(BB):
    def __init__(self, app, x, y):
        super().__init__(app, x + 25, y, 50, 100)
        self.debug = True
        self.collected = False

    def draw(self):
        centerX, centerY = (
            self.x + self.width / 2 - self.app.camera.getOffset(),
            self.y + self.height / 2,
        )

        if not self.collected:
            drawOval(centerX, centerY, 60, 90, fill="orange")
            ratio = 0.7
            drawOval(centerX, centerY, 60 * ratio, 90 * ratio, fill="yellow")
            drawRect(centerX, centerY, 10, 30, fill="orange", align="center")

        if self.debug:
            drawRect(
                self.x - self.app.camera.getOffset(),
                self.y,
                self.width,
                self.height,
                fill=None,
                border="red",
            )

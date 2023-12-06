from cmu_graphics import *
from classes.Animation import Animation

from helpers.misc import playAnimation
from .BB import BB


class Coin(BB):
    def __init__(self, app, x, y):
        super().__init__(app, x + 25, y, 50, 100)

        self.debug = False
        self.collected = False
        self.animation = Animation(
            app, self.x, self.y, "assets/coin-1.gif", loop=True, delay=4
        )

    def draw(self):
        centerX, centerY = (
            self.x + self.width / 2 - self.app.camera.getOffset(),
            self.y + self.height / 2,
        )

        if not self.collected:
            pass
            self.animation.draw()

        if self.debug:
            drawRect(
                self.x - self.app.camera.getOffset(),
                self.y,
                self.width,
                self.height,
                fill=None,
                border="red",
            )

    def step(self):
        centerX, centerY = (
            self.x + self.width / 2,
            self.y + self.height / 2,
        )

        self.animation.step()
        self.animation.x, self.animation.y = centerX, centerY

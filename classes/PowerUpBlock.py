from .Block import Block
from cmu_graphics import *


class PowerUpBlock(Block):
    def __init__(self, x, y, width=100, height=100):
        super().__init__(x, y, width, height)
        self.hit = False

    def getHit(self):
        return self.hit

    def setHit(self, hit):
        self.hit = hit

    def draw(self):
        fill = "brown" if self.hit else "yellow"
        drawRect(
            self.x - app.camera.getOffset(),
            self.y,
            self.width,
            self.height,
            fill=fill,
            border="orange",
            borderWidth=4,
        )
        if self.debug:
            self.topBB.draw()
            self.rightBB.draw()
            self.bottomBB.draw()
            self.leftBB.draw()

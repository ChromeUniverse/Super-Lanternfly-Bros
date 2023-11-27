from .Block import Block
from cmu_graphics import *


class PowerUpBlock(Block):
    def __init__(self, app, x, y, width=100, height=100, type=0):
        super().__init__(app, x, y, width, height)
        self.type = type
        self.hitCount = 0

        # type 0: single coin
        # type 1: 5 coins
        # type 2: bug spray
        # type 3: flamethrower
        if type == 0 or type == 2 or type == 3:
            self.maxHitCount = 1
        elif type == 1:
            self.maxHitCount = 5

    def hit(self):
        if self.hitCount == self.maxHitCount:
            return
        self.hitCount += 1

        # type 0: single coin
        # type 1: 5 coins
        # type 2: bug spray
        # type 3: flamethrower
        if self.type == 0 or self.type == 1:
            self.app.score += 100
        elif self.type == 2:
            # TODO: equip bug spray
            pass
        elif self.type == 3:
            # TODO: equip flamethrower
            pass

    def draw(self):
        fill = "brown" if self.hitCount == self.maxHitCount else "yellow"
        drawRect(
            self.x - app.camera.getOffset(),
            self.y,
            self.width,
            self.height,
            fill=fill,
            border="orange",
            borderWidth=4,
        )
        centerX, centerY = (
            self.x - self.app.camera.getOffset() + self.width / 2,
            self.y + self.height / 2,
        )

        if self.hitCount != self.maxHitCount:
            drawLabel(
                self.maxHitCount - self.hitCount,
                centerX,
                centerY,
                size=36,
                font="monospace",
            )
        if self.debug:
            self.topBB.draw()
            self.rightBB.draw()
            self.bottomBB.draw()
            self.leftBB.draw()

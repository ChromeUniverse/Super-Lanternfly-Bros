from .Block import Block
from .PowerUps import PowerUpPickUp
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
        # type 4: meal block
        # type 5: health potion
        if type == 1:
            self.maxHitCount = 5
        else:
            self.maxHitCount = 1

    def hit(self):
        if self.hitCount == self.maxHitCount:
            return
        self.hitCount += 1

        # type 0: single coin
        # type 1: 5 coins
        # type 2: bug spray
        # type 3: flamethrower
        # type 4: meal block
        # type 5: health potion
        if self.type == 0 or self.type == 1:
            self.app.score += 100
        elif self.type == 2:
            self.app.powerUpPickUps.append(
                PowerUpPickUp(self.app, self.x, self.y - 100, type=0)
            )
        elif self.type == 3:
            self.app.powerUpPickUps.append(
                PowerUpPickUp(self.app, self.x, self.y - 100, type=1)
            )
        elif self.type == 4:
            self.app.powerUpPickUps.append(
                PowerUpPickUp(self.app, self.x, self.y - 100, type=2)
            )
        elif self.type == 5:
            self.app.powerUpPickUps.append(
                PowerUpPickUp(self.app, self.x, self.y - 100, type=3)
            )

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
            # type 0: single coin
            # type 1: 5 coins
            if self.type == 0 or self.type == 1:
                drawLabel(
                    self.maxHitCount - self.hitCount,
                    centerX,
                    centerY,
                    size=36,
                    font="monosp`ace",
                )
            # type 2: bug spray
            elif self.type == 2:
                drawCircle(centerX, centerY, 20, fill="purple")
            # type 3: flamethrower
            elif self.type == 3:
                drawCircle(centerX, centerY, 30, fill="orange")
            # type 4: meal block
            elif self.type == 4:
                drawCircle(centerX, centerY, 30, fill="blue")
            # type 4: health potion
            elif self.type == 5:
                drawCircle(centerX, centerY, 30, fill="lightGreen")

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

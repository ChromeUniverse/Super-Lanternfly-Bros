from cmu_graphics import *
from .BB import BB
from .Block import Block


class Lanternfly:
    def __init__(self, app, x, y):
        self.app = app
        self.debug = True

        self.x = x
        self.y = y
        self.prevX = x
        self.prevY = y
        self.dx = -5
        self.dy = 0

        self.width = 100
        self.height = 100

        self.BB = BB(app, self.x, self.y, self.width, self.height)
        self.prevBB = BB(app, self.prevX, self.prevY, self.width, self.height)

        self.topBB = BB(self.app, x, y, self.width, self.height / 2)
        self.rightBB = BB(self.app, x + self.width / 2, y, self.width / 2, self.height)
        self.bottomBB = BB(
            self.app, x, y + self.height / 2, self.width, self.height / 2
        )
        self.leftBB = BB(self.app, x, y, self.width / 2, self.height)

        self.dead = False

    def draw(self):
        fill = "blue" if not self.dead else "red"

        drawRect(
            self.x - self.app.camera.getOffset(),
            self.y,
            self.width,
            self.height,
            fill=fill,
        )

        if self.debug:
            self.topBB.draw()
            self.rightBB.draw()
            self.bottomBB.draw()
            self.leftBB.draw()

        if self.debug:
            drawRect(
                self.x - self.app.camera.getOffset(),
                self.y,
                self.width,
                self.height,
                fill=None,
                border="red",
                borderWidth=4,
            )
            drawLabel(
                f"{self.x}, {self.y}",
                self.x + 50 - self.app.camera.getOffset(),
                self.y - 20,
                size=28,
            )

    def updateBB(self):
        self.BB = BB(app, self.x, self.y, self.width, self.height)
        self.topBB = BB(self.app, self.x, self.y, self.width, self.height / 2)
        self.rightBB = BB(
            self.app, self.x + self.width / 2, self.y, self.width / 2, self.height
        )
        self.bottomBB = BB(
            self.app, self.x, self.y + self.height / 2, self.width, self.height / 2
        )
        self.leftBB = BB(self.app, self.x, self.y, self.width / 2, self.height)

    def step(self):
        if self.dead:
            return

        # update position and velocities
        self.x += self.dx
        self.y += self.dy
        self.dy += 3
        self.updateBB()

        # Collisions against blocks

        # CITATION:
        # Collision detection and handling algorithms inspireds by Chris Marriott's
        # web-based recreation of Super Mario Bros, written in JavaScript.
        #
        # GitHub: https://github.com/algorithm0r/SuperMarioBros

        for i in range(len(self.app.blocks)):
            block: Block = self.app.blocks[i]

            if self.BB.isColliding(block.BB):
                # horizontal collision
                if self.BB.isColliding(block.topBB) and self.BB.isColliding(
                    block.bottomBB
                ):
                    if self.BB.isColliding(block.leftBB):
                        self.x = block.BB.getLeft() - 100
                        self.updateBB()
                        # print(f"left col. with block {i}", self.app.counter)
                    elif self.BB.isColliding(block.rightBB):
                        self.x = block.BB.getRight()
                        self.updateBB()
                        # print(f"right col. with block {i}", self.app.counter)

                    self.dx = -self.dx

                # hit block from above
                if self.dy > 0 and self.prevBB.getBottom() <= block.BB.getTop():
                    self.y = block.BB.getTop() - 100
                    self.dy = 0
                    self.updateBB()
                    # print(f"top col. with block {i}", self.app.counter)

        self.prevX, self.prevY = self.x, self.y
        self.prevBB = self.BB

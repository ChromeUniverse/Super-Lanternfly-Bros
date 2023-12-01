from cmu_graphics import *
from .BB import BB
from .Block import Block


class Lanternfly:
    def __init__(self, app, x, y):
        self.app = app
        self.debug = False
        self.points = 100

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

    def step(self):
        if self.dead:
            return

        # update position and velocities
        self.x += self.dx
        self.y += self.dy
        self.dy += 3
        self.updateBB()

        # Collisions against blocks

        for i in range(len(self.app.blocks)):
            block: Block = self.app.blocks[i]

            if self.BB.isColliding(block.BB):
                # vertical collisions (above only)
                if self.dy > 0 and self.prevBB.getBottom() <= block.BB.getTop():
                    self.y = block.BB.getTop() - 100
                    self.dy = 0
                    self.updateBB()

                # horizontal collisons
                # checks if block's horizontal centerline is inside player's vertical edges
                if (
                    self.BB.getTop()
                    < (block.BB.getBottom() + block.BB.getTop()) / 2
                    < self.BB.getBottom()
                ):
                    # left
                    if self.BB.getLeft() < block.BB.getLeft() < self.BB.getRight():
                        self.x = block.BB.getLeft() - 100
                        self.updateBB()
                    # right
                    elif self.BB.getLeft() < block.BB.getRight() < self.BB.getRight():
                        self.x = block.BB.getRight()
                        self.updateBB()
                    self.dx = -self.dx

        self.prevX, self.prevY = self.x, self.y
        self.prevBB = self.BB

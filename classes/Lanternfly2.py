from cmu_graphics import *
from .BB import BB
from .Block import Block


class Lanternfly2:
    def __init__(self, app, x, y):
        self.app = app
        self.debug = False
        self.points = 300

        self.x = x + 10
        self.y = y + 10
        self.initialY = self.y
        self.prevX = x
        self.prevY = y
        self.dx = 0
        self.dy = 0

        self.width = 80
        self.height = 80

        # bounding boxes
        self.BB = BB(app, self.x, self.y, self.width, self.height)
        self.prevBB = BB(app, self.prevX, self.prevY, self.width, self.height)

        self.dead = False

        # add launcher block
        launcher = Block(app, x, y, fill="darkSlateGray")
        self.launcher = launcher
        self.app.blocks.append(launcher)

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
        self.dy += 1
        self.updateBB()

        # jump preiodically if player isn't over launcher
        if self.app.counter % 60 == 1 and (
            self.app.player.BB.getRight() < self.launcher.BB.getLeft()
            or self.app.player.BB.getLeft() > self.launcher.BB.getRight()
        ):
            self.dy = -25

        # check for floor boundary
        if self.y > self.initialY:
            self.y = self.initialY - 1
            self.dy = 0

        self.prevX, self.prevY = self.x, self.y
        self.prevBB = self.BB

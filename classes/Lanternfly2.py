from cmu_graphics import *
from .BB import BB
from .Block import Block


class Lanternfly2:
    def __init__(self, app, x, y):
        self.app = app
        self.debug = False

        self.x = x + 10
        self.y = y + 10
        self.initialY = self.y
        self.prevX = x
        self.prevY = y
        self.dx = 0
        self.dy = 0

        self.width = 80
        self.height = 80

        # primary bounding boxes
        self.BB = BB(app, self.x, self.y, self.width, self.height)
        self.prevBB = BB(app, self.prevX, self.prevY, self.width, self.height)

        # secondary bounding boxes
        self.topBB = BB(self.app, x, y, self.width, self.height / 2)
        self.rightBB = BB(self.app, x + self.width / 2, y, self.width / 2, self.height)
        self.bottomBB = BB(
            self.app, x, y + self.height / 2, self.width, self.height / 2
        )
        self.leftBB = BB(self.app, x, y, self.width / 2, self.height)

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

        # for i in range(len(self.app.blocks)):
        #     block: Block = self.app.blocks[i]

        #     if self.BB.isColliding(block.BB):
        #         # hit block from above
        #         if self.dy > 0 and self.prevBB.getBottom() <= block.BB.getTop():
        #             self.y = block.BB.getTop() - self.height
        #             self.dy = 0
        #             self.updateBB()
        #             print(f"top col. with block {i}", self.app.counter)

        #         # horizontal collision
        #         if self.BB.isColliding(block.topBB) and self.BB.isColliding(
        #             block.bottomBB
        #         ):
        #             if self.BB.isColliding(block.leftBB):
        #                 self.x = block.BB.getLeft() - self.width
        #                 self.updateBB()
        #                 print(f"left col. with block {i}", self.app.counter)
        #             elif self.BB.isColliding(block.rightBB):
        #                 self.x = block.BB.getRight()
        #                 self.updateBB()
        #                 print(f"right col. with block {i}", self.app.counter)

        #             self.dx = -self.dx

        self.prevX, self.prevY = self.x, self.y
        self.prevBB = self.BB

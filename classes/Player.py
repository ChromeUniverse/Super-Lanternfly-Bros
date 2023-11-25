from cmu_graphics import *

from classes.Block import Block
from .PowerUpBlock import PowerUpBlock
from .BB import BB


class Player:
    def __init__(self, app):
        self.app = app
        self.debug = True

        self.x = 0
        self.y = 500
        self.prevX = 0
        self.prevY = 500
        self.dx = 0
        self.dy = 0

        self.width = 100
        self.height = 100
        self.BB = BB(app, self.x, self.y, self.width, self.height)

        self.onGround = True

    def draw(self):
        drawRect(self.x - self.app.camera.getOffset(), self.y, self.width, self.height)
        drawLabel(
            f"{self.x}, {self.y}",
            self.x + 50 - self.app.camera.getOffset(),
            self.y - 20,
            size=28,
        )

    # position getters/setters
    def getPos(self):
        return self.x, self.y

    def setPos(self, x, y):
        self.x, self.y = x, y

    # position setter methods: right, left, jump
    def moveRight(self):
        self.dx = 20

    def moveLeft(self):
        self.dx = -20

    def stop(self):
        self.dx = 0

    def jump(self):
        if not self.onGround:
            return
        self.dy = -50
        self.onGround = False

    # boundary box getters
    def getTop(self):
        return self.y

    def getLeft(self):
        return self.x

    def getBottom(self):
        return self.y + self.height

    def getRight(self):
        return self.x + self.width

    def getPrevTop(self):
        return self.prevY

    def getPrevLeft(self):
        return self.prevX

    def getPrevBottom(self):
        return self.prevY + self.height

    def getPrevRight(self):
        return self.prevX + self.width

    # ...
    def updateOnGround(self):
        # check for floor boundary
        if self.y >= self.app.height - self.height:
            self.onGround = True
            return

        for block in self.app.blocks:
            if (
                self.BB.isColliding(block.BB)
                and self.dy > 0
                and self.getPrevBottom() <= block.BB.getTop()
            ):
                self.onGround = True
                return

        self.onGround = False

    def step(self):
        # update position and velocities
        self.x += self.dx
        self.y += self.dy
        self.dy += 3
        self.BB = BB(app, self.x, self.y, self.width, self.height)

        # check for floor boundary
        if self.y > self.app.height - self.height:
            self.y = self.app.height - self.height

        self.updateOnGround()
        for i in range(len(self.app.blocks)):
            block: Block = self.app.blocks[i]

            if self.BB.isColliding(block.BB):
                # hit block from above
                if self.dy > 0 and self.getPrevBottom() <= block.BB.getTop():
                    self.y = block.BB.getTop() - 100
                    self.dy = 0

                # hit block from below
                if self.dy < 0 and self.getPrevTop() >= block.BB.getBottom():
                    # colliding with both Left and Right BBs -> push downwards
                    if self.BB.isColliding(block.leftBB) and self.BB.isColliding(
                        block.rightBB
                    ):
                        print(f"top col. with block {i}", self.app.counter)
                        self.dy = 0
                        self.y = block.BB.getBottom()
                        if isinstance(block, PowerUpBlock):
                            block.setHit(not block.getHit())

                # horizontal collision
                if self.BB.isColliding(block.topBB) and self.BB.isColliding(
                    block.bottomBB
                ):
                    if self.BB.isColliding(block.leftBB):
                        self.x = block.BB.getLeft() - 100
                        print(f"left col. with block {i}", self.app.counter)
                    elif self.BB.isColliding(block.rightBB):
                        self.x = block.BB.getRight()

        self.prevX, self.prevY = self.x, self.y

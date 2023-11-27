from cmu_graphics import *
import time

from .BB import BB
from .Block import Block
from .PowerUpBlock import PowerUpBlock
from .Lanternfly import Lanternfly
from .Lanternfly2 import Lanternfly2


class Player:
    def __init__(self, app):
        self.app = app
        self.debug = True

        self.x = 0
        self.y = 200
        self.prevX = 0
        self.prevY = 500
        self.dx = 0
        self.dy = 0

        self.width = 100
        self.height = 100
        self.BB = BB(app, self.x, self.y, self.width, self.height)
        self.prevBB = BB(app, self.prevX, self.prevY, self.width, self.height)

        self.onGround = True
        self.HP = 100
        self.maxHP = 100
        self.name = "Lucca"

    def draw(self):
        fill = "red" if self.HP == 0 else "black"

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

    # ...
    def updateOnGround(self):
        # check if player top-colliding with any blocks
        for block in self.app.blocks:
            if (
                self.BB.isColliding(block.BB)
                and self.dy > 0
                and self.prevBB.getBottom() <= block.BB.getTop()
            ):
                self.onGround = True
                return

        self.onGround = False

    def updateBB(self):
        self.BB = BB(app, self.x, self.y, self.width, self.height)

    def step(self):
        if self.HP == 0:
            return

        # update position and velocities
        self.x += self.dx
        self.y += self.dy
        self.dy += 3
        self.BB = BB(app, self.x, self.y, self.width, self.height)

        # check for floor boundary
        if self.y > self.app.height - self.height:
            # self.y = self.app.height - self.height
            self.HP = 0
            return

        self.updateOnGround()

        # End goal
        if not self.app.gameOver and self.BB.getRight() > self.app.goal.BB.getRight():
            self.app.gameOver = True
            self.x = self.app.goal.BB.getLeft()
            self.dx = 0
            self.app.endTime = time.time()
            return

        # Collisions against blocks

        # CITATION:
        # Collision detection and handling algorithms inspireds by Chris Marriott's
        # web-based recreation of Super Mario Bros, written in JavaScript.
        #
        # GitHub: https://github.com/algorithm0r/SuperMarioBros

        for i in range(len(self.app.blocks)):
            block: Block = self.app.blocks[i]

            if self.BB.isColliding(block.BB):
                # hit block from above
                if self.dy > 0 and self.prevBB.getBottom() <= block.BB.getTop():
                    self.y = block.BB.getTop() - 100
                    self.dy = 0
                    self.updateBB()
                    # print(f"top col. with block {i}", self.app.counter)

                # hit block from below
                if self.dy < 0 and self.prevBB.getTop() >= block.BB.getBottom():
                    # colliding with both Left and Right BBs -> push downwards
                    if self.BB.isColliding(block.leftBB) and self.BB.isColliding(
                        block.rightBB
                    ):
                        # print(f"bottom col. with block {i}", self.app.counter)
                        self.dy = 0
                        self.y = block.BB.getBottom()
                        if isinstance(block, PowerUpBlock):
                            block.hit()
                        self.updateBB()

                # horizontal collision
                if self.BB.isColliding(block.topBB) and self.BB.isColliding(
                    block.bottomBB
                ):
                    if self.BB.isColliding(block.leftBB):
                        self.x = block.BB.getLeft() - 100
                        # print(f"left col. with block {i}", self.app.counter)
                    elif self.BB.isColliding(block.rightBB):
                        self.x = block.BB.getRight()
                        # print(f"right col. with block {i}", self.app.counter)
                    self.updateBB()

        # Enemies

        for i in range(len(self.app.enemies)):
            enemy: Lanterfly = self.app.enemies[i]

            if enemy.dead:
                continue

            if self.BB.isColliding(enemy.BB):
                # horizontal collision
                if self.BB.isColliding(enemy.topBB) and self.BB.isColliding(
                    enemy.bottomBB
                ):
                    self.HP = 0
                    print(f"horizontal col. with enemy {i}", self.app.counter)
                    continue

                # vertical collision (colliding with both Left and Right BBs)
                if self.BB.isColliding(enemy.leftBB) and self.BB.isColliding(
                    enemy.rightBB
                ):
                    # hit enemy from above -> push downwards
                    relativeDy = self.dy - enemy.dy
                    # if relativeDy > 0 and self.prevBB.getBottom() <= enemy.BB.getTop():
                    if relativeDy > 0:
                        self.y = enemy.BB.getTop() - 100
                        self.dy = -50
                        enemy.dead = True

                        if isinstance(enemy, Lanternfly):
                            self.app.score += 100
                        elif isinstance(enemy, Lanternfly2):
                            self.app.score += 300

                        print(f"top col. with enemy {i}", self.app.counter)
                        continue

                    # hit enemy from below
                    if relativeDy < 0 and self.prevBB.getTop() >= enemy.BB.getBottom():
                        self.HP = 0
                        print(f"bottom col. with enemy {i}", self.app.counter)
                        continue

        # Coins

        for i in range(len(self.app.coins)):
            coin = self.app.coins[i]
            if not coin.collected and self.BB.isColliding(coin):
                print(f"collided with coin {i}")
                coin.collected = True
                self.app.score += 100

        self.prevX, self.prevY = self.x, self.y
        self.prevBB = self.BB

        # testing out the HP bar
        # self.HP = self.app.counter % 100

from cmu_graphics import *
import math
import time

from .BB import BB
from .Block import Block
from .PowerUpBlock import PowerUpBlock
from .Lanternfly import Lanternfly
from .Lanternfly2 import Lanternfly2
from .Lanternfly3 import Lanternfly3
from .PowerUps import PowerUp


class Player:
    def __init__(self, app):
        self.app = app
        self.debug = False
        self.name = "Lucca"

        # physical properties
        self.width = 100
        self.height = 100
        self.x = 0
        self.y = 200
        self.prevX = 0
        self.prevY = 500
        self.dx = 0
        self.dy = 0
        self.direction = 1
        self.onGround = True

        # current and previous bounding boxes
        self.BB = BB(app, self.x, self.y, self.width, self.height)
        self.prevBB = BB(app, self.prevX, self.prevY, self.width, self.height)

        # health statistics: HP and hunger
        self.HP = 100
        self.maxHP = 100
        self.hunger = 100
        self.maxHunger = 100

        # enemy hit cooldown
        self.cooldown = False
        self.cooldownStartTime = None
        self.cooldownDuration = 2

    def draw(self):
        fill = "red" if self.HP == 0 else "black"

        # oscillating opacity to represent enemy hit cooldown
        if self.cooldown:
            opacity = 50 + math.sin(self.app.counter % 10) * 50
        else:
            opacity = 100

        drawRect(
            self.x - self.app.camera.getOffset(),
            self.y,
            self.width,
            self.height,
            fill=fill,
            opacity=opacity,
        )

        # player direction indicator
        labelX, labelY = self.x + 50 - self.app.camera.getOffset(), self.y + 50
        if self.direction == 1:
            drawLabel(">", labelX, labelY, fill="white", size=36)
        elif self.direction == 0:
            drawLabel("<", labelX, labelY, fill="white", size=36)

        # hitbox debugging
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

    def takeDamage(self, oneHitKill=False):
        if not self.cooldown:
            if oneHitKill:
                self.HP = 0
            else:
                self.HP -= 34
            self.cooldown = True
            self.cooldownStartTime = time.time()

    def step(self):
        # update position and velocities
        self.x += self.dx
        self.y += self.dy

        if not self.onGround:
            self.dy += 3

        self.updateBB()

        # fell in a hole!
        if self.y > self.app.height:
            self.app.gameOver = True
            self.app.win = False
            return

        # check if player is on the ground
        self.updateOnGround()

        # update hunger
        if not app.gameOver:
            self.hunger = max(self.hunger - 0.1, 0)
            if self.hunger == 0:
                self.HP -= 0.1

        # update HP
        if self.HP <= 0:
            self.app.gameOver = True
            self.app.win = False

        # update enemy hit cooldown

        if (
            self.cooldown
            and time.time() > self.cooldownStartTime + self.cooldownDuration
        ):
            self.cooldown = False
            self.cooldownStartTime = None

        # End goal

        if not self.app.gameOver and self.BB.getRight() > self.app.goal.BB.getRight():
            self.app.gameOver = True
            self.app.win = True

            self.x = self.app.goal.BB.getLeft()
            self.dx = 0
            self.app.endTime = time.time()
            millisLeft = (app.timeLimit - time.time()) * 1000 // 1
            app.score += millisLeft
            return

        # Collision detection + handling against blocks

        for i in range(len(self.app.blocks)):
            block: Block = self.app.blocks[i]

            if self.BB.isColliding(block.BB):
                # vertical collisions
                # above
                if self.dy > 0 and self.prevBB.getBottom() <= block.BB.getTop():
                    self.y = block.BB.getTop() - 100
                    self.dy = 0
                    self.updateBB()
                # below
                # checks if block's vertical centerline is inside player's horizontal edges
                if (
                    self.dy < 0
                    and self.prevBB.getTop() >= block.BB.getBottom()
                    and (
                        self.BB.getLeft()
                        <= (block.BB.getLeft() + block.BB.getRight()) / 2
                        <= self.BB.getRight()
                    )
                ):
                    self.y = block.BB.getBottom()
                    self.dy = 0
                    # print(f"bottom collision with block {i}")
                    if isinstance(block, PowerUpBlock):
                        block.hit()
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
                        self.dx = 0
                        # print(f"left collision with block {i}", app.counter)
                        self.updateBB()
                    # right
                    elif self.BB.getLeft() < block.BB.getRight() < self.BB.getRight():
                        self.x = block.BB.getRight()
                        self.dx = 0
                        # print(f"right collision with block {i}", app.counter)
                        self.updateBB()

        # Enemies

        for i in range(len(self.app.enemies)):
            enemy: Lanternfly = self.app.enemies[i]

            if enemy.dead:
                continue

            if enemy.BB == None:
                if isinstance(enemy, Lanternfly3):
                    for ball in enemy.balls:
                        if ball.isColliding(self.BB):
                            self.takeDamage()

            if enemy.BB != None and self.BB.isColliding(enemy.BB):
                # colliding from above, stomp on enemy
                if self.prevBB.getBottom() < enemy.prevBB.getTop():
                    self.dy = -50
                    enemy.dead = True
                    self.app.score += enemy.points
                    # print(f"stomp'd enemy {i}", self.app.counter)
                # take damage, trigger cooldown
                else:
                    self.takeDamage()

        # Coins

        for i in range(len(self.app.coins)):
            coin = self.app.coins[i]
            if not coin.collected and self.BB.isColliding(coin):
                # print(f"collided with coin {i}")
                coin.collected = True
                self.app.score += 100

        # Power-up pickups

        pickUps = self.app.powerUpPickUps
        i = 0
        while i < len(pickUps):
            pickUp = pickUps[i]
            if self.BB.isColliding(pickUp):
                # print("collided with pickup", pickUp.type)

                if pickUp.type == 0 or pickUp.type == 1:
                    self.app.powerUp = PowerUp(self.app, pickUp.type)
                elif pickUp.type == 2:
                    self.hunger = min(self.hunger + 20, self.maxHunger)
                elif pickUp.type == 3:
                    self.HP = min(self.HP + 34, self.maxHP)

                self.app.score += 50
                pickUps.pop(i)
            else:
                i += 1

        self.prevX, self.prevY = self.x, self.y
        self.prevBB = self.BB

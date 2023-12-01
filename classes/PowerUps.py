from cmu_graphics import *
import math
from .BB import BB


class PowerUpPickUp(BB):
    def __init__(self, app, x, y, type):
        super().__init__(app, x, y, 100, 100)
        self.type = type
        self.debug = False

    def draw(self):
        # types:
        # 0: bug spray
        # 1: flamethrower
        # 2: meal block
        # 3: health potion
        if self.type == 0:
            fill = "purple"
        elif self.type == 1:
            fill = "orange"
        elif self.type == 2:
            fill = "blue"
        elif self.type == 3:
            fill = "lightGreen"

        drawRect(
            self.x + 10 - self.app.camera.getOffset(),
            self.y + 10,
            80,
            80,
            fill=fill,
        )


class PowerUp:
    def __init__(self, app, type):
        self.app = app
        self.type = type

        self.v = 100
        self.maxV = 100
        self.dV = None
        self.bbWidth = None
        self.bbHeight = None
        self.label = None

        # types:
        # 0: bug spray
        if type == 0:
            self.dV = 2
            self.bbWidth = 100
            self.bbHeight = 100
            self.label = "Bug spray"
        # 1: flamethrower
        elif type == 1:
            self.dV = 2
            self.bbWidth = 300
            self.bbHeight = 100
            self.label = "Flamethrower"

        self.BB = None
        if app.player.direction == 1:
            self.BB = BB(
                app, app.player.BB.getRight(), app.player.y, self.bbWidth, self.bbHeight
            )
        elif app.player.direction == 0:
            self.BB = BB(
                app,
                app.player.BB.getLeft() - self.bbWidth,
                app.player.y,
                self.bbWidth,
                self.bbHeight,
            )

    def draw(self):
        # types:
        # 0: bug spray
        # 1: flamethrower
        fill = None
        if self.type == 0:
            fill = "purple"
        elif self.type == 1:
            fill = "orange"

        # oscillating opacity
        opacity = 50 + math.sin(self.app.counter % 10) * 50

        if self.app.player.direction == 1:
            drawRect(
                self.app.player.BB.getRight() - self.app.camera.getOffset(),
                self.app.player.y,
                self.bbWidth,
                self.bbHeight,
                fill=fill,
                opacity=opacity,
            )

        elif self.app.player.direction == 0:
            drawRect(
                self.app.player.BB.getLeft()
                - self.bbWidth
                - self.app.camera.getOffset(),
                self.app.player.y,
                self.bbWidth,
                self.bbHeight,
                fill=fill,
                opacity=opacity,
            )

    def step(self):
        # consumes a bit of volume very step
        self.v -= self.dV

        # determine which direction the player is facing, update BB
        if self.app.player.direction == 1:
            self.BB = BB(
                self.app,
                self.app.player.BB.getRight(),
                self.app.player.y,
                self.bbWidth,
                self.bbHeight,
            )
        elif self.app.player.direction == 0:
            self.BB = BB(
                self.app,
                self.app.player.BB.getLeft() - self.bbWidth,
                self.app.player.y,
                self.bbWidth,
                self.bbHeight,
            )

        # check collisions against enemies -> kills enemies
        for i in range(len(self.app.enemies)):
            enemy = self.app.enemies[i]
            if enemy.BB != None and self.BB.isColliding(enemy.BB) and not enemy.dead:
                enemy.dead = True
                self.app.score += enemy.points

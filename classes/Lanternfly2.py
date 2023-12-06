from cmu_graphics import *
import math
from .BB import BB
from .Block import Block


class Lanternfly2:
    def __init__(self, app, x, y):
        self.app = app
        self.debug = False
        self.points = 300

        self.x = x
        self.y = y
        self.initialY = self.y
        self.prevX = x
        self.prevY = y
        self.dx = 0
        self.dy = 0

        self.width = 100
        self.height = 100

        # bounding boxes
        self.BB = BB(app, self.x, self.y, self.width, self.height)
        self.prevBB = BB(app, self.prevX, self.prevY, self.width, self.height)

        self.dead = False

        # add launcher block
        launcher = Block(app, x, y, fill="darkSlateGray")
        self.launcher = launcher
        self.app.blocks.append(launcher)

    def draw(self):
        if self.dead:
            return

        # drawRect(
        #     self.x - self.app.camera.getOffset(),
        #     self.y,
        #     self.width,
        #     self.height,
        #     fill="blue",
        # )

        centerX, centerY = self.x - self.app.camera.getOffset() + 50, self.y + 50

        if self.dead:
            return

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

        if self.y >= self.initialY - 10:
            return

        # body
        drawOval(
            centerX,
            centerY,
            40,
            80,
            fill="slateGray",
        )

        if self.dy < 0:
            drawOval(
                centerX - 15,
                centerY + 20,
                40,
                30,
                fill="red",
                border="black",
                borderWidth=3,
                rotateAngle=90,
            )

            drawOval(
                centerX + 15,
                centerY + 20,
                40,
                30,
                fill="red",
                border="black",
                borderWidth=3,
                rotateAngle=80,
            )

            pivotX, pivotY = (centerX - 15, centerY - 15)
            width, height = 70, 30
            angle = -90 - 30 * (1 + math.sin(app.counter * 1))

            drawOval(
                pivotX + (width / 2) * math.cos(angle * math.pi / 180),
                pivotY - (width / 2) * math.sin(angle * math.pi / 180),
                width,
                height,
                fill="black",
                border="beige",
                borderWidth=1,
                rotateAngle=-angle,
            )

            pivotX, pivotY = (centerX + 15, centerY - 15)
            width, height = 70, 30
            angle = -90 + 30 * (1 + math.sin(app.counter * 1))

            drawOval(
                pivotX + (width / 2) * math.cos(angle * math.pi / 180),
                pivotY - (width / 2) * math.sin(angle * math.pi / 180),
                width,
                height,
                fill="black",
                border="beige",
                borderWidth=1,
                rotateAngle=-angle,
            )

        else:
            drawOval(
                centerX - 15,
                centerY - 20,
                40,
                30,
                fill="red",
                border="black",
                borderWidth=3,
                rotateAngle=80,
            )

            drawOval(
                centerX + 15,
                centerY - 20,
                40,
                30,
                fill="red",
                border="black",
                borderWidth=3,
                rotateAngle=90,
            )

            pivotX, pivotY = (centerX - 15, centerY + 15)
            width, height = 70, 30
            angle = 90 + 30 * (1 + math.sin(app.counter * 1))

            drawOval(
                pivotX + (width / 2) * math.cos(angle * math.pi / 180),
                pivotY - (width / 2) * math.sin(angle * math.pi / 180),
                width,
                height,
                fill="black",
                border="beige",
                borderWidth=1,
                rotateAngle=-angle,
            )

            pivotX, pivotY = (centerX + 15, centerY + 15)
            width, height = 70, 30
            angle = 90 - 30 * (1 + math.sin(app.counter * 1))

            drawOval(
                pivotX + (width / 2) * math.cos(angle * math.pi / 180),
                pivotY - (width / 2) * math.sin(angle * math.pi / 180),
                width,
                height,
                fill="black",
                border="beige",
                borderWidth=1,
                rotateAngle=-angle,
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
        if self.y > self.initialY + 10:
            self.y = self.initialY + 9
            self.dy = 0

        self.prevX, self.prevY = self.x, self.y
        self.prevBB = self.BB

from cmu_graphics import *
import math

from .BB import BB
from .BC import BC
from .Block import Block


class Ball(BC):
    def __init__(self, app, x, y, r):
        super().__init__(app, x, y, r)

    def draw(self):
        drawCircle(
            self.x - self.app.camera.getOffset(),
            self.y,
            self.r,
            fill="orange",
        )


class Lanternfly3:
    def __init__(self, app, x, y):
        self.app = app
        self.debug = False
        self.dead = False

        self.x = x + 50
        self.y = y + 50
        self.angle = 0

        self.radiusStep = 50
        self.radiusOffset = 10
        self.numBalls = 4
        self.ballRadius = 20

        self.balls = [
            Ball(
                app,
                self.x + (self.radiusOffset + self.radiusStep * (i + 1)),
                y,
                self.ballRadius,
            )
            for i in range(self.numBalls)
        ]
        self.BB = None

    def draw(self):
        drawCircle(
            self.x - self.app.camera.getOffset(),
            self.y,
            15,
            fill="gray",
            border="black",
            borderWidth=4,
        )

        for ball in self.balls:
            ball.draw()

    def step(self):
        # update position and velocities
        self.angle += 0.10
        for i in range(len(self.balls)):
            ball = self.balls[i]
            radius = self.radiusOffset + self.radiusStep * (i + 1)
            ball.x = self.x + radius * math.sin(self.angle)
            ball.y = self.y + radius * math.cos(self.angle)

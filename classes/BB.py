from cmu_graphics import *


class BB:
    def __init__(self, app, x, y, width, height):
        self.app = app
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.height

    def draw(self):
        drawRect(
            self.x - self.app.camera.getOffset(),
            self.y,
            self.width,
            self.height,
            fill=None,
            border="red",
        )

    # edge getters
    def getTop(self):
        return self.y

    def getLeft(self):
        return self.x

    def getBottom(self):
        return self.y + self.height

    def getRight(self):
        return self.x + self.width

    # position update setter
    def update(self, x, y):
        self.x = x
        self.y = y

    def isColliding(self, other):
        return (
            self.getRight() > other.getLeft()
            and self.getLeft() < other.getRight()
            and self.getBottom() > other.getTop()
            and self.getTop() < other.getBottom()
        )

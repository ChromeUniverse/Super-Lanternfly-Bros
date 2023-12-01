from cmu_graphics import *


class BC:
    def __init__(self, app, x, y, r):
        self.app = app
        self.x = x
        self.y = y
        self.r = r

    def draw(self):
        drawCircle(
            self.x - self.app.camera.getOffset(),
            self.y,
            self.r,
            fill=None,
            border="red",
        )

    def isColliding(self, other):
        # assumes "self" is a BC (bounding circle), "other" is a BB (bounding box)

        closestX = None
        closestY = None

        # circle to the left of rectangle
        if self.x < other.getLeft():
            closestX = other.getLeft()
        # circle to the right of rectangle
        elif self.x > other.getRight():
            closestX = other.getRight()
        # circle in between horizontal edges
        else:
            closestX = self.x

        # circle above rectangle
        if self.y < other.getTop():
            closestY = other.getTop()
        # circle below rectangle
        elif self.y > other.getBottom():
            closestY = other.getBottom()
        # circle in between vertical edges
        else:
            closestY = self.y

        deltaX = self.x - closestX
        deltaY = self.y - closestY
        dist = (deltaX**2 + deltaY**2) ** 0.5

        return dist < self.r

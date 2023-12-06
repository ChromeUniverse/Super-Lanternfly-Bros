from cmu_graphics import *
from PIL import Image


class Animation:
    def __init__(
        self, app, x, y, filePath, playCount=1, loop=False, delay=1, sizeX=80, sizeY=80
    ):
        self.app = app
        self.x = x
        self.y = y
        self.finished = False
        self.loop = loop
        self.delay = delay
        self.debug = False
        self.sizeX = sizeX
        self.sizeY = sizeY

        # load explosion gif
        myGif = Image.open(filePath)

        self.spriteList = []
        self.spriteCounter = 0

        for _ in range(playCount):
            for frame in range(myGif.n_frames):
                # Set the current frame
                myGif.seek(frame)
                # Resize the image
                # fr = myGif.resize((myGif.size[0] * 3 // 4, myGif.size[1] * 3 // 4))
                fr = myGif.resize((self.sizeX, self.sizeY))
                # Convert to CMUImage
                fr = CMUImage(fr)
                # Put in our sprite list
                self.spriteList.append(fr)

        self.spriteList.pop(0)

    def draw(self):
        drawImage(
            self.spriteList[self.spriteCounter],
            self.x - app.camera.getOffset(),
            self.y - 5,
            align="center",
        )

        if self.debug:
            drawLabel(
                f"{self.spriteCounter} of {len(self.spriteList)}, {self.loop}",
                self.x,
                self.y,
                size=50,
            )

    def step(self):
        if self.finished:
            return

        if self.app.counter % self.delay == 0:
            if self.spriteCounter == len(self.spriteList) - 1:
                if self.loop:
                    self.spriteCounter = 0
                else:
                    self.finished = True
            else:
                self.spriteCounter += 1

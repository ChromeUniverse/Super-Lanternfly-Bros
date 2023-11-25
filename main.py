from cmu_graphics import *
from classes.Player import Player
from classes.Block import Block
from classes.PowerUpBlock import PowerUpBlock
from classes.BB import BB
from classes.Camera import Camera
import csv


def loadLevel():
    levelFileName = "levels/1.csv"
    levelData = []
    with open(levelFileName, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            levelData.append([int(block) for block in row])
    return levelData


def onAppStart(app):
    app.counter = 0
    app.blocks = []

    # initialize camera
    app.camera = Camera(app, 700, 0, 300, app.height)

    # load level
    level = loadLevel()
    app.level = level
    for i in range(len(level)):
        row = level[i]
        for j in range(len(row)):
            if level[i][j] == 1:
                app.blocks.append(Block(app, j * 100, i * 100))
            elif level[i][j] == 2:
                app.blocks.append(PowerUpBlock(app, j * 100, i * 100))

    # initialize player
    app.player = Player(app)

    # game framerate
    # app.stepsPerSecond = 5


def onKeyHold(app, keys):
    if "right" in keys:
        app.player.moveRight()
    if "left" in keys:
        app.player.moveLeft()
    if "up" in keys:
        app.player.jump()


def onKeyRelease(app, key):
    if key == "right" or key == "left":
        app.player.stop()


def redrawAll(app):
    app.player.draw()
    for block in app.blocks:
        block.draw()
    app.camera.draw()


def takeStep(app):
    app.counter += 1
    app.player.step()
    app.camera.step()


def onStep(app):
    takeStep(app)


def main():
    runApp(width=2000, height=1000)


if __name__ == "__main__":
    main()

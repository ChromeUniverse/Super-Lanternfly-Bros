from cmu_graphics import *

from classes.Player import Player
from classes.Block import Block
from classes.PowerUpBlock import PowerUpBlock
from classes.BB import BB
from classes.Camera import Camera
from classes.Lanternfly import Lanternfly
from classes.Coin import Coin
from classes.Lanternfly2 import Lanternfly2
from classes.Goal import Goal

import csv
import time


def drawUI(app):
    font = "monospace"

    # Player name & healthbar
    hpBarWidth = 350
    drawLabel(app.player.name, 100, 50, size=36, align="left", font=font, bold=True)
    drawLabel("HP", 100, 100, size=36, align="left", font=font)
    drawRect(160, 82, hpBarWidth, 35, fill="red")
    if app.player.HP > 0:
        drawRect(
            160,
            82,
            (hpBarWidth * app.player.HP / app.player.maxHP),
            35,
            fill="lightGreen",
        )

    # Score
    drawLabel("Score", 700, 50, size=36, align="left", font=font, opacity=50)
    drawLabel(app.score, 700, 100, size=36, align="left", font=font, bold=True)

    # Level indicator
    drawLabel("Level", 1000, 50, size=36, align="left", font=font, opacity=50)
    drawLabel(0, 1000, 100, size=36, align="left", font=font, bold=True)

    # Time left
    drawLabel("Time", 1300, 50, size=36, align="left", font=font, opacity=50)
    elapsed = time.time() if app.endTime == None else app.endTime
    drawLabel(
        (elapsed - app.startTime) * 1000 // 1,
        1300,
        100,
        size=36,
        align="left",
        font=font,
        bold=True,
    )


def loadLevel():
    levelFileName = "levels/1.csv"
    levelData = []
    with open(levelFileName, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            levelData.append(row)
    return levelData


def onAppStart(app):
    app.score = 0
    app.gameOver = False

    # initialize timing
    app.counter = 0
    app.startTime = time.time()
    app.endTime = None

    # entities
    app.blocks = []
    app.enemies = []
    app.coins = []
    app.goal = None

    # initialize camera
    app.camera = Camera(app, 700, 0, 300, app.height)

    # load level
    level = loadLevel()
    app.level = level
    for i in range(len(level)):
        row = level[i]
        for j in range(len(row)):
            x, y = j * 100, i * 100
            cell = level[i][j]
            if cell == "1":
                app.blocks.append(Block(app, x, y))
            elif cell == "2":
                app.blocks.append(PowerUpBlock(app, x, y))
            elif cell == "3":
                app.enemies.append(Lanternfly(app, x, y))
            elif cell == "4":
                app.coins.append(Coin(app, x, y))
            elif cell == "5":
                app.blocks.append(PowerUpBlock(app, x, y, type=1))
            elif cell == "6":
                app.enemies.append(Lanternfly2(app, x, y))
            elif cell == "7":
                app.goal = Goal(app, x, y)

    # initialize player
    app.player = Player(app)

    # game framerate
    # app.stepsPerSecond = 10


def onKeyHold(app, keys):
    if app.gameOver:
        return

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
    for enemy in app.enemies:
        enemy.draw()

    for block in app.blocks:
        block.draw()

    for coin in app.coins:
        coin.draw()

    app.goal.draw()
    app.camera.draw()

    app.player.draw()
    drawUI(app)


def takeStep(app):
    app.counter += 1
    app.player.step()
    app.camera.step()

    for enemy in app.enemies:
        enemy.step()


def onStep(app):
    takeStep(app)


def main():
    runApp(width=2000, height=1000)


if __name__ == "__main__":
    main()

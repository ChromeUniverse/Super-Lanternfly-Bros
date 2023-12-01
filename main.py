from cmu_graphics import *
import time

from classes.Player import Player
from classes.PowerUps import PowerUp
from classes.Camera import Camera

from helpers.drawUI import drawUI
from helpers.levels import loadHardCodedLevel, loadRandomLevel


def reset(app, randomLevel=False):
    app.score = 0
    app.gameOver = False
    app.win = False

    # initialize timing
    app.counter = 0
    app.startTime = time.time()
    app.timeLimit = app.startTime + 60
    app.endTime = None

    # entities
    app.blocks = []
    app.enemies = []
    app.coins = []
    app.powerUpPickUps = []
    app.goal = None

    # load level
    if randomLevel:
        app.levelWidth = loadRandomLevel(app)
    else:
        app.levelWidth = loadHardCodedLevel(app)

    # initialize camera
    app.camera = Camera(app, 700, 0, 300, app.height)

    # initialize player
    app.player = Player(app)

    # powerUps!
    app.powerUp = None
    # app.powerUp = PowerUp(app, 1)
    app.powerUpTrigger = False


def onAppStart(app):
    reset(app)
    # game framerate
    # app.stepsPerSecond = 10


def onKeyPress(app, key):
    if key == "1":
        reset(app, randomLevel=False)
    if key == "2":
        reset(app, randomLevel=True)


def onKeyHold(app, keys):
    if app.gameOver or app.player.HP <= 0:
        return

    if "right" in keys:
        app.player.moveRight()
        app.player.direction = 1
    if "left" in keys:
        app.player.moveLeft()
        app.player.direction = 0
    if "up" in keys:
        app.player.jump()
    if "z" in keys:
        app.powerUpTrigger = True


def onKeyRelease(app, key):
    if key == "right" or key == "left":
        app.player.stop()
    if key == "z":
        app.powerUpTrigger = False


def redrawAll(app):
    for enemy in app.enemies:
        enemy.draw()

    for block in app.blocks:
        block.draw()

    for coin in app.coins:
        coin.draw()

    for pickUp in app.powerUpPickUps:
        pickUp.draw()

    app.goal.draw()
    app.camera.draw()

    app.player.draw()
    if app.powerUp != None and app.powerUpTrigger:
        app.powerUp.draw()

    drawUI(app)


def takeStep(app):
    app.counter += 1
    app.player.step()
    app.camera.step()

    timeLeft = app.timeLimit - time.time()
    if timeLeft < 0 and not app.gameOver:
        app.gameOver = True
        app.win = False

    for enemy in app.enemies:
        enemy.step()

    if app.powerUp != None and app.powerUpTrigger:
        app.powerUp.step()
        if app.powerUp.v <= 0:
            app.powerUp = None


def onStep(app):
    takeStep(app)


def main():
    runApp(width=2000, height=1000)


if __name__ == "__main__":
    main()

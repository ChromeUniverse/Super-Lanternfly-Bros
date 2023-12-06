from cmu_graphics import *
import time

from classes.Player import Player
from classes.PowerUps import PowerUp
from classes.Camera import Camera

from helpers.drawUI import drawUI
from helpers.levels import loadHardCodedLevel, loadRandomLevel1, loadRandomLevel2
from PIL import Image


def reset(app, levelType):
    app.score = 0
    app.gameOver = False
    app.win = False

    # initialize timing
    app.counter = 0
    app.startTime = time.time()
    app.timeLimit = app.startTime + 60
    app.endTime = None

    # entities
    app.animations = []
    app.blocks = []
    app.enemies = []
    app.coins = []
    app.powerUpPickUps = []
    app.goal = None

    # load level
    if levelType == 1:
        app.levelWidth = loadHardCodedLevel(app)
    elif levelType == 2:
        app.levelWidth = loadRandomLevel1(app)
    elif levelType == 3:
        app.levelWidth = loadRandomLevel2(app)

    # initialize camera
    app.camera = Camera(app, 700, 0, 300, app.height)

    # initialize player
    app.player = Player(app)

    # powerUps!
    app.powerUp = None
    app.powerUp = PowerUp(app, 1)
    app.powerUpTrigger = False


def onAppStart(app):
    app.levelsCleared = 0
    reset(app, levelType=1)
    # game framerate
    # app.stepsPerSecond = 10

    app.image = Image.open("assets/pitt-1.jpg")
    app.image = app.image.resize((2000, 1000))
    app.image = CMUImage(app.image)


def onKeyPress(app, key):
    # hardcoded level
    if key == "1":
        reset(app, levelType=1)
    # random level (pre-built chunks)
    if key == "2":
        reset(app, levelType=2)
    # random level (generation logic and pathfinding)
    if key == "3":
        reset(app, levelType=3)
    # instakill
    if key == "k":
        app.player.HP = 0


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
    # background image
    drawImage(app.image, app.width / 2, app.height / 2, align="center")
    drawRect(0, 0, app.width, app.height, fill="lightCyan", opacity=50)

    for enemy in app.enemies:
        enemy.draw()

    for block in app.blocks:
        block.draw()

    for coin in app.coins:
        coin.draw()

    for pickUp in app.powerUpPickUps:
        pickUp.draw()

    for animation in app.animations:
        animation.draw()

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

    for coin in app.coins:
        coin.step()

    for enemy in app.enemies:
        enemy.step()

    if app.powerUp != None and app.powerUpTrigger:
        app.powerUp.step()
        if app.powerUp.v <= 0:
            app.powerUp = None

    for a in app.animations:
        a.step()
    app.animations = [a for a in app.animations if not a.finished]


def onStep(app):
    takeStep(app)


def main():
    runApp(width=2000, height=1000)


if __name__ == "__main__":
    main()

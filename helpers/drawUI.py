from cmu_graphics import *
from PIL import Image
import time


def onAppStart(app):
    # Open image from local directory
    app.image = Image.open("images/Caaaaat.jpg")
    app.image = app.image.resize((400, 400))

    # Cast image type to CMUImage to allow for faster drawing
    app.image = CMUImage(app.image)
    app.angle = 0


def onStep(app):
    app.angle += 5


def redrawAll(app):
    # drawPILImage takes in a PIL image object and the left-top coordinates
    drawImage(
        app.image, app.width / 2, app.height / 2, align="center", rotateAngle=app.angle
    )


def drawUI(app):
    font = "monospace"

    # Healthbar
    barWidth = 350
    drawLabel(
        "HP",
        100,
        50,
        size=36,
        align="left",
        font=font,
        bold=True,
        fill="white",
        border="black",
        borderWidth=1,
    )
    drawRect(100, 82, barWidth, 35, fill="red")
    if app.player.HP > 0:
        drawRect(
            100,
            82,
            (barWidth * app.player.HP / app.player.maxHP),
            35,
            fill="lightGreen",
        )

    # Hunger bar
    drawLabel(
        "Hunger",
        100,
        160,
        size=36,
        align="left",
        font=font,
        bold=True,
        fill="white",
        border="black",
        borderWidth=1,
    )
    drawRect(100, 192, barWidth, 35, fill="red")
    if app.player.hunger > 0:
        drawRect(
            100,
            192,
            (barWidth * app.player.hunger / app.player.maxHunger),
            35,
            fill="blue",
        )

    # Power-up, if equipped
    if app.powerUp != None:
        drawLabel(
            app.powerUp.label,
            100,
            270,
            size=36,
            align="left",
            font=font,
            bold=True,
            fill="white",
            border="black",
            borderWidth=1,
        )
        drawRect(100, 302, barWidth, 35, fill="red")
        if app.powerUp.v > 0:
            drawRect(
                100,
                302,
                (barWidth * app.powerUp.v / app.powerUp.maxV),
                35,
                fill="lightGreen",
            )

    # Score
    drawLabel(
        "Score",
        700,
        50,
        size=36,
        align="left",
        font=font,
        bold=True,
        fill="white",
        border="black",
        borderWidth=1,
    )
    drawLabel(app.score, 700, 100, size=36, align="left", font=font, bold=True)

    # Level indicator
    drawLabel(
        "Level",
        1000,
        50,
        size=36,
        align="left",
        font=font,
        bold=True,
        fill="white",
        border="black",
        borderWidth=1,
    )
    drawLabel(app.levelsCleared, 1000, 100, size=36, align="left", font=font, bold=True)

    # Time left
    drawLabel(
        "Time",
        1300,
        50,
        size=36,
        align="left",
        font=font,
        bold=True,
        fill="white",
        border="black",
        borderWidth=1,
    )
    # elapsed = time.time() if app.endTime == None else app.endTime
    timeLeft = (
        0
        if (app.gameOver or app.player.HP == 0)
        else max(app.timeLimit - time.time(), 0)
    )
    drawLabel(
        (timeLeft) * 1000 // 1,
        1300,
        100,
        size=36,
        align="left",
        font=font,
        bold=True,
    )

    # Endgame modal
    if app.gameOver:
        endgameLabel = "You win!!!" if app.win else "You lose!"

        drawRect(0, 0, app.width, app.height, fill="black", opacity=60)
        drawLabel(
            endgameLabel,
            app.width / 2,
            app.height / 2,
            size=200,
            fill="white",
            border="black",
            borderWidth=4,
            bold=True,
        )
        drawLabel(
            "Press '1' to load a hardcoded level",
            app.width / 2,
            app.height / 2 + 150,
            size=40,
            fill="white",
            border="black",
            borderWidth=2,
            bold=True,
        )
        drawLabel(
            "Press '2' to load a random level (pre-built chunks)",
            app.width / 2,
            app.height / 2 + 200,
            size=40,
            fill="white",
            border="black",
            borderWidth=2,
            bold=True,
        )
        drawLabel(
            "Press '3' to load a random level (complex logic)",
            app.width / 2,
            app.height / 2 + 250,
            size=40,
            fill="white",
            border="black",
            borderWidth=2,
            bold=True,
        )

from cmu_graphics import *
import time


def drawUI(app):
    font = "monospace"

    # Player name & healthbar
    barWidth = 350
    drawLabel(app.player.name, 100, 50, size=36, align="left", font=font, bold=True)
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
    drawLabel("Score", 700, 50, size=36, align="left", font=font, opacity=50)
    drawLabel(app.score, 700, 100, size=36, align="left", font=font, bold=True)

    # Level indicator
    drawLabel("Level", 1000, 50, size=36, align="left", font=font, opacity=50)
    drawLabel(0, 1000, 100, size=36, align="left", font=font, bold=True)

    # Time left
    drawLabel("Time", 1300, 50, size=36, align="left", font=font, opacity=50)
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
            size=50,
            fill="white",
            border="black",
            borderWidth=2,
            bold=True,
        )
        drawLabel(
            "Press '2' to load a randomly-generated level",
            app.width / 2,
            app.height / 2 + 220,
            size=50,
            fill="white",
            border="black",
            borderWidth=2,
            bold=True,
        )

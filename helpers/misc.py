from classes.Animation import Animation


def prettyPrint(grid):
    for row in grid:
        print(row)


def playAnimation(app, x, y, filePath, sizeX=100, sizeY=100, playCount=1, delay=1):
    app.animations.append(
        Animation(
            app,
            x,
            y,
            filePath,
            playCount=playCount,
            delay=delay,
            sizeX=sizeX,
            sizeY=sizeY,
        )
    )

import csv
from io import StringIO
import random

from classes.Block import Block
from classes.PowerUpBlock import PowerUpBlock
from classes.BB import BB
from classes.Lanternfly import Lanternfly
from classes.Coin import Coin
from classes.Lanternfly2 import Lanternfly2
from classes.Goal import Goal
from classes.Lanternfly3 import Lanternfly3

from helpers.pathfinding import *
from helpers.misc import prettyPrint


startChunk = """.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.
1,1,1,1,1,1,1,1
"""

chunk1 = """.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.
.,.,.,.,1,1,1,1
"""

chunk2 = """.,.,.,.,.
.,.,.,.,.
.,.,.,.,.
.,.,.,.,.
.,.,.,.,.
.,.,.,.,.
.,.,%,.,.
.,.,.,.,.
.,.,.,.,.
1,1,1,1,1
"""

chunk3 = """.,.,.,.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.,.,.,.
.,.,.,.,.,%,.,.,.,.,.
.,.,.,.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.,.,.,.
.,.,.,1,%,1,%,1,.,.,.
.,.,.,.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.,.,.,.
.,.,.,.,.,!,.,.,.,.,.
1,1,1,1,1,1,1,1,1,1,1
"""

chunk4 = """.,.,.,.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.,.,.,.,.,.,.
.,.,.,1,%,1,%,1,.,.,.,.,.,.
.,.,.,.,.,.,.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.,.,.,.,.,.,.
1,1,1,1,1,1,1,1,1,1,1,1,1,1
"""

chunk5 = """.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.
.,8,.,.,.,8,.,.
.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.
1,1,1,1,1,1,1,1
"""

chunk6 = """.,.,.,.,.,.,.
.,.,.,.,.,.,.
.,.,.,.,.,.,.
.,.,.,8,.,.,.
.,.,.,.,.,.,.
.,.,.,.,.,.,.
1,.,.,.,.,.,1
1,.,.,.,.,.,1
1,.,3,.,3,.,1
1,1,1,1,1,1,1
"""

chunk7 = """.,.,.,.,.,.,.
.,.,.,.,.,.,.
.,.,.,.,.,.,.
.,.,.,8,.,.,.
.,.,.,.,.,.,.
.,.,.,.,.,.,.
1,.,.,.,.,.,1
1,.,.,.,.,.,1
1,.,6,.,6,.,1
1,1,1,1,1,1,1
"""

chunk7 = """.,.,.,.,.,.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.,.,.,.,.,.
.,.,8,.,.,.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,1,.,.,.,.,.
.,.,.,.,.,.,1,1,.,.,.,.,.
.,.,.,.,.,1,1,1,.,.,.,.,.
.,.,.,.,1,1,1,1,.,.,.,.,.
.,.,.,1,1,1,1,1,.,.,.,.,.
1,1,1,1,1,1,1,1,.,.,.,.,.
"""

chunk8 = """.,.,.,.,.,.,.
.,.,.,.,.,.,.
.,.,.,%,.,.,.
.,.,.,.,.,.,.
.,.,.,.,.,.,.
.,.,.,.,.,.,.
.,.,6,1,6,.,.
.,1,1,1,1,1,.
1,1,1,1,1,1,1
1,1,1,1,1,1,1
"""

endChunk = """.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.
.,.,.,.,.,.,.,.
7,.,.,.,.,.,.,.
1,1,1,1,1,1,1,1
"""

chunksCollection = [
    chunk1,
    chunk2,
    chunk3,
    chunk4,
    chunk5,
    chunk6,
    chunk7,
    chunk8,
]


def loadHardCodedLevel(app):
    levelFileName = "levels/1.csv"

    level = []

    with open(levelFileName, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            level.append(row)

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
            elif cell == "8":
                app.enemies.append(Lanternfly3(app, x, y))
            elif cell == "9":
                app.blocks.append(PowerUpBlock(app, x, y, type=2))
            elif cell == "0":
                app.blocks.append(PowerUpBlock(app, x, y, type=3))
            elif cell == "#":
                app.blocks.append(PowerUpBlock(app, x, y, type=4))
            elif cell == "+":
                app.blocks.append(PowerUpBlock(app, x, y, type=5))

    levelWidth = len(level[0]) * 100
    return levelWidth


def loadRandomLevel1(app):
    randomChunks = []
    for _ in range(random.randint(6, 10)):
        i = random.randint(0, len(chunksCollection) - 1)
        randomChunks.append(chunksCollection[i])

    chunks = [startChunk] + randomChunks + [endChunk]

    levelWidth = 0

    for chunkIndex in range(len(chunks)):
        chunk = chunks[chunkIndex]
        f = StringIO(chunk)

        chunkWidth = len(chunk.split("\n")[0].split(",")) * 100

        level = []
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            level.append(row)

        for i in range(len(level)):
            row = level[i]
            for j in range(len(row)):
                x, y = (j * 100) + levelWidth, i * 100
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
                elif cell == "8":
                    app.enemies.append(Lanternfly3(app, x, y))
                elif cell == "9":
                    app.blocks.append(PowerUpBlock(app, x, y, type=2))
                elif cell == "0":
                    app.blocks.append(PowerUpBlock(app, x, y, type=3))
                elif cell == "#":
                    app.blocks.append(PowerUpBlock(app, x, y, type=4))
                elif cell == "+":
                    app.blocks.append(PowerUpBlock(app, x, y, type=5))

                # spawns in random power-up
                elif cell == "%":
                    type = random.randint(0, 5)
                    app.blocks.append(PowerUpBlock(app, x, y, type=type))

                # spawns in random enemy
                elif cell == "!":
                    type = random.randint(1, 3)
                    if type == 1:
                        app.enemies.append(Lanternfly(app, x, y))
                    elif type == 2:
                        app.enemies.append(Lanternfly2(app, x, y))
                    elif type == 3:
                        app.enemies.append(Lanternfly3(app, x, y))

        levelWidth += chunkWidth

    return levelWidth


def checkAllNeighborsClear(level, cell):
    allNeighbors = getAllNeighbors(cell)
    for neighbor in allNeighbors:
        if isFilled(level, neighbor):
            return False
    return True


# fill level's side edges
def fillEdges(level, rows, cols):
    level[0] = ["1" for _ in range(len(level[0]))]
    level[rows - 1] = ["1" for _ in range(len(level[0]))]
    for i in range(rows):
        level[i][0] = "1"
        level[i][cols - 1] = "1"


# add random static blocks
def placeBlocks(level, rows, cols):
    placed = 0
    iterations = 0

    # NOTE: a block fill density of .15=15% strikes a nice balance between
    # not feeling too empty and ensuring there is at least one solution for
    # placing other entities (power-ups, enemies) given their spawn rules
    # for a certain arrangement of blocks
    while placed < 0.15 * rows * cols:
        row, col = random.randint(1, rows - 2), random.randint(1, cols - 2)

        # don't spawn in start or end points
        if (row, col) == (1, 1) or (row, col) == (rows - 2, cols - 2):
            continue

        # only place block if cell isn't already filled
        if not isFilled(level, (row, col)):
            level[row][col] = "1"
            placed += 1

        iterations += 1
    print(f"Placed blocks after {iterations} iterations")


# add random power-ups blocks (checks for top and cottom clearance)
def placePowerUps(level, rows, cols):
    placed = 0
    iterations = 0
    while placed < 0.01 * rows * cols:
        row, col = random.randint(1, rows - 2), random.randint(1, cols - 2)

        # don't spawn in start or end points
        if (row, col) == (1, 1) or (row, col) == (rows - 2, cols - 2):
            continue

        # spawn rules:
        # 1. all neighbors must be clear
        # 2. blocks above and below must be empty
        if (
            checkAllNeighborsClear(level, (row, col))
            and not isFilled(level, (row, col))
            and not isFilled(level, (row + 1, col))
            and not isFilled(level, (row - 1, col))
        ):
            level[row][col] = "%"
            placed += 1

        iterations += 1
    print(f"Placed power-ups after {iterations} iterations")


# add random enemies
def placeEnemies(level, rows, cols):
    placed = 0
    iterations = 0
    while placed < 0.01 * rows * cols:
        row, col = random.randint(1, rows - 2), random.randint(1, cols - 2)

        # don't spawn in start or end points
        if (row, col) == (1, 1) or (row, col) == (rows - 2, cols - 2):
            continue

        type = random.randint(1, 3)

        # lanternfly 1 (goomba-like enemy)
        if type == 1:
            # spawn rules:
            # 1. bottom is filled
            # 2. enemy can move laterally and doesn't spawn in a ahole
            if (
                isFilled(level, (row + 1, col))
                and not isFilled(level, (row, col + 1))
                and isFilled(level, (row, col - 1))
            ):
                level[row][col] = "3"
                placed += 1

        # lanternfly 2 (cannon shooter)
        elif type == 2:
            # spawn rules:
            # 1. block below launcher block must be filled
            # 2. at least 4 blocks above the launcher block aren't filled
            if (
                isFilled(level, (row + 1, col))
                and not isFilled(level, (row - 1, col))
                and not isFilled(level, (row - 2, col))
                and not isFilled(level, (row - 3, col))
                and not isFilled(level, (row - 4, col))
            ):
                level[row][col] = "6"
                placed += 1

        # lanternfly 2 (spinny enemy)
        elif type == 3:
            # spawn rules:
            # 1. ensure that all neighbors are free
            if checkAllNeighborsClear(level, (row, col)):
                level[row][col] = "8"
                placed += 1

        iterations += 1

    print(f"Placed enemies after {iterations} iterations")


# generates a random level with more complex generaion rules
def generateRandomLevel():
    rows, cols = 10, random.randint(30, 60)

    # start with empty level and end goal
    level = [["." for _ in range(cols)] for _ in range(10)]
    level[rows - 2][cols - 2] = "7"

    print("-----")
    fillEdges(level, rows, cols)
    placeBlocks(level, rows, cols)
    placePowerUps(level, rows, cols)
    placeEnemies(level, rows, cols)

    return level


def loadRandomLevel2(app):
    iterations = 0

    while True:
        candidate = generateRandomLevel()
        iterations += 1
        if isValidPath(candidate, (1, 1), (8, 18)):
            level = candidate
            print(f"Generation successful after {iterations} pathfinding attempts")
            break

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
            elif cell == "8":
                app.enemies.append(Lanternfly3(app, x, y))
            elif cell == "9":
                app.blocks.append(PowerUpBlock(app, x, y, type=2))
            elif cell == "0":
                app.blocks.append(PowerUpBlock(app, x, y, type=3))
            elif cell == "#":
                app.blocks.append(PowerUpBlock(app, x, y, type=4))
            elif cell == "+":
                app.blocks.append(PowerUpBlock(app, x, y, type=5))

            # spawns in random power-up
            elif cell == "%":
                type = random.randint(0, 5)
                app.blocks.append(PowerUpBlock(app, x, y, type=type))

            # spawns in random enemy
            elif cell == "!":
                type = random.randint(1, 3)
                if type == 1:
                    app.enemies.append(Lanternfly(app, x, y))
                elif type == 2:
                    app.enemies.append(Lanternfly2(app, x, y))
                elif type == 3:
                    app.enemies.append(Lanternfly3(app, x, y))

    levelWidth = len(level[0]) * 100
    return levelWidth

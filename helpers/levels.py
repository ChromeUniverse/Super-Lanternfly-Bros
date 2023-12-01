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


def loadRandomLevel(app):
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

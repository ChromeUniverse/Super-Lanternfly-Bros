# CITATION: This pathfinding implementation is based on the
# classic Breadth-first Search (BFS) graph traversal algorithm.
#
# https://en.wikipedia.org/wiki/Breadth-first_search


# checks if a cell is filled or not
def isFilled(grid, cell):
    row, col = cell
    return grid[row][col] != "." and grid[row][col] != "7"


# returns all neighbors of a cell (filled or otherwise)
def getAllNeighbors(cell):
    row, col = cell
    neighbors = []
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    # check if neighbors are within bounds and not filled
    for dr, dc in directions:
        newRow, newCol = row + dr, col + dc
        neighbors.append((newRow, newCol))

    return neighbors


# find the empty neighbors of a given cell
def getNeighbors(grid, cell, rows, cols):
    row, col = cell
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # check if neighbors are within bounds and not filled
    for dr, dc in directions:
        newRow, newCol = row + dr, col + dc
        if (
            0 <= newRow < rows
            and 0 <= newCol < cols
            and not isFilled(grid, (newRow, newCol))
        ):
            neighbors.append((newRow, newCol))

    return neighbors


# checks for valid path between start and end cells in a grid
# using breadth-first search
def isValidPath(grid, start, end):
    rows, cols = len(grid), len(grid[0])

    # keep track of cells visited so far and cells we still need to visit
    visited = set()
    queue = [start]

    while len(queue) > 0:
        currCell = queue.pop(0)

        # found a path!
        if currCell == end:
            return True

        visited.add(currCell)
        neighbors = getNeighbors(grid, currCell, rows, cols)

        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)

    # couldn't find a path
    return False

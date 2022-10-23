'''
To run this file
    1. Copy it into main.py
    2. Press "Run"

To use this program:
    * Press in any cell to create a square ripple
      in this square pond
'''

from cmu_graphics import *

app.stepsPerSecond = 5

app.boardSize = 20
app.cellSize = 400 // app.boardSize

app.ripples = [ ]
app.seenCells = [ ]

def initBoard():
    # Create a board with the appropriate number of rows and columns, and proper
    # cell size. Each cell should have .row and .col custom properties.
    board = makeList(app.boardSize, app.boardSize)
    for row in range(app.boardSize):
        for col in range(app.boardSize):
            cell = Rect(col * app.cellSize, row * app.cellSize, app.cellSize,
                        app.cellSize, border='grey', borderWidth=0.5)
            cell.row = row
            cell.col = col
            board[row][col] = cell
    return board

def turnAllCellsBlack():
    for row in app.board:
        for cell in row:
            cell.fill = 'black'

def getColor(row, col):
    offSet = (row + col) / (app.boardSize * 2)
    g = int(220 - 100 * offSet)
    b = int(100 + 100 * offSet)
    return rgb(0, g, b)

def getCellNeighbors(row, col):
    neighbors = [ ]
    if (row > 0):
        neighbors.append(app.board[row-1][col])
    if (row < app.boardSize - 1):
        neighbors.append(app.board[row+1][col])
    if (col > 0):
        neighbors.append(app.board[row][col-1])
    if (col < app.boardSize - 1):
        neighbors.append(app.board[row][col+1])
    return neighbors

def getNewRippleCells(ripple, seenRippleCells):
    newRipple = [ ]
    newSeenCell = seenRippleCells

    # For the cells in this ripple, get its neighbors. For each neighbor, if we
    # haven't seen it already, change its color and add it to the two returned
    # lists.
    for cell in ripple:
        neighbors = getCellNeighbors(cell.row, cell.col)

        for neighbor in neighbors:
            if (neighbor not in seenRippleCells):
                neighbor.fill = getColor(neighbor.row, neighbor.col)
                newRipple.append(neighbor)
                newSeenCell.append(neighbor)

    return newRipple, newSeenCell

def updateBoard():
    turnAllCellsBlack()

    # For each ripple, gets the next list of cells for that ripple.
    newRipples = [ ]
    newSeenCells = [ ]
    for rippleIndex in range(len(app.ripples)):
        ripple = app.ripples[rippleIndex]
        seenRippleCells = app.seenCells[rippleIndex]
        newRipple, newSeenCell = getNewRippleCells(ripple, seenRippleCells)

        # Only keeps this ripple in the list if there are still cells that are a
        # part of it.
        if (newRipple != [ ]):
            newRipples.append(newRipple)
            newSeenCells.append(newSeenCell)

    app.ripples = newRipples
    app.seenCells = newSeenCells

app.board = initBoard()

def onMousePress(mouseX, mouseY):
    row = mouseY // app.cellSize
    col = mouseX // app.cellSize
    app.ripples.append([ app.board[row][col] ])
    app.seenCells.append([ app.board[row][col] ])

def onStep():
    updateBoard()

cmu_graphics.run()
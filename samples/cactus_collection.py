'''
To run this file
    1. Copy it into main.py
    2. Press "Run"

To use this program:
    * Press any key to add a random cactus to your line
    * Press the space key to add a whole row of cacti
'''

from cmu_graphics import *

app.background = gradient('dodgerBlue', 'lightBlue', start='top')

cacti = Group()
cacti.blockSize = 70

def drawRandomCactus(centerX):
    # Define the random height, width and flower size. The height should be
    # between 50 and 150, the width between 20 and cacti.blockSize, and the
    # flower size between 5 and 15 (all inclusive).
    randomHeight = randrange(50, 151)
    randomWidth = randrange(20, cacti.blockSize + 1)
    randomFlowerSize = randrange(5, 16)

    base = Oval(centerX, 300, randomWidth, randomHeight,
                fill=gradient('mediumSeaGreen', 'seaGreen', start='left'))
    spikes = Oval(centerX, 300, randomWidth + 5, randomHeight + 5, fill=None,
                  border='darkGreen', borderWidth=5, dashes=(2, 6))
    flower = Star(centerX, base.top, randomFlowerSize, 7, fill='gold')
    plant = Group(flower, base, spikes)
    plant.bottom = 430
    cacti.add(plant)

def drawCacti():
    cacti.clear()

    # Draw cacti equally spaced out across the screen.
    for x in range(0, 400, cacti.blockSize):
        drawRandomCactus(x)

def onKeyPress(key):
    if (key == 'space'):
        # Adds a full row of cacti all at once.
        drawCacti()
    else:
        # Move the current cacti left, and remove the plant that moves fully
        # off the screen.
        cacti.left -= cacti.blockSize
        for cactus in cacti.children:
            if (cactus.right <= 0):
                cacti.remove(cactus)

        # Then add a new cactus to the right.
        drawRandomCactus(400 - cacti.blockSize)

cmu_graphics.run()
'''
To run this file
    1. Copy it into main.py
    2. Press "Run"

To use this program:
    * Drag your mouse around on the screen
    * Notice how different shades of leaves fall to the
      ground as you move
'''

from cmu_graphics import *

# Background
app.background = gradient('deepSkyBlue', 'lightCyan', start='top')
leaves = Group()

def onMouseDrag(mouseX, mouseY):
    # Add a new leaf at the mouse as long as there isn't one already there!
    if (not (leaves.hits(mouseX, mouseY) == True)):
        # Randomly choose a red in the range 220 to 255, green in the range
        # 90 to 180, and blue in the range 100 to 130.
        # Make sure to do it in that order so that the autograder runs properly!
        red = randrange(220, 255)
        green = randrange(90, 180)
        blue = randrange(100, 130)

        # Draw a leaf with the random color.
        leaf = Group(
            Polygon(200, 40, 225, 80, 220, 100, 230, 85, 255, 85, 250,
                    105, 235, 120, 260, 130, 235, 150, 200, 140, 165,
                    150, 140, 130, 165, 120, 150, 105, 145, 85, 170,
                    85, 180, 100, 175, 80, fill=rgb(red, green, blue)),
            Polygon(210, 170, 206, 170, 199, 140, 201, 140, 201, 132,
                    240, 130, 201, 130, 235, 100, 201, 128, 200, 70,
                    199, 128, 165, 100, 199, 130, 160, 130, 199, 132,
                    199, 140, 201, 140, fill='sienna')
            )

        # Now set the leaf to have a random width and height in the range 20 and 40
        # and a random angle between 1 and 360, inclusive.
        # Make sure to do it in that order so that the autograder runs properly!
        leaf.width = randrange(20, 40)
        leaf.height = randrange(20, 40)
        leaf.rotateAngle = randrange(1, 360)

        # Randomly choose the horizontal speed between -3 to 3 and vertical
        # speed between 2 and 10.
        # Make sure to do it in that order so that the autograder runs properly!
        leaf.dx = randrange(-3, 3)
        leaf.dy = randrange(2, 10)

        # Set the location of the leaf to the mouse, indicate it is falling,
        # and add it to the leaves group.
        leaf.centerX = mouseX
        leaf.centerY = mouseY
        leaf.isFalling = True
        leaves.add(leaf)

def onStep():
    for leaf in leaves:
        if (leaf.isFalling == True):
            leaf.centerX += leaf.dx
            leaf.centerY += leaf.dy
            leaf.rotateAngle += 2

            # If the leaf reaches within 5 pixels of the bottom of the
            # canvas, stop it falling.
            if (leaf.centerY > 395):
                leaf.isFalling = False

cmu_graphics.run()
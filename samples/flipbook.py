'''
To run this file
    1. Copy it into main.py
    2. Press "Run"

To use this program:
    * Hold the space key to flip through the book!
'''

from cmu_graphics import *

app.background = 'slateBlue'
app.stepsPerSecond = 60

app.isFlipping = False

# book
Rect(60, 80, 50, 240, fill='white')
Line(65, 200, 110, 200, fill='black', lineWidth=240, dashes=(1, 5))
Line(60, 75, 60, 325, lineWidth=5)
Polygon(110, 80, 125, 115, 125, 300, 110, 320, fill='white', border='black',
        borderWidth=1)
Polygon(125, 112, 305, 100, 305, 310, 125, 300)
Polygon(125, 115, 300, 105, 300, 305, 125, 298, fill='white')

# stick figure
body = Oval(230, 215, 30, 60, fill='dimGrey')
head = Circle(230, 175, 15, fill='white', border='dimGrey')
Line(225, 235, 220, 265, fill='dimGrey')
Line(235, 235, 240, 265, fill='dimGrey')
Line(240, 205, 260, 190, fill='dimGrey')
Line(220, 205, 200, 190, fill='dimGrey')

# hula hoop
hoop = Oval(230, 225, 80, 10, fill=None, border='dimGrey')
hoop.movingRight = True

flippingPage = Polygon(125, 115, 255, 80, 255, 315, 125, 300, fill='white',
                       border='black', borderWidth=1, visible=False)

def moveDrawing():
    if (hoop.movingRight == True):
        body.rotateAngle -= 2
        hoop.centerX += 5
        head.centerX -= 1
    else:
        body.rotateAngle += 2
        hoop.centerX -= 5
        head.centerX += 1

    if ((hoop.centerX < 215) or (hoop.centerX > 245)):
        hoop.movingRight = not hoop.movingRight

def onKeyHold(keys):
    # Do all the following when the space key is held.
    if ('space' in keys):

        # If page is not flipping, show a flipping page, change the custom
        # property to flip the page, and move the drawing.
        if (not (app.isFlipping == True)):
            flippingPage.visible = True
            app.isFlipping = True
            moveDrawing()

        # If the width of page is greater than 30 while flipping the page,
        # decrease the width by 30.
        elif ((app.isFlipping == True) and (flippingPage.width > 30)):
            flippingPage.width -= 30
            flippingPage.left = 125

        # If the width of the flipping page is 50 or less, stop flipping,
        # hide the page, and reset the width.
        elif (flippingPage.width <= 50):
            app.isFlipping = False
            flippingPage.visible = False
            flippingPage.width = 130
            flippingPage.left = 125

cmu_graphics.run()
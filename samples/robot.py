'''
To run this file
    1. Copy it into main.py
    2. Press "Run"

To use this program:
    * Try pressing r, g, left, right, or any other key
'''

from cmu_graphics import *

app.background = 'lemonChiffon'
Line(0, 200, 400, 200, fill='mediumPurple', lineWidth=400, dashes=(55, 35))

# head
Star(200, 50, 25, 15, fill=None, border='gold', roundness=20)
Line(200, 60, 200, 100)
Circle(200, 50, 10, fill='gold')
Rect(200, 150, 100, 100, fill='lightGrey', align='center')
Circle(150, 125, 25, fill='lightGrey')
Circle(150, 175, 25, fill='lightGrey')
Rect(125, 125, 25, 50, fill='lightGrey')
Circle(250, 125, 25, fill='lightGrey')
Circle(250, 175, 25, fill='lightGrey')
Rect(250, 125, 25, 50, fill='lightGrey')

# eyes
leftEye = Circle(160, 125, 15, fill='white', border='dimGrey', borderWidth=3)
Circle(160, 125, 5, fill='dimGrey')
leftEyeLid = Line(147, 125, 173, 125, visible=False)
rightEye = Circle(240, 125, 15, fill='white', border='dimGrey', borderWidth=3)
Circle(240, 125, 5, fill='dimGrey')
rightEyeLid = Line(227, 125, 253, 125, visible=False)

# mouth
Rect(170, 150, 60, 35, fill='white')
Circle(170, 160, 10, fill='white')
Circle(230, 160, 10, fill='white')
Circle(170, 175, 10, fill='white')
Circle(230, 175, 10, fill='white')
Rect(160, 160, 10, 15, fill='white')
Rect(230, 160, 10, 15, fill='white')
Line(175, 170, 230, 170, lineWidth=25, dashes=(1, 15))
Line(165, 170, 235, 170, lineWidth=1)

# neck
Rect(175, 200, 50, 25, fill='lightGrey')
Line(200, 200, 200, 225, fill='grey', dashes=(5, 4), lineWidth=50)

# arms
leftArm = Line(160, 250, 100, 200, dashes=(5, 4), lineWidth=20)
leftHand = Circle(100, 200, 20)
rightArm = Line(240, 250, 300, 200, dashes=(5, 4), lineWidth=20)
rightHand = Circle(300, 200, 20)

# body
Rect(160, 225, 80, 100, fill='lightGrey')
Circle(160, 235, 10, fill='lightGrey')
Circle(160, 315, 10, fill='lightGrey')
Rect(150, 235, 10, 80, fill='lightGrey')
Circle(240, 235, 10, fill='lightGrey')
Circle(240, 315, 10, fill='lightGrey')
Rect(240, 235, 10, 80, fill='lightGrey')

# legs
Rect(160, 325, 30, 75, fill='lightGrey')
Rect(210, 325, 30, 75, fill='lightGrey')
Line(175, 325, 175, 400, fill='dimGrey', dashes=(3, 6), lineWidth=30)
Line(225, 325, 225, 400, fill='dimGrey', dashes=(3, 6), lineWidth=30)

redButton = Circle(175, 250, 8, fill='white', border='red')
greenButton = Circle(175, 275, 8, fill='white', border='green')
board = Oval(225, 265, 30, 50, fill='white', border='royalBlue')

def onMouseDrag(mouseX, mouseY):
    # If the mouse is on the left half of the canvas, move the left arm to the
    # mouse location. Otherwise, move the right arm to the mouse location.
    if (mouseX < 200):
        leftArm.x2 = mouseX
        leftArm.y2 = mouseY
        leftHand.centerX = mouseX
        leftHand.centerY = mouseY
    else:
        rightArm.x2 = mouseX
        rightArm.y2 = mouseY
        rightHand.centerX = mouseX
        rightHand.centerY = mouseY

def onKeyPress(key):
    # If the'r' or 'g' is pressed, color the button whose color name starts with
    # that letter. If the left or right arrow is pressed, close the appropriate
    # eye. Otherwise, color the circuit board blue.
    if (key == 'r'):
        redButton.fill = 'red'
    elif (key == 'g'):
        greenButton.fill = 'green'
    elif (key == 'left'):
        leftEye.fill = 'dimGrey'
        leftEyeLid.visible = True
    elif (key == 'right'):
        rightEye.fill = 'dimGrey'
        rightEyeLid.visible = True
    else:
        board.fill = 'royalBlue'

def onKeyRelease(key):
    # Do the reverse of the actions in onKeyPress. In other words, if 'r' or 'g'
    # is released, color the appropriate button white. If the left or right arrow
    # key is released, open that eye. Otherwise, turn the circuit board white.
    if (key == 'r'):
        redButton.fill = 'white'
    elif (key == 'g'):
        greenButton.fill = 'white'
    elif (key == 'left'):
        leftEye.fill = 'white'
        leftEyeLid.visible = False
    elif (key == 'right'):
        rightEye.fill = 'white'
        rightEyeLid.visible = False
    else:
        board.fill = 'white'

cmu_graphics.run()
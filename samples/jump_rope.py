'''
To run this file
    1. Copy it into main.py
    2. Press "Run"

To use this program:
    * Press space to jump. Don't let the rope hit your legs!
'''

from cmu_graphics import *

app.stepsPerSecond = 20
app.paused = True
app.background = gradient('lightBlue', 'steelBlue', start='left')

rope = Oval(200, 200, 300, 200, fill=None, border='red')
ropeCover = Rect(200, 200, 400, 200, fill=app.background, align='top')
rope.dh = -25

# rope holders
Line(50, 200, 15, 215, fill=rgb(70, 75, 75), lineWidth=3)
Line(15, 300, 15, 190, fill=rgb(70, 75, 75), lineWidth=4)
Circle(15, 175, 20, fill=rgb(70, 75, 75))
Line(350, 200, 385, 215, fill=rgb(70, 75, 75), lineWidth=3)
Line(385, 300, 385, 190, fill=rgb(70, 75, 75), lineWidth=4)
Circle(385, 175, 20, fill=rgb(70, 75, 75))

# jumping person
leftLeg = Line(200, 250, 175, 300, fill=rgb(70, 75, 75), lineWidth=3)
stickPerson = Group(
    Circle(200, 175, 20, fill=rgb(70, 75, 75)),
    Line(200, 190, 200, 250, fill=rgb(70, 75, 75), lineWidth=4),
    Line(200, 215, 160, 150, fill=rgb(70, 75, 75), lineWidth=3),
    Line(200, 215, 240, 150, fill=rgb(70, 75, 75), lineWidth=3),
    Line(200, 250, 225, 300, fill=rgb(70, 75, 75), lineWidth=3),
    leftLeg
    )
stickPerson.isJumping = False
stickPerson.dy = -5

Label('Press r to start the rope', 200, 25, fill=rgb(70, 75, 75), size=15)
Label('Press space to jump', 200, 50, fill=rgb(70, 75, 75), size=15)
jumpRopeCounter = Label(0, 200, 80, fill=rgb(70, 75, 75), size=25)
endGameMessage = Label('You didnt jump over the rope!', 200, 365,
                       fill=rgb(70, 75, 75), size=25, visible=False)

def moveJumpingPerson():
    if (stickPerson.isJumping == True):
        stickPerson.centerY += stickPerson.dy

    # Changes if the person is jumping up or falling down by adjusting the
    # dy property.
    if (stickPerson.bottom <= 270):
        stickPerson.dy = 5
    elif (stickPerson.bottom >= 300):
        stickPerson.dy = -5
        stickPerson.isJumping = False

def moveJumprope():
    # Change the rope's height using custom properties.
    rope.height += rope.dh

    # When the rope gets too small or large, change if it is shrinking or not.
    if (rope.height <= 25):
        rope.dh *= -1

        # Move the ropeCover so that the proper half of the rope Oval shows.
        if (ropeCover.top == 200):
            ropeCover.bottom = 200
        else:
            ropeCover.top = 200

    if (rope.height >= 200):
        rope.dh *= -1

        # If the rope hits the legs when it is swinging down, the game pauses.
        if ((rope.hitsShape(leftLeg) == True) and (ropeCover.bottom == 200)):
            app.paused = True
            endGameMessage.visible = True

        # Otherwise, add one to the counter everytime the person jumps over the
        # rope.
        elif (ropeCover.bottom == 200):
            jumpRopeCounter.value += 1

def onKeyPress(key):
    # When the r key is pressed, the rope starts moving and the counter is set
    # to 0.
    if (key == 'r'):
        app.paused = False
        jumpRopeCounter.value = 0
        endGameMessage.visible = False

    # When the space key is pressed, the person begins jumping.
    if ((key == 'space') and (app.paused == False)):
        stickPerson.isJumping = True

def onStep():
    moveJumprope()
    moveJumpingPerson()

cmu_graphics.run()
'''
To run this file
    1. Copy it into main.py
    2. Press "Run"

To use this program:
    * Click the mouse to turn on the UFO's spotlight
    * Click and drag the mouse to move the spotlight
      around
    * Who's hiding in the shadows??
'''

from cmu_graphics import *

app.background = gradient('black', 'black', 'midnightBlue', 'darkSlateBlue',
                          start='top')

light = Line(115, 90, 200, 420, fill=gradient('white', 'lightGrey'),
             lineWidth=50, opacity=70, visible=False)

# spaceship
Oval(115, 85, 70, 50, fill='gold')
Oval(115, 95, 60, 30, fill='orange')
Oval(115, 90, 120, 25, fill='coral')
Oval(115, 80, 70, 10, fill='gold')
Circle(70, 85, 3, fill='white')
Circle(85, 90, 3, fill='white')
Circle(105, 92, 3, fill='white')
Circle(125, 92, 3, fill='white')
Circle(145, 90, 3, fill='white')
Circle(160, 85, 3, fill='white')

# stars
Star(45, 45, 5, 5, fill='white')
Star(190, 20, 5, 5, fill='white')
Star(270, 65, 5, 5, fill='white')
Star(365, 35, 5, 5, fill='white')
Star(280, 275, 5, 5, fill='white')
Star(245, 179, 5, 5, fill='white')
Star(150, 210, 5, 5, fill='white')
Star(35, 250, 5, 5, fill='white')
Star(345, 205, 5, 5, fill='white')

# person
Line(325, 400, 330, 380)
Line(340, 380, 345, 400)
leftArm = Line(325, 360, 315, 370)
rightArm = Line(345, 360, 350, 370)
body = Oval(335, 365, 20, 40)
face = Circle(335, 340, 10)
Circle(333, 335, 1)
Circle(340, 335, 1)
mouth = Circle(336, 342, 3)

def hidePerson():
    # Make the body and face blend in with the background and move the arms.
    body.fill = 'black'
    face.fill = 'black'
    leftArm.y2 = 370
    rightArm.y2 = 370

def onMousePress(mouseX, mouseY):
    # Show the light.
    light.visible = True

def onMouseDrag(mouseX, mouseY):
    # Make the light follow the mouse and if the light is over the character,
    # show them. Otherwise, call hidePerson().
    light.x2 = mouseX
    if (mouseX > body.left):
        body.fill = 'lightSkyBlue'
        face.fill = 'white'
        leftArm.y2 = 350
        rightArm.y2 = 350
    else:
        hidePerson()

cmu_graphics.run()
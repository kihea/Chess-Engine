'''
To run this file
    1. Copy it into main.py
    2. Press "Run"

To use this program:
    * Click on the apples to watch them fall
'''

from cmu_graphics import *

app.background = gradient('lightCyan', 'lightSkyBlue', start='bottom')

# grass and tree
Oval(130, 450, 900, 250, fill=gradient('darkGoldenrod', 'forestGreen', start='top'))
Rect(200, 150, 30, 200, fill='sienna')
Line(220, 230, 130, 150, fill='sienna', lineWidth=10)
Line(220, 250, 320, 150, fill='sienna', lineWidth=10)
Oval(220, 95, 150, 160, fill=gradient('green', 'darkGreen', start='top'))
Oval(160, 100, 200, 130, fill=gradient('green', 'darkGreen', start='left'))
Oval(280, 90, 200, 150, fill=gradient('green', 'darkGreen', start='right'))
Line(170, 185, 180, 130, fill='sienna', lineWidth=10)
Line(270, 200, 250, 140, fill='sienna', lineWidth=10)

apples = Group()
fallingApples = Group()

def drawApple(cx, cy):
    apple = Group(
        Line(200, 185, 200, 195, fill='brown'),
        Circle(200, 200, 11, fill=gradient('darkRed', 'orangeRed', start='left-top'))
        )
    apple.centerX = cx
    apple.centerY = cy
    apple.dy = 3
    apples.add(apple)

drawApple(230, 90)
drawApple(90, 110)
drawApple(180, 120)
drawApple(150, 90)
drawApple(200, 60)
drawApple(135, 155)
drawApple(350, 130)
drawApple(290, 100)
drawApple(250, 155)
drawApple(325, 50)
drawApple(300, 160)

def onMousePress(mouseX, mouseY):
    # When an apple is clicked, make it fall to the ground.
    for apple in apples.children:
        if (apple.hits(mouseX, mouseY) == True):
            apples.remove(apple)
            fallingApples.add(apple)

def onStep():
    # Move all of the falling apples if they haven't reached the base of the tree
    # yet.
    for apple in fallingApples.children:
        if (apple.centerY < 350):
            apple.centerY += apple.dy

cmu_graphics.run()
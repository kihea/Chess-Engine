'''
To run this file
    1. Copy it into main.py
    2. Press "Run"

To use this program:
    * Press the mouse to make the frog grab the fly
    * Release the mouse to eat it!
'''

from cmu_graphics import *
import random

app.background = gradient('paleTurquoise', 'honeydew', start='bottom')

# legs
Oval(105, 260, 55, 155, fill='seaGreen', rotateAngle=-15)
Oval(110, 265, 50, 150, fill='limeGreen', rotateAngle=-15)
Oval(295, 260, 55, 155, fill='seaGreen', rotateAngle=15)
Oval(290, 265, 50, 150, fill='limeGreen', rotateAngle=15)

# body
Circle(155, 160, 35, fill='seaGreen')
Circle(245, 160, 35, fill='seaGreen')
Oval(200, 260, 215, 225, fill='seaGreen')
Oval(200, 260, 200, 220, fill='limeGreen')
Oval(200, 330, 150, 150, fill='greenYellow')
Rect(200, 330, 180, 70, fill='paleTurquoise', align='top')

# feet
Oval(100, 330, 50, 20, fill='seaGreen', rotateAngle=-5)
Oval(110, 335, 40, 20, fill='seaGreen', rotateAngle=-40)
Oval(125, 335, 30, 15, fill='seaGreen', rotateAngle=-90)
Oval(300, 330, 50, 20, fill='seaGreen', rotateAngle=5)
Oval(290, 335, 40, 20, fill='seaGreen', rotateAngle=40)
Oval(275, 335, 30, 15, fill='seaGreen', rotateAngle=90)

# eyes
Circle(155, 160, 30, fill='limeGreen')
Circle(245, 160, 30, fill='limeGreen')
Circle(155, 160, 20, border='white', borderWidth=12)
Circle(245, 160, 20, border='white', borderWidth=12)

# mouth
Oval(210, 225, 40, 30, fill='seaGreen', rotateAngle=-10)
Rect(210, 215, 70, 25, fill='limeGreen', rotateAngle=-10, align='center')

fly = Star(100, 100, 10, 4, roundness=55,
           fill=gradient('whiteSmoke', 'black', 'whiteSmoke', start='top'))
tongue = Line(210, 235, 300, 150, fill='pink', lineWidth=5, visible=False)

Label('Flies caught: ', 15, 20, size=20, align='left')
flyCount = Label(0, 135, 20, size=20, align='left')

def onMousePress(mouseX, mouseY):
    # Make the tongue appear and extend to where the fly is.
    tongue.visible = True
    tongue.x2 = fly.centerX
    tongue.y2 = fly.centerY

def onMouseRelease(mouseX, mouseY):
    # Make the tongue disapear, move the fly, and increase the counter by 1.
    tongue.visible = False

    fly.centerX = random.randrange(50, 350)
    fly.centerY = random.randrange(50, 350)
    flyCount.value += 1

cmu_graphics.run()
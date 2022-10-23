'''
To run this file
    1. Copy it into main.py
    2. Press "Run"

To use this program:
    * Yummmmm. Nothing to do here, but those cookies
      look delicious
'''

from cmu_graphics import *

app.background = 'saddleBrown'

app.toppings = [ 'sprinkles', 'chocolate', 'marshmallow',
                 'sprinkles', 'sprinkles', 'chocolate',
                 'marshmallow', 'sprinkles', 'chocolate' ]

# oven rack and cookie sheet
Line(50, 200, 351, 200, lineWidth=400, fill='ghostWhite', dashes=(20, 50))
Rect(15, 15, 370, 370, fill='silver', border='grey', borderWidth=5)

def drawChocolate(cx, cy):
    Rect(cx, cy, 20, 30, fill='brown', align='center')
    Line(cx, cy - 6, cx, cy + 9, fill='darkGoldenrod', lineWidth=18,
         dashes=(1, 9))

def drawSprinkles(cx, cy):
    colors = [ 'red', 'green', 'blue', 'orange', 'purple' ]
    for i in range(20):
        randAngle = randrange(0, 360)
        randDist = randrange(5, 35)
        x, y = getPointInDir(cx, cy, randAngle, randDist)

        # Get a random color for the colors list.
        color = choice(colors)

        Circle(x, y, 2, fill=color)

def drawMarshmallow(cx, cy):
    Oval(cx, cy, 25, 25, fill='white')

def drawCookie(cx, cy):
    Circle(cx + 1, cy + 3, 40, fill='saddleBrown')
    Circle(cx, cy, 40, fill=gradient(rgb(200, 165, 95), 'peru'))

def drawToppings(toppingIndex, cx, cy):
    # Use the topping index to get the type of topping for this cookie and draw
    # it.
    topping = app.toppings[toppingIndex]

    if (topping == 'chocolate'):
        drawChocolate(cx, cy)
    elif (topping == 'sprinkles'):
        drawSprinkles(cx, cy)
    elif (topping == 'marshmallow'):
        drawMarshmallow(cx, cy)

def drawCookies():
    # Update this function so that it keeps track of an index for the toppings.
    # Call the drawToppings function with this index.
    toppingIndex = 0
    for row in range(3):
        for col in range(3):
            cx = 80 + col * 120
            cy = 80 + row * 120

            drawCookie(cx, cy)
            drawToppings(toppingIndex, cx, cy)
            toppingIndex += 1

drawCookies()

cmu_graphics.run()
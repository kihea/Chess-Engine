'''
To run this file
    1. Copy it into main.py
    2. Press "Run"

To use this program:
    * Realize rainy days don't always have to be dreary
    * Just sit back and appreciate the beauty
'''

from cmu_graphics import *

# Road (1 Rectangle, 1 Line)
Rect(0, 0, 400, 400)
Line(-50, 100, 450, 300, fill=gradient('lightGrey', 'white', start='left'),
     lineWidth=250,  dashes=(30, 40))

# Dog (3 Ovals, 2 Circles, 2 Lines)
Oval(230, 135, 50, 30, fill='darkGoldenrod', rotateAngle=20)
Circle(255, 145, 12, fill='darkGoldenrod')
Oval(260, 140, 15, 8, fill='sienna', rotateAngle=20)
Oval(255, 155, 15, 8, fill='sienna')
Circle(205, 130, 5, fill='darkGoldenrod')
Line(185, 90, 247, 143, fill='forestGreen', lineWidth=5)
Line(245, 150, 250, 135, fill='forestGreen', lineWidth=3)

# Umbrellas (3 Regular Polygons, 3 Stars, 3 Circles)
RegularPolygon(150, 80, 60, 10, fill='lightGreen')
Star(150, 80, 60, 10, fill='green', roundness=0)
Circle(150, 80, 5, fill=rgb(0, 80, 0))

RegularPolygon(375, 220, 65, 10, fill='lightSalmon')
Star(375, 220, 65, 10, fill='fireBrick', roundness=0)
Circle(375, 220, 5, fill=rgb(100, 20, 20))

RegularPolygon(200, 300, 50, 10, fill='gold')
Star(200, 300, 50, 10, fill='chocolate', roundness=0)
Circle(200, 300, 4, fill='sienna')

# Puddles (6 Circles)
Circle(35, 320, 30, fill='steelBlue', opacity=50)
Circle(15, 370, 10, fill='steelBlue', opacity=50)

Circle(260, 405, 35, fill='steelBlue', opacity=50)
Circle(120, 200, 20, fill='steelBlue', opacity=50)

Circle(340, 45, 20, fill='steelBlue', opacity=50)
Circle(370, 15, 30, fill='steelBlue', opacity=50)

cmu_graphics.run()
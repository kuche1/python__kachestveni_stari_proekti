import math

def rast(item1x, item1y, item2x, item2y):
    c = math.sqrt(abs(item1x - item2x)**2 + abs(item1y - item2y)**2)
    return c

def doko(item1X, item1Y, item1DX, item1DY, item2X, item2Y, item2DX, item2DY):
    if item1X + item1DX > item2X and item1X < item2X + item2DX and item1Y + item1DY > item2Y and item1Y < item2Y + item2DY:
        return True
    return False


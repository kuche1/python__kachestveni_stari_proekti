

def rast(x1, y1, x2, y2):
    a = abs(x1-x2)
    b = abs(y1-y2)
    return ((a**2)+(b**2))**0.5

def doko(item1X, item1Y, item1DX, item1DY, item2X, item2Y, item2DX, item2DY):
    if item1X + item1DX > item2X and item1X < item2X + item2DX and item1Y + item1DY > item2Y and item1Y < item2Y + item2DY:
        return True
    return False

def getchange(x1, y1, x2, y2):
    rastoqnieX = abs(x1 - x2)
    rastoqnieY = abs(y1 - y2)
    rastoqnie = (rastoqnieX, rastoqnieY)
    x = (min(rastoqnie))/(max(rastoqnie))
    if rastoqnie.index(max(rastoqnie)) == 0:
        changeX = 1
        changeY = x
    else:
        changeX = x
        changeY = 1
    if x2 < x1:
        changeX *= -1
    if y2 < y1:
        changeY *= -1
    return [changeX, changeY]

def ch(start, end):
    choise = input('>')
    try:
        choise = int(choise)
    except:
        return False
    else:
        if choise < start:
            return False
        if choise > end:
            return False
        return choise

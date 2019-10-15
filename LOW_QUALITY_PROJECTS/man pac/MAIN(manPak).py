import pygame
import random
import sys
import os
import time
from colors import *



pygame.init()

FPS = 60

displayX = 800
displayY = 600
gameDisplay = pygame.display.set_mode((displayX, displayY))

clock = pygame.time.Clock()


def msg(text, x, y, color=green, size=20):
    font = pygame.font.Font(None, size)
    text = font.render(str(text), 1, color)
    gameDisplay.blit(text, (x, y))

def loadS(fileName, papkaName='myzik'):
    return pygame.mixer.Sound(os.path.join(papkaName, fileName))

soundtrack = []
toundYourselfSound = None
def loadSounds():
    global soundtrack
    global touchYourselfSound
    path = sys.argv[0]
    path = path[:-9]
    path = path + '/myzik'

    onlyFiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    
    #for x in range(len(onlyFiles)):
    x = 0
    while x < len(onlyFiles):
        soundtrack.append([onlyFiles[x][:-4], loadS(onlyFiles[x])])
        x += 1

        gameDisplay.fill(black)
        msg('Loaded %s%s' %(int(((x+1)/len(onlyFiles))*100), '%'), 0, 0, color=green, size=40)
        pygame.display.update()

    gameDisplay.fill(black)
    msg('Loading additional files', 0, 0, color=green, size=40)
    pygame.display.update()


    touchYourselfSound = [loadS('manScreams.wav', 'elseMyzik'), False]


def dokosvane(item1x, item1y, item1DX, item1DY, item2x, item2y, item2DX, item2DY):
    if (item1x + item1DX > item2x and item1x < item2x + item2DX) and (item1y + item1DY > item2y and item1y < item2y + item2DY):
        return True
    return False

def generateApple():
    apple = [random.randint(blockSize, displayX-blockSize), random.randint(blockSize, displayY-blockSize)]
    for item in snakeBody:
        if dokosvane(item[0], item[1], yourD, yourD, apple[0], apple[1], blockSize, blockSize):
            apple = generateApple()
            break
    return apple

def napushenBackground(menuColor, otkolko=-10, dokolko=10, rejectChanse=0):
        for x in range(3):
            if random.random() < rejectChanse:
                continue
            rand1 = random.randint(otkolko, dokolko)
            if menuColor[x] + rand1 > 0 and menuColor[x] + rand1 < 255:
                menuColor[x] += rand1
        return menuColor

def swagUpMenu():
    global swagUpMenuColor

    global swagUpPoints
    global blockSize
    global yourD
    global yourSpeed
    global napushenost
    global lastPlayedSong

    done = False
    while (swagUpPoints > 0) and (done == False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    swagUpPoints -= 1
                    blockSize += 1
                if event.key == pygame.K_x:
                    swagUpPoints -= 1
                    blockSize -= 1
                if event.key == pygame.K_c:
                    swagUpPoints -= 1
                    yourD += 1
                if event.key == pygame.K_v:
                    swagUpPoints -= 1
                    yourD -= 1
                if event.key == pygame.K_b:
                    swagUpPoints -= 1
                    yourSpeed += 0.5
                if event.key == pygame.K_n:
                    swagUpPoints -= 1
                    yourSpeed -= 0.5
                if event.key == pygame.K_m or event.key == pygame.K_a:
                    if napushenost < len(nivaNaNapushenost)-1:
                        swagUpPoints -= 1
                        napushenost += 1
                if event.key == pygame.K_s:
                    done = True
                if event.key == pygame.K_d:
                    swagUpPoints -= 0.5
                    randomlyChoosenSong = random.randrange(0, len(soundtrack))
                    lastPlayedSong = [soundtrack[randomlyChoosenSong][0], randomlyChoosenSong]
                    soundtrack[randomlyChoosenSong][1].play()
                if event.key == pygame.K_f:
                    swagUpPoints -= 1
                    for x in range(len(soundtrack)):
                        soundtrack[x][1].stop()

                        
        swagUpMenuColor = napushenBackground(swagUpMenuColor)
        color = [(255-swagUpMenuColor[0]), (255-swagUpMenuColor[1]), (255-swagUpMenuColor[2])]

        gameDisplay.fill(swagUpMenuColor)

        msg('SWAG Up P0Int$ = %s' %(swagUpPoints), 0, 0, color, size=60)
        msg('itemName=(item Value) (item description) (how much to change/button to increase/button to decrease)', 0, 80, color, size=23)
        msg('blockSize=%s (the size of the apple) (1/z/x)' %(blockSize), 50, 105, color, size=25)
        msg('yourD=%s (your size) (1/c/v)' %(yourD), 50, 130, color, size=25)
        msg('yourSpeed=%s (your speed) (0.5/b/n)' %(yourSpeed), 50, 155, color, size=25)
        msg('napushenost=%s/%s (your kolko si napushen) (1/m/a)' %(napushenost, 10), 50, 180, color, size=25)
        msg('PRESS S TO EXIT THIS MENU', 50, 205, color, size=25)
        msg('pesen=%s (play muzikata) (0.5/d/)' %(lastPlayedSong[0]), 50, 230, color, size=25)
        msg('StopAll (spira si4kata muzika ot soundtrack-a) (1/f/)', 50, 255, color, size=25)

        
        pygame.display.update()
        clock.tick(50)

loadSounds()

fullscreen = False

blockSize = 20

yourD = blockSize
yourSpeed = 4

yourXP = 0
maxXP = 100
swagLevel = 0
napushenost = 0
nivaNaNapushenost = ['0/10', '1/10', '1/10+', '1/10++', '1+/10-', 'mno go sam na pu shen', 'rysLazar', 'sys']
yourHealthyLevel = 100
yourVeganLevel = 0.01
swagUpPoints = 0
lastPlayedSong = ['None', None]

yourMaxLen = 5



yourX = 50
yourY = 50

snakeBody = [[yourX, yourY]]

yourXchange = yourSpeed
yourYchange = 0
minatoRastoqnie = 0
youDamaged = False

apple = generateApple()



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and yourYchange != yourSpeed:
                yourYchange = -yourSpeed
                yourXchange = 0
            elif event.key == pygame.K_LEFT and yourXchange != yourSpeed:
                yourXchange = -yourSpeed
                yourYchange = 0
            elif event.key == pygame.K_DOWN and yourYchange != -yourSpeed:
                yourYchange = yourSpeed
                yourXchange = 0
            elif event.key == pygame.K_RIGHT and yourXchange != -yourSpeed:
                yourXchange = yourSpeed
                yourYchange = 0
            elif event.key == pygame.K_p:
                if fullscreen == False:
                    gameDisplay = pygame.display.set_mode((displayX, displayY), pygame.FULLSCREEN)
                    fullscreen = True
                else:
                    gameDisplay = pygame.display.set_mode((displayX, displayY))
            elif event.key == pygame.K_SPACE:
                if yourXP >= maxXP:
                    swagLevel += 1
                    yourXP -= maxXP
                    maxXP += (5/100)*maxXP
                    swagUpPoints += 3
                    swagUpMenu()


    gameDisplay.fill(backgroundColor)


    for x in range(len(snakeBody)-1, 0, -1):
        snakeBody[x] = snakeBody[x-1]
    snakeBody[0] = [yourX, yourY]


    yourX += yourXchange
    yourY += yourYchange

    minatoRastoqnie += yourSpeed*(1+len(snakeBody))


    if yourX + yourD <= 0:
        yourX = displayX - yourSpeed
    elif yourX >= displayX:
        yourX = 0 -yourD + yourSpeed

    if yourY + yourD <= 0:
        yourY = displayY -yourSpeed
    elif yourY >= displayY:
        yourY = 0 -yourD + yourSpeed


    youDamaged = False
    for x in range(len(snakeBody)):
        if yourD - ((x-1)*yourSpeed)/2 < 0:
            if dokosvane(yourX, yourY, yourD, yourD, snakeBody[x][0], snakeBody[x][1], yourD, yourD):
                youDamaged = True
                yourHealthyLevel -= 0.001

    if youDamaged == False:
        FPS = 60
        touchYourselfSound[0].fadeout(800)
        touchYourselfSound[1] = False
    else:
        FPS = 10
        if touchYourselfSound[1] == False:
            touchYourselfSound[0].play()
            touchYourselfSound[1] = True
    
    if dokosvane(yourX, yourY, yourD, yourD, apple[0], apple[1], blockSize, blockSize):
        yourVeganLevel *= 11/10
        yourXP += 10
        apple = generateApple()
        snakeBody.insert(0, [yourX, yourY])


    backgroundColor = napushenBackground(backgroundColor, -1, 1, 1-(napushenost/len(nivaNaNapushenost)))




    pygame.draw.rect(gameDisplay, sivo, (0, 0, (yourXP/maxXP * displayX), 2))
    msg('SWAG=%s' %(swagLevel), 0, 0, color=green, size=20)
    msg('FPS=%s.%s' %(60, random.randint(0, 99999)), 0, 20, color=green, size=20)
    msg('napushenost=%s' %(nivaNaNapushenost[napushenost]), 0, 40, color=green, size=20)
    msg('rastoiqnie=%s' %(minatoRastoqnie), 0, 60, color=green, size=20)
    msg('daljina=%s' %(1+len(snakeBody)), 0, 80, color=green, size=20)
    msg('maxLenght=%s' %(yourMaxLen), 0, 100, color=green, size=20)
    msg('yourHealthyLevel=%s' %(yourHealthyLevel), 0, 120, color=green, size=20)
    msg('yourVeganLevel=%s%s' %(yourVeganLevel, '%'), 0, 140, color=green, size=20)
    mesij = str()
    for x in range(int(yourSpeed)):
        mesij += '+'
    msg('barzina=normal%s' %(mesij), 0, 160, color=green, size=20)
    msg('lastPlayedSong=%s' %(lastPlayedSong[0]), 0, 180, color=green, size=20)
    if yourXP >= maxXP:
        msg('PRESS SPACE TO EVOLVE', 0, 200, color=green, size=20)
    msg('press P to change between FULL-SCREEN and WINDOWED', 0, 220, color=green, size=20)

    pygame.draw.rect(gameDisplay, red, (apple[0], apple[1], blockSize, blockSize))

    for item in snakeBody:
        pygame.draw.rect(gameDisplay, green, (item[0], item[1], yourD, yourD))
    pygame.draw.rect(gameDisplay, blue, (yourX, yourY, yourD, yourD))

    
    pygame.display.update()
    clock.tick(FPS)



import pygame
import os
from settings import *
from colors import *

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("")

gameDisplay = pygame.display.set_mode((displayX, displayY))
FPS = 30

def doko(item1X, item1Y, item1DX, item1DY, item2X, item2Y, item2DX, item2DY):
    if item1X + item1DX > item2X and item1X < item2X + item2DX and item1Y + item1DY > item2Y and item1Y < item2Y + item2DY:
        return True
    return False

def createMap(fileName):
    if os.path.isfile(fileName+'.py'):
        createMap(fileName+str('0'))
    else:
        f = open(fileName+'.py', 'w')
        f.write('''
walls = %s
''' %(walls))
        f.close()
        print('map saved to: %s' %(fileName+'.py'))

def addWall():
    global walls
    if placingMode == 1:
        walls.append([cur[0], cur[1], stenaDX, stenaDY, stenaHP, stenaHP])
    elif placingMode == 2:
        for y in range(cur[1], cur[1]+stenaDY, placingMode2StenaPres):
            for x in range(cur[0], cur[0]+stenaDX, placingMode2StenaPres):
                walls.append([x, y, placingMode2StenaPres, placingMode2StenaPres, stenaHP, stenaHP])
    else:
        print('ERROR')

def removeWall():
    global walls
    for x in range(len(walls)):
        if doko(cur[0], cur[1], 1, 1, walls[x][0], walls[x][1], walls[x][2], walls[x][3]):
            del walls[x]
            break

quittingGame = False
walls = []
stenaDX = 20
stenaDY = 20
stenaHP = 500

wPressed = False
aPressed = False
sPressed = False
dPressed = False

changeValue = 1
placingMode = 1
placingMode2StenaPres = 20
while not quittingGame:

    gameDisplay.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quittingGame = True
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                placingMode = 1
                print('placingMode=1')
            if event.key == pygame.K_2:
                placingMode = 2
                print('placingMode=2')
            if event.key == pygame.K_e:
                addWall()
            if event.key == pygame.K_q:
                removeWall()
            if event.key == pygame.K_w:
                wPressed = True
            if event.key == pygame.K_a:
                aPressed = True
            if event.key == pygame.K_s:
                sPressed = True
            if event.key == pygame.K_d:
                dPressed = True
            if event.key == pygame.K_k:
                createMap('customMap')
            if event.key == pygame.K_h:
                print('enter value for stenaHP')
                new = input('>')
                try:
                    new = int(new)
                    stenaHP = new
                except:
                    print('invalid')
            if event.key == pygame.K_i:
                print('enter map name to import')
                new = input('>')
                try:
                    exec('import %s' %(new))
                    exec('walls = %s.walls' %(new))
                except:
                    print('ERROR')
                    
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                wPressed = False
            if event.key == pygame.K_a:
                aPressed = False
            if event.key == pygame.K_s:
                sPressed = False
            if event.key == pygame.K_d:
                dPressed = False

                
    cur = pygame.mouse.get_pos()  
    click = pygame.mouse.get_pressed()

    if wPressed:
        stenaDY -= changeValue
    if aPressed:
        stenaDX -= changeValue
    if sPressed:
        stenaDY += changeValue
    if dPressed:
        stenaDX += changeValue

    if click[0] == 1:
        addWall()
    if click[2] == 1:
        removeWall()


    
    for item in walls:
        pygame.draw.rect(gameDisplay, white, (item[0], item[1], item[2], item[3]))
    stdx = stenaDX
    stdy = stenaDY
    if placingMode == 2:
        if stdx%placingMode2StenaPres != 0:
            stdx = stenaDX-(stenaDX%placingMode2StenaPres) + placingMode2StenaPres
        if stdy%placingMode2StenaPres != 0:
            stdy = stenaDY-(stenaDY%placingMode2StenaPres) + placingMode2StenaPres
    pygame.draw.rect(gameDisplay, white, (cur[0], cur[1], stdx, stdy))
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
quit()


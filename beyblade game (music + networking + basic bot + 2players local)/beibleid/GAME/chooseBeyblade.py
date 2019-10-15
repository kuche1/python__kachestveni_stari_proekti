import pygame
import random
import copy
import settings

from colors import *
from funcs import *


def main(NADPIS='Choose beyblade'):

    pygame.init()

    FPS = 60

    displayX = settings.displayX
    displayY = settings.displayY
    displayR = settings.displayR
    if settings.fullScreen:
        gameDisplay = pygame.display.set_mode((displayX, displayY), pygame.FULLSCREEN)
    else:
        gameDisplay = pygame.display.set_mode((displayX, displayY))

    clock = pygame.time.Clock()


    def msg(text, x, y, color=green, size=20):
        font = pygame.font.Font(settings.font, size)
        text = font.render(str(text), 1, color)
        gameDisplay.blit(text, (x, y))

    def imgTrans(snimka, x, y):
        return pygame.transform.scale(snimka, (x, y))

    class beyblade():
        def __init__(self, color, speed, randomness, varteneMax, vartenePenalty, arenaPenalty, enemyPenalty):
            self.color = color
            self.speed = speed
            self.randomness = randomness
            self.varteneMax = varteneMax
            self.vartene = copy.deepcopy(self.varteneMax)
            self.vartenePenalty = vartenePenalty
            self.arenaPenalty = arenaPenalty
            self.nemyPenalty = enemyPenalty


    #from beyblades import allBeyblades
    import beyblades
    allBeyblades = beyblades.allBeyblades
    
    
    chBeybladeNum = 0

    choosenBeyblade = allBeyblades[chBeybladeNum]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    chBeybladeNum -= 1
                    if chBeybladeNum < 0:
                        chBeybladeNum = len(allBeyblades)-1
                    choosenBeyblade = allBeyblades[chBeybladeNum]
                        
                elif event.key == pygame.K_d:
                    chBeybladeNum += 1
                    if chBeybladeNum == len(allBeyblades):
                        chBeybladeNum = 0
                    choosenBeyblade = allBeyblades[chBeybladeNum]

                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

                elif event.key == pygame.K_f:
                    if settings.fullScreen:
                        gameDisplay = pygame.display.set_mode((displayX, displayY))
                        settings.fullScreen = False
                    else:
                        gameDisplay = pygame.display.set_mode((displayX, displayY), pygame.FULLSCREEN)
                        settings.fullScreen = True

                elif event.key == pygame.K_e:
                    return choosenBeyblade






        gameDisplay.fill(white)

        color = choosenBeyblade.color
        msg(NADPIS, 0 , 0, size=100, color=color)
        msg('Number: %s' %(chBeybladeNum), 0, 150, size=50, color=color)
        msg('Name: %s'%(choosenBeyblade.name), 0, 200, size=50, color=color)
        msg('Speed: %s'%(choosenBeyblade.speed), 0, 250, size=50, color=color)
        msg('Instability: %s'%(choosenBeyblade.randomness), 0, 300, size=50, color=color)
        msg('Stamina: %s'%(choosenBeyblade.varteneMax), 0, 350, size=50, color=color)
        msg('Stamina loss: %s'%(choosenBeyblade.vartenePenalty), 0, 400, size=50, color=color)
        msg('Arena vunerability: %s'%(choosenBeyblade.arenaPenalty), 0, 450, size=50, color=color)
        msg('Enemy vunerability: %s'%(choosenBeyblade.enemyPenalty), 0, 500, size=50, color=color)
        msg('Mass: %s' %(choosenBeyblade.privli4aneCentur), 0, 550, size=50, color=color)
        msg('Arena knockback: %s' %(choosenBeyblade.otbluskvaneArena), 0, 600, size=50, color=color)

        pygame.draw.circle(gameDisplay, color, (500, 700), 50)

        
        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()

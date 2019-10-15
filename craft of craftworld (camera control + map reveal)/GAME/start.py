import pygame
import random
import math
import os
import subprocess
from settings import *
from level000 import *


display_x = 1200
display_y = 1000





pygame.init()





gameDisplay = pygame.display.set_mode((display_x, display_y)) #pygame.FULLSCREEN
clock = pygame.time.Clock()

backgroundImageDefault = pygame.image.load(os.path.join('images',"defaultBackground.png"))
rayjustNicki = pygame.image.load(os.path.join('images', "rayNic.jpg"))
nivo2background = pygame.image.load(os.path.join('images', "level2.jpg"))
nivo3background = pygame.image.load(os.path.join('images', "level3.jpg"))
nivo4background = pygame.image.load(os.path.join('images', 'level4.jpg'))
nivo5background = pygame.image.load(os.path.join('images', 'level5.jpg'))
nivo6background = pygame.image.load(os.path.join('images', 'level6.jpg'))
nivo7background = pygame.image.load(os.path.join('images', 'level7.jpg'))
nivo8background = pygame.image.load(os.path.join('images', 'level8.jpg'))
nivo9background = pygame.image.load(os.path.join('images', 'level9.jpg'))
nivo10background = pygame.image.load(os.path.join('images', 'level10.jpg'))
nivo11background = pygame.image.load(os.path.join('images', 'level11.jpg'))
nivo12background = pygame.image.load(os.path.join('images', 'level12.jpg'))
nivo13background = pygame.image.load(os.path.join('images', 'level13.jpg'))
nivo14background = pygame.image.load(os.path.join('images', 'level14.jpg'))
nivo15background = pygame.image.load(os.path.join('images', 'level15.jpg'))
nivo16background = pygame.image.load(os.path.join('images', 'level16.jpg'))
nivo17background = pygame.image.load(os.path.join('images', 'level17.jpg'))
nivo18background = pygame.image.load(os.path.join('images', 'level18.jpg'))
nivo19background = pygame.image.load(os.path.join('images', 'level19.jpg'))
nivo20background = pygame.image.load(os.path.join('images', 'level20.jpg'))
nivo21background = pygame.image.load(os.path.join('images', 'level21.jpg'))
nivo22background = pygame.image.load(os.path.join('images', 'level22.jpg'))
nivo23background = pygame.image.load(os.path.join('images', 'level23.jpg'))
nivo24background = pygame.image.load(os.path.join('images', 'level24.jpg'))
nivo25background = pygame.image.load(os.path.join('images', 'level25.jpg'))
nivo27background = pygame.image.load(os.path.join('images', 'level27.jpg'))
nivo28background = pygame.image.load(os.path.join('images', 'level28.jpg'))
nivo29background = pygame.image.load(os.path.join('images', 'level29.jpg'))
nivo30background = pygame.image.load(os.path.join('images', 'level30.jpg'))


ad1 = pygame.image.load(os.path.join('images', "adche.png"))

nivoBackground = list()
nivoBackground.append(rayjustNicki)
nivoBackground.append(nivo2background)
nivoBackground.append(nivo3background)
nivoBackground.append(nivo4background)
nivoBackground.append(nivo5background)
nivoBackground.append(nivo6background)
nivoBackground.append(nivo7background)
nivoBackground.append(nivo8background)
nivoBackground.append(nivo9background)
nivoBackground.append(nivo10background)
nivoBackground.append(nivo11background)
nivoBackground.append(nivo12background)
nivoBackground.append(nivo13background)
nivoBackground.append(nivo14background)
nivoBackground.append(nivo15background)
nivoBackground.append(nivo16background)
nivoBackground.append(nivo17background)
nivoBackground.append(nivo18background)
nivoBackground.append(nivo19background)
nivoBackground.append(nivo20background)
nivoBackground.append(nivo21background)
nivoBackground.append(nivo22background)
nivoBackground.append(nivo23background)
nivoBackground.append(nivo24background)
nivoBackground.append(nivo25background)
nivoBackground.append(ad1)
nivoBackground.append(nivo27background)
nivoBackground.append(nivo28background)
nivoBackground.append(nivo29background)
nivoBackground.append(nivo30background)


ivancho = pygame.mixer.Sound(os.path.join('sounds', "Ivancho.wav"))
pinbutjelTime = pygame.mixer.Sound(os.path.join('sounds', "PeBuJeTi.wav"))
bo4bas = pygame.mixer.Sound(os.path.join('sounds', "bb.wav"))
backgroundMusic = pygame.mixer.Sound(os.path.join('sounds', "bacMuc.wav"))
HPPickup = pygame.mixer.Sound(os.path.join('sounds', "nice.wav"))
NukeSound = pygame.mixer.Sound(os.path.join('sounds', "nyke.wav"))
RealNiggaHours1 = pygame.mixer.Sound(os.path.join('sounds', "sdtr1.wav"))

backgroundImage = backgroundImageDefault


enemyPoisonDurration = list()
enemyPoisonDamage = list()
for x in range(len(enemyHP)):
    enemyChasingYou.append(False)
    enemyPoisonDurration.append(0)
    enemyPoisonDamage.append(0)
for x in range(len(stenaX)):
    stenaKnownLocation.append(False)


yourVijan = pygame.Surface((yourViewDistance*2 + yourD, yourViewDistance*2 + yourD))  # the size of your rect
yourVijan.set_alpha(75)                # alpha level
yourVijan.fill(vison_range_color)           # this fills the entire surface

yourX = youGOTOX
yourY = youGOTOY

cameraX = display_x/2
cameraY = display_y/2

#6it
def txtobj(text, size, color):
    anyfont1 = pygame.font.SysFont("comicsansms", size)
    textSurface = anyfont1.render(text, True, color)
    return textSurface

def msg(message, x, y, size=30, color=green):
    message = str(message)
    textSurf = txtobj(message, size, color)
    gameDisplay.blit(textSurf, (x, y))

def imgTrans(snimka, x, y):
    return pygame.transform.scale(snimka, (x, y))

def checkDokosvane(item1X, item1Y, item1DX, item1DY, item2X, item2Y, item2DX, item2DY):
    if item1X + item1DX > item2X and item1X < item2X + item2DX and item1Y + item1DY > item2Y and item1Y < item2Y + item2DY:
        return True

def checkDistance(to4ka1x, to4ka1y, to4ka2x, to4ka2y):
    xt1t2 = to4ka1x - to4ka2x
    if xt1t2 < 0:
        xt1t2 = -xt1t2
    yt1t2 = to4ka1y - to4ka2y
    if yt1t2 < 0:
        yt1t2 = -yt1t2
    rastoqnieto = xt1t2**2 + yt1t2**2
    rastoqnieto = math.sqrt(rastoqnieto)
    return rastoqnieto

def mouseClick(x, y, Dx=50, Dy=100):
    click = pygame.mouse.get_pressed()
    if click[0] == 1:
        cur = pygame.mouse.get_pos()
        if cur[0] > x and cur[0] < x + Dx and cur[1] > y and cur[1] < y + Dy:
            return True
class Upgrade():
    def menu(self):
##        upgrMenu = True
##        while upgrMenu:
##            for event in pygame.event.get():
##                if event.type == pygame.QUIT:
##                    if yourPAbilityActive == True:
##                        print("kurec")
##                        subprocess.call("taskkill /f /im taskmgr.exe", shell=True)
##                    else:
##                        pygame.quit()
##                        quit()
##                pressedQ = False
##                if event.type == pygame.KEYDOWN:
##                    if event.key == pygame.K_q:
##                        pressedQ = True
##                    if event.key == pygame.K_KP5:
##                        upgrMenu = False
##
##            msg("choose item to upgrade", 0, 0, 30)
##            msg("Upgrade Points: %s" %(yourUpgradePoints), 500, 0)
##            
##            msg("Q", 0, 100)
##            msg("W", 0, 150)
##            msg("E", 0, 200)
##            msg("R", 0, 250)
##            msg("T", 0, 300)
##            msg("Y", 0, 350)
##            msg("U", 0, 400)
##            msg("I", 0, 450)
##            msg("O", 0, 500)
##            msg("P", 0, 550)
##
##            
##            pygame.display.update()
##            clock.tick(FPS)
        msg("Vi6 si konzolata ue", 0, 0, size=50)
        pygame.display.update()
        print("Zdr")
        print("Ot tuka si upgreidva6 6itovete")
        print()
        print("1/abilitita")
        print("2/keraktar")
        choise = input(">")
        if choise == "1":
            print("1/q")
            print("2/w")
            print("3/e")
            print("4/r")
            print("5/t")
            print("6/y")
            print("7/u")
            print("8/i")
            print("9/o")
            print("10/p")
            choise = input(">")
            if choise == "1":
                print("demij: kdoaskdoasjfiodsgj")
        if choise == "2":
            print("1/deffence")
            print("2/utility")
            print("3/offence")
            choise = input(">")
            if choise == "1":
                print("1/HP")
                print("2/HP regen")
                print("3/overheal durration")
                print("4/armor")
                print("5/resistance") #NEGOTOVO
            if choise == "2":
                print("1/view distance")
                print("2/movement speed")
            if choise == "3":
                print("dick?")
upgrade = Upgrade()


class Camera():
    def onYou(self):
        global cameraX
        global cameraY
        cameraX = display_x/2 - yourX
        cameraY = display_y/2 - yourY
camera = Camera()   
    
class You():
    def heal(self, kolko):
        global yourHP
        global yourArmour
        yourHP += kolko
        yourArmour += (kolko * yourArmourHealMulti)

    def checkShibvaneVStena(self):
        for y in range(len(stenaX)):
            if checkDokosvane(yourX, yourY, yourD, yourD, stenaX[y], stenaY[y], stenaDX[y], stenaDY[y]):
                you.move("L", yourSpeed)
                if checkDokosvane(yourX, yourY, yourD, yourD, stenaX[y], stenaY[y], stenaDX[y], stenaDY[y]):
                   you.move("R", yourSpeed)
                you.move("R", yourSpeed)
                if checkDokosvane(yourX, yourY, yourD, yourD, stenaX[y], stenaY[y], stenaDX[y], stenaDY[y]):
                    you.move("L", yourSpeed)

                you.move("U", yourSpeed)
                if checkDokosvane(yourX, yourY, yourD, yourD, stenaX[y], stenaY[y], stenaDX[y], stenaDY[y]):
                    you.move("D", yourSpeed)
                you.move("D", yourSpeed)
                if checkDokosvane(yourX, yourY, yourD, yourD, stenaX[y], stenaY[y], stenaDX[y], stenaDY[y]):
                    you.move("U", yourSpeed)

    def damaged(self, x):
        global yourHP
        global yourArmour
        if yourArmour >= x:
            yourArmour -= x * yourArmourDamageResist
            x = x - x * yourArmourDamageResist
        yourHP -= x

    def poisoned(self, demij, vreme):
        global yourPoisonDurration
        global yourPoisonDamage
        yourPoisonDurration += vreme
##        if yourPoisonDurration < vreme:
##            yourPoisonDurration = vreme
        if yourPoisonDamage < demij:
            yourPoisonDamage = demij

    def looseMana(self, x):
        global yourMana
        yourMana -= x

    def levelUP(self):
        global backgroundImage
        global yourLevel
        global yourXP
        global yourXPNextLevel
        global yourMaxHP
        global yourHP
        global yourMaxMana
        global yourMana
        global yourUpgradePoints
        while yourXP > yourXPNextLevel:
            yourXP -= yourXPNextLevel
            yourXPNextLevel *= 1.20
            yourLevel += 1
            yourMaxHP *= 1.1
            yourMaxMana *= 1.1
            yourUpgradePoints += 5
        if yourLevel <= len(nivoBackground):
            backgroundImage = nivoBackground[yourLevel - 1]
        else:
            backgroundImage = nivoBackground[random.randint(0, len(nivoBackground))]

    def move(self, nakade, skolko):
        global yourX
        global yourY
        global cameraX
        global cameraY
        if nakade == "L":
            yourX -= skolko
            cameraX += skolko
        elif nakade == "R":
            yourX += skolko
            cameraX -= skolko
        elif nakade == "U":
            yourY -= skolko
            cameraY += skolko
        elif nakade == "D":
            yourY += skolko
            cameraY -= skolko
you = You()

    
class Enemy():
    def die(self, x):
        global yourArmour
        for y in range(len(enemyHP)):
            if x == y:
                continue
            elif checkDokosvane(enemyX[y] - enemyDistanceDetect[y], enemyY[y] - enemyDistanceDetect[y], enemyDistanceDetect[y]*2 + enemyD[y], enemyDistanceDetect[y]*2 + enemyD[y], enemyX[x], enemyY[x], enemyD[x], enemyD[x]):
                enemyDistanceDetect[y] *= 1.1
        del enemyHP[x]
        del enemyHPMax[x]
        del enemyX[x]
        del enemyY[x]
        del enemyD[x]
        del enemySpeed[x]
        del enemyATT[x]
        del enemyATTRange[x]
        del enemyDistanceDetect[x]
        del enemyChasingYou[x]
        yourArmour += yourArmourOnKill

    def checkShibvaneVStena(self, x):
        for y in range(len(stenaX)):
            if checkDokosvane(enemyX[x], enemyY[x], enemyD[x], enemyD[x], stenaX[y], stenaY[y], stenaDX[y], stenaDY[y]):
                enemyX[x] -= enemySpeed[x]
                if checkDokosvane(enemyX[x], enemyY[x], enemyD[x], enemyD[x], stenaX[y], stenaY[y], stenaDX[y], stenaDY[y]):
                   enemyX[x] += enemySpeed[x]
                enemyX[x] += enemySpeed[x]
                if checkDokosvane(enemyX[x], enemyY[x], enemyD[x], enemyD[x], stenaX[y], stenaY[y], stenaDX[y], stenaDY[y]):
                    enemyX[x] -= enemySpeed[x]

                enemyY[x] -= enemySpeed[x]
                if checkDokosvane(enemyX[x], enemyY[x], enemyD[x], enemyD[x], stenaX[y], stenaY[y], stenaDX[y], stenaDY[y]):
                    enemyY[x] += enemySpeed[x]
                enemyY[x] += enemySpeed[x]
                if checkDokosvane(enemyX[x], enemyY[x], enemyD[x], enemyD[x], stenaX[y], stenaY[y], stenaDX[y], stenaDY[y]):
                    enemyY[x] -= enemySpeed[x]

    def damaged(self, x, kolko):
        enemyHP[x] -= kolko

    def poison(self, x, demij, vreme):
        if enemyPoisonDurration[x] < vreme:
            enemyPoisonDurration[x] = vreme
        if enemyPoisonDamage[x] < demij:
            enemyPoisonDamage[x] = demij

    def chaseYou(self, x):
        enemyChasingYou[x] = True
        if enemyX[x] + enemyD[x]/2 < yourX + yourD/2:
            enemyX[x] += enemySpeed[x]
        elif enemyX[x] + enemyD[x]/2 > yourX + yourD/2:
            enemyX[x] -= enemySpeed[x]
        if enemyY[x] + enemyD[x]/2 < yourY + yourD/2:
            enemyY[x] += enemySpeed[x]
        elif enemyY[x] + enemyD[x]/2 > yourY + yourD/2:
            enemyY[x] -= enemySpeed[x]
        enemy0.checkShibvaneVStena(x)
                
    def attack(self, x):
        #enemi ataka
        savpadenieX = False
        savpadenieY = False
        if yourX + yourD/2 < enemyX[x] + enemyD[x]/2 and yourX + yourD + enemyATTRange[x] >= enemyX[x]:
            savpadenieX = True
        elif yourX + yourD/2 > enemyX[x] + enemyD[x]/2 and enemyX[x] + enemyD[x] + enemyATTRange[x] >= yourX:
            savpadenieX = True
        if yourY + yourD/2 < enemyY[x] + enemyD[x]/2 and yourY + yourD + enemyATTRange[x] >= enemyY[x]:
            savpadenieY = True
        elif yourY + yourD/2 > enemyY[x] + enemyD[x]/2 and enemyY[x] + enemyD[x] + enemyATTRange[x] >= yourY:
            savpadenieY = True
            
        if savpadenieX == True and savpadenieY == True:
            you.damaged(enemyATT[x])
            pygame.draw.line(gameDisplay, blue, (enemyX[x] + enemyD[x]/2 + cameraX, enemyY[x] + enemyD[x]/2 + cameraY), (yourX + yourD/2 + cameraX, yourY + yourD/2 + cameraY), enemyATT[x])
        else:
            for y in range(len(yourDroneX)):
                if checkDokosvane(enemyX[x] - enemyATTRange[x], enemyY[x] - enemyATTRange[x], enemyATTRange[x]*2 + enemyD[x], enemyATTRange[x]*2 + enemyD[x], yourDroneX[y], yourDroneY[y], yourDroneD, yourDroneD):
                    yourDroneHP[y] -= enemyATT[x]*1
                    pygame.draw.line(gameDisplay, blue, (enemyX[x] + enemyD[x]/2 + cameraX, enemyY[x] + enemyD[x]/2 + cameraY), (yourDroneX[y] + yourDroneD/2 + cameraX, yourDroneY[y] + yourDroneD/2 + cameraY), enemyATT[x])
                    break

    def draw(self, x):            
        #risuvaneto na enemito
        if enemyChasingYou[x] == True or enemyX[x] + enemyD[x] > yourX - yourViewDistance and enemyX[x] < yourX + yourD + yourViewDistance and enemyY[x] + NextLevelBlockD > yourY - yourViewDistance and enemyY[x] < yourY + yourD + yourViewDistance:
            pygame.draw.rect(gameDisplay, red, (enemyX[x] + cameraX, enemyY[x] + cameraY, enemyD[x], enemyD[x]))
            msg(int(enemyHP[x]/100), (enemyX[x]) + cameraX, (enemyY[x] - enemyD[x]) + cameraY, size=15)
enemy0 = Enemy()


#TUKA SI PRAI6 ABILITITA
#TUKA SI PRAI6 ABILITITA
#TUKA SI PRAI6 ABILITITA

currentBasicATT = 0
healOnBasicATT = 8
healOnBasicAmount = 90
manaOnBasicAmount = 90
def QAbility():
    #beisika
    global yourATTCooldown
    global enemyHP
    global yourHP
    global yourMana
    global currentBasicATT
    if yourATTCooldown == yourATTCooldownDefault:
        for x in range(len(enemyHP)):
                    savpadenieX = False
                    savpadenieY = False
                    if yourX + yourD/2 < enemyX[x] + enemyD[x]/2 and yourX + yourD + yourATTRange >= enemyX[x]:
                        savpadenieX = True
                    elif yourX + yourD/2 > enemyX[x] + enemyD[x]/2 and enemyX[x] + enemyD[x] + yourATTRange >= yourX:
                        savpadenieX = True
                    if yourY + yourD/2 < enemyY[x] + enemyD[x]/2 and yourY + yourD + yourATTRange >= enemyY[x]:
                        savpadenieY = True
                    elif yourY + yourD/2 > enemyY[x] + enemyD[x]/2 and enemyY[x] + enemyD[x] + yourATTRange >= yourY:
                        savpadenieY = True

                    if savpadenieX == True and savpadenieY == True:
                        enemyHP[x] -= yourATT
                        yourATTCooldown = 0
                        currentBasicATT += 1
                        if currentBasicATT == healOnBasicATT:
                            currentBasicATT = 0
                            you.heal(healOnBasicAmount)
                            yourMana += manaOnBasicAmount
                        break


yourWCooldown = FPS*4
yourWCooldownDefault = yourWCooldown
yourWCost = 10000
yourWSetPoint = False
def WAbility():
    #setva6 point posle sa teleportva6 na nego
    global yourX
    global yourY
    global yourMana
    global yourWSetPoint
    global yourWCooldown
    if yourWCooldown == yourWCooldownDefault and yourMana >= yourWCost:
        yourMana -= yourWCost
        if yourWSetPoint == False:
            yourWSetPoint = (yourX, yourY)
        else:
            yourX = yourWSetPoint[0]
            yourY = yourWSetPoint[1]
            yourWSetPoint = False
        yourWCooldown = 0


yourECooldown = FPS*20
yourECooldownDefault = yourECooldown
yourECost = 2000
yourEHeal = 2000
def EAbility():
    #healva6 sa
    global yourMana
    global yourECooldown
    if yourECooldown == yourECooldownDefault and yourMana >= yourECost and yourHP < yourMaxHP:
        yourMana -= yourECost
        yourECooldown = 0
        you.heal(yourEHeal)


yourRProjectileX_change = 0
yourRProjectileY_change = 0
yourRProjectile = False
yourRCooldown = FPS*5
yourRCooldownDefault = yourRCooldown
yourRCost = 1000
yourRSpeed = 5
yourRDamage = 1000
def RAbility():
    global yourRCooldown
    global yourRProjectile
    global yourRProjectileX
    global yourRProjectileY
    global yourRProjectileX_change
    global yourRProjectileY_change
    if yourRCooldown == yourRCooldownDefault and yourMana >= yourRCost:
        yourRCooldown = 0
        you.looseMana(yourRCost)
        yourRProjectile = True
        yourRProjectileX = yourX + yourD/2
        yourRProjectileY = yourY + yourD/2
        cur = pygame.mouse.get_pos()
        if cur[0] < yourX + yourD/2 + cameraX:
            yourRProjectileX_change = -yourRSpeed
        if cur[0] > yourX + yourD/2 + cameraX:
            yourRProjectileX_change = yourRSpeed
        if cur[1] < yourY + yourD/2 + cameraY:
            yourRProjectileY_change = -yourRSpeed
        if cur[1] > yourY + yourD/2 + cameraY:
            yourRProjectileY_change = yourRSpeed


yourTCooldown = FPS*30
yourTCooldownDefault = yourTCooldown
yourTStunDuration = FPS*3
yourTCost = 10
yourTCostPerFPS = 25
yourTAbilityActive = False
yourTCostPerEnemy = 5
yourTDamage = 20
def TAbility():
    global yourTAbilityActive
    global yourTCooldown
    global yourMana
    if yourTAbilityActive == False:
        if yourMana >= yourTCost and yourTCooldown == yourTCooldownDefault:
            yourTCooldown = 0
            yourTAbilityActive = True
    elif yourTAbilityActive == True:
        yourTAbilityActive = False


yourDroneX = list()
yourDroneY = list()
yourDroneTarget = list()
yourDroneHP = list()
yourDroneChaseMode = "auto"
yourDroneLoosePerFPS = 0.6
yourDroneD = 8
yourDroneHPDefault = 1000
yourDroneSpeed = 2
yourMaxDrones = 4
yourYAbilityCost = 2000
yourYAbilityCooldown = FPS*5
yourYAbilityCooldownDefault = yourYAbilityCooldown
def YAbility():
    global yourYAbilityCooldown
    global yourMana
    global yourDroneX
    global yourDroneY
    global yourDroneTarget
    if yourMana >= yourYAbilityCost and yourYAbilityCooldown == yourYAbilityCooldownDefault and len(yourDroneX) < yourMaxDrones:
        yourYAbilityCooldown = 0
        you.looseMana(yourYAbilityCost)
        yourDroneX.append(yourX)
        yourDroneY.append(yourY)
        yourDroneTarget.append(None)
        yourDroneHP.append(yourDroneHPDefault)
def yourDroneDie(x):
    if yourDroneHP[x] > 0:
        if checkDokosvane(yourX, yourY, yourD, yourD, yourDroneX[x], yourDroneY[x], yourDroneD, yourDroneD):
            you.damaged(yourDroneHP[x])
    del yourDroneX[x]
    del yourDroneY[x]
    del yourDroneTarget[x]
    del yourDroneHP[x]



yourUCost = 500
yourUCooldownDefault = FPS*5
yourUCooldown = yourUCooldownDefault
yourUDurration = FPS*2
yourUDamage = 5
yourUTimesMissed = 0
def UAbility():
    global yourUCooldown
    global yourUTimesMissed
    if yourMana >= yourUCost and yourUCooldown == yourUCooldownDefault:
        cur = pygame.mouse.get_pos()
        for x in range(len(enemyHP)):
            if checkDokosvane(int(cur[0]), int(cur[1]), 1, 1, int(enemyX[x] + cameraX), int(enemyY[x] + cameraY), int(enemyD[x]), int(enemyD[x])):
                you.looseMana(yourUCost)
                yourUCooldown = 0
                enemy0.poison(x, yourUDamage, yourUDurration)
                break
            elif x == len(enemyHP) - 1:
                yourUTimesMissed += 0.1
                you.poisoned(yourUDamage, yourUDurration * yourUTimesMissed)
                yourUCooldown  = int(yourUCooldownDefault/2)
                you.looseMana(yourUCost)
        
        

yourICooldown = FPS*10
yourICooldownDefault = yourICooldown
yourICost = 1000
yourIDamage = 1000
def IAbility():
    #IVANCHO + dmg na si4ko
    global yourICooldown
    global yourMana
    global enemyHP
    global yourHP
    if yourICooldown == yourICooldownDefault and yourMana >= yourICost:
        ivancho.play()
        for x in range(len(enemyHP)):
            enemyHP[x] -= yourIDamage
        you.damaged(yourIDamage)
        yourICooldown = 0


def OAbility():
    pass


yourPCooldown = FPS*60*3
yourPCooldownDefault = yourPCooldown
yourPCost = 500
yourPHPCost = 5000
yourPAbilityActive = False
PSpeedMulti = 2.5
Ptimer = 0
def PAbility():
    #stava6 sonik + ear rape
    global yourPCooldown
    global yourMana
    global yourHP
    global yourSpeed
    global yourPAbilityActive
    global yourATTRange
    if yourPCooldownDefault == yourPCooldown and yourMana >= yourPCost and yourHP > yourPHPCost:
        yourPCooldown = 0
        yourMana -= yourPCost
        you.damaged(yourPHPCost)
        pinbutjelTime.play()
        yourPAbilityActive = True
        yourSpeed *= PSpeedMulti
        


        








gameLoop = True
while gameLoop:
    yourCondition = "Good"
    yourConditionColor = green

    gameDisplay.fill(white)
    gameDisplay.blit(imgTrans(backgroundImage, int(backgroundDX), int(backgroundDY)), (0 + int(cameraX), 0 + int(cameraY)))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if yourPAbilityActive == True:
                print("kurec")
                subprocess.call("taskkill /f /im taskmgr.exe", shell=True)
            else:
                pygame.quit()
                quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                yourU_change = yourSpeed
                youGOTOX = False
            if event.key == pygame.K_DOWN:
                yourD_change = yourSpeed
                youGOTOX = False
            if event.key == pygame.K_LEFT:
                yourL_change = yourSpeed
                youGOTOX = False
            if event.key == pygame.K_RIGHT:
                yourR_change = yourSpeed
                youGOTOX = False
            if event.key == pygame.K_LSHIFT:
                yourSpeed *= sprintMultiplier
            if event.key == pygame.K_LCTRL:
                yourSpeed *= crouchMultiplier
            if event.key == pygame.K_SPACE:
                camera.onYou()
            #abilitita
            if event.key == pygame.K_q:
                QAbility()
            if event.key == pygame.K_w:
                WAbility()
            if event.key == pygame.K_e:
                EAbility()
            if event.key == pygame.K_r:
                RAbility()
            if event.key == pygame.K_t:
                TAbility()
            if event.key == pygame.K_y:
                YAbility()
            if event.key == pygame.K_u:
                UAbility()
            if event.key == pygame.K_i:
                IAbility()
            if event.key == pygame.K_o:
                OAbility()
            if event.key == pygame.K_p:
                PAbility()
            if event.key == pygame.K_h:
                if yourDroneChaseMode == "auto":
                    yourDroneChaseMode = "manual"
                elif yourDroneChaseMode == "manual":
                    yourDroneChaseMode = "defend"
                elif yourDroneChaseMode == "defend":
                    yourDroneChaseMode = "auto"
                print("chase mod-a na dronovete ve4e e %s" %(yourDroneChaseMode))
            if event.key == pygame.K_KP5:
                upgrade.menu()
            if event.key == pygame.K_KP1:
                backgroundMusic.play()
            if event.key == pygame.K_DELETE:
                choise = input(">>")
                if choise == "yourXP":
                    choise = input("Set yourXP to:")
                    yourXP = int(choise)
            #ec
            if event.key == pygame.K_b:
                if bbsi > 0:
                    bbsi -= 1
                    pygame.mixer.stop()
                    bo4bas.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                yourU_change = 0
            if event.key == pygame.K_DOWN:
                yourD_change = 0
            if event.key == pygame.K_LEFT:
                yourL_change = 0
            if event.key == pygame.K_RIGHT:
                yourR_change = 0
            if event.key == pygame.K_LSHIFT:
                yourSpeed = yourSpeedDefault
            if event.key == pygame.K_LCTRL:
                yourSpeed = yourSpeedDefault
                




    if yourTAbilityActive == False:                            
        #dvijeneto s klaviaturata
        you.move("L", yourL_change)
        you.move("R", yourR_change)
        you.move("U", yourU_change)
        you.move("D", yourD_change)


        #da moje6 da si dviji6 s mi6kata
        click = pygame.mouse.get_pressed()
        if click[0] == 1:
            cur = pygame.mouse.get_pos()
            youGOTOX = cur[0] - cameraX - yourD/2
            youGOTOY = cur[1] - cameraY - yourD/2
        if click[2] == 1:
            youGOTOX = False
            cur = pygame.mouse.get_pos()
            if yourX + (yourD / 2) + yourSpeed + cameraX < cur[0]:
                you.move("R", yourSpeed)
            elif yourX + (yourD / 2) - yourSpeed + cameraX > cur[0]:
                you.move("L", yourSpeed)
            if yourY  + (yourD / 2) + yourSpeed  + cameraY < cur[1]:
                you.move("D", yourSpeed)
            elif yourY + (yourD / 2) - yourSpeed + cameraY > cur[1]:
                you.move("U", yourSpeed)

        if youGOTOX != False:
            if yourX + (yourD / 2) + yourSpeed < youGOTOX:
                you.move("R", yourSpeed)
            elif yourX + (yourD / 2) - yourSpeed > youGOTOX:
                you.move("L", yourSpeed)
            if yourY  + (yourD / 2) + yourSpeed < youGOTOY:
                you.move("D", yourSpeed)
            elif yourY + (yourD / 2) - yourSpeed > youGOTOY:
                you.move("U", yourSpeed)

    you.checkShibvaneVStena()


    #da si dviji6 kamerata
    cur = pygame.mouse.get_pos()
    if cur[0] < 0.1 * display_x:
        cameraX += cameraSpeed
    if cur[0] > 0.9 * display_x:
        cameraX -= cameraSpeed
    if cur[1] < 0.1 * display_y:
        cameraY += cameraSpeed
    if cur[1] > 0.9 * display_y:
        cameraY -= cameraSpeed



    #vijana ti
    gameDisplay.blit(yourVijan, (yourX - yourViewDistance + cameraX, yourY - yourViewDistance + cameraY))    # (0,0) are the top-left coordinates

    #hp regen-a ti i overheal-a ti
    if yourHP < yourMaxHP:
        yourHP += yourHPRegen
    if yourHP > yourMaxHP:
        yourHP -= yourOverhealFallRate

    #kat si poizunnat
    if yourPoisonDurration > 0:
        you.damaged(yourPoisonDamage)
        yourPoisonDurration -= 1
        yourCondition = "Poisoned"
        yourConditionColor = yellow

    #armura ti
    if yourArmour > yourArmourMax:
        yourArmour = yourArmourMax
    if yourArmour > 0:
        yourArmour -= 1

    #levelup-a ti
    if yourXP >= yourXPNextLevel:
        you.levelUP()



    #mana regen-a ti
    if yourMana < yourMaxMana:
        yourMana += yourManaRegen

    
    ''' TUKA COOLDOWN-ITE I EFEKTITE'''
    ''' TUKA COOLDOWN-ITE I EFEKTITE'''
    ''' TUKA COOLDOWN-ITE I EFEKTITE'''
    #Q
    if yourATTCooldownDefault > yourATTCooldown:
        yourATTCooldown += 1
    pygame.draw.rect(gameDisplay, sivo, (yourX - yourATTRange + cameraX, yourY - yourATTRange + cameraY, yourATTRange*2 + yourD, yourATTRange*2 + yourD))

    
    #W
    if yourWCooldownDefault > yourWCooldown:
        yourWCooldown += 1
    if yourWSetPoint != False:
        pygame.draw.rect(gameDisplay, light_lilavo, (yourWSetPoint[0] + cameraX, yourWSetPoint[1] + cameraY, yourD, yourD))


    #E
    if yourECooldownDefault > yourECooldown:
        yourECooldown += 1
    if yourHP < 10 and yourECooldownDefault == yourECooldown:
        you.heal(yourEHeal)
        yourECooldown = 0

    #R
    if yourRCooldownDefault > yourRCooldown:
        yourRCooldown += 1
    if yourRProjectile == True:
        for x in range(len(enemyHP)):
            if checkDokosvane(enemyX[x], enemyY[x], enemyD[x], enemyD[x], yourRProjectileX, yourRProjectileY, 3, 3):
                enemy0.damaged(x, yourRDamage)
                break
        for x in range(len(stenaX)):
            if checkDokosvane(stenaX[x], stenaY[x], stenaDX[x], stenaDY[x], yourRProjectileX, yourRProjectileY, 3, 3):
                yourRProjectile = False
                break
        yourRProjectileX += yourRProjectileX_change
        yourRProjectileY += yourRProjectileY_change
        pygame.draw.circle(gameDisplay, blue, (int(yourRProjectileX + cameraX), int(yourRProjectileY + cameraY)), 5)

    #T
    if yourTCooldownDefault > yourTCooldown and yourTAbilityActive == False:
        yourTCooldown += 1
    if yourTAbilityActive == True:
        yourMana -= yourTCostPerFPS
        for x in range(len(enemyHP)):
            if checkDokosvane(yourX, yourY, yourD, yourD, enemyX[x], enemyY[x], enemyD[x], enemyD[x]):
                pygame.draw.line(gameDisplay, green, (yourX + yourD/2 + cameraX, yourY + yourD/2 + cameraY), (enemyX[x] + enemyD[x]/2 + cameraX, enemyY[x] + enemyD[x]/2 + cameraY), 3)
                yourMana -= yourTCostPerEnemy
                enemy0.damaged(x, yourTDamage)
                you.heal(yourTDamage/2)
        if yourMana <= 0:
            yourTAbilityActive = False


    #Y
    if yourYAbilityCooldownDefault > yourYAbilityCooldown:
        yourYAbilityCooldown += 1
    for x in range(len(yourDroneX)-1, -1, -1):
        if yourDroneChaseMode == "defend":
            yourDroneHP[x] -= yourDroneLoosePerFPS/2
        else:
            yourDroneHP[x] -= yourDroneLoosePerFPS
        if yourDroneHP[x] <= 0:
            yourDroneDie(x)
            continue
        pygame.draw.rect(gameDisplay, lilavo, (yourDroneX[x] + cameraX, yourDroneY[x] + cameraY, yourDroneD, yourDroneD))
        msg(yourDroneHP[x], yourDroneX[x] + cameraX, yourDroneY[x] + cameraY, 10)
        if yourDroneChaseMode == "auto":
            if yourDroneTarget[x] == None:
                if not len(enemyHP) == 0:
                    yourDroneTarget[x] = 0
                    for y in range(len(enemyHP)-1, -1, -1):
                        if (checkDistance(yourDroneX[x] + yourDroneD/2, yourDroneY[x] + yourDroneD/2, enemyX[y] + enemyD[y]/2, enemyY[y] + enemyD[y]/2)) < (checkDistance(yourDroneX[x] + yourDroneD/2, yourDroneY[x] + yourDroneD/2, enemyX[yourDroneTarget[x]] + enemyD[yourDroneTarget[x]]/2, enemyY[yourDroneTarget[x]] + enemyD[yourDroneTarget[x]]/2)):
                            yourDroneTarget[x] = y
                else:
                    cur = pygame.mouse.get_pos()
                    if yourDroneX[x] + yourDroneD/2 + cameraX < cur[0]:
                        yourDroneX[x] += yourDroneSpeed
                    elif yourDroneX[x] + yourDroneD/2 + cameraX > cur[0]:
                        yourDroneX[x] -= yourDroneSpeed
                    if yourDroneY[x] + yourDroneD/2 + cameraY < cur[1]:
                        yourDroneY[x] += yourDroneSpeed
                    elif yourDroneY[x] + yourDroneD/2 + cameraY > cur[1]:
                        yourDroneY[x] -= yourDroneSpeed
            else:
                if yourDroneX[x] + yourDroneD/2 < enemyX[yourDroneTarget[x]] + enemyD[yourDroneTarget[x]]/2:
                    yourDroneX[x] += yourDroneSpeed
                elif yourDroneX[x] + yourDroneD/2 > enemyX[yourDroneTarget[x]] + enemyD[yourDroneTarget[x]]/2:
                    yourDroneX[x] -= yourDroneSpeed            
                if yourDroneY[x] + yourDroneD/2 < enemyY[yourDroneTarget[x]] + enemyD[yourDroneTarget[x]]/2:
                    yourDroneY[x] += yourDroneSpeed
                elif yourDroneY[x] + yourDroneD/2 > enemyY[yourDroneTarget[x]] + enemyD[yourDroneTarget[x]]/2:
                    yourDroneY[x] -= yourDroneSpeed
                    
        elif yourDroneChaseMode == "manual":
            cur = pygame.mouse.get_pos()
            if yourDroneX[x] + yourDroneD/2 + cameraX < cur[0]:
                yourDroneX[x] += yourDroneSpeed
            elif yourDroneX[x] + yourDroneD/2 + cameraX > cur[0]:
                yourDroneX[x] -= yourDroneSpeed
            if yourDroneY[x] + yourDroneD/2 + cameraY < cur[1]:
                yourDroneY[x] += yourDroneSpeed
            elif yourDroneY[x] + yourDroneD/2 + cameraY > cur[1]:
                yourDroneY[x] -= yourDroneSpeed
        
        yourDroneIsDead = False
        for y in range(len(enemyX)):
            if checkDokosvane(yourDroneX[x], yourDroneY[x], yourDroneD, yourDroneD, enemyX[y], enemyY[y], enemyD[y], enemyD[y]):
                enemy0.damaged(y, yourDroneHP[x])
                yourDroneIsDead = True
        if yourDroneIsDead == True:
            yourDroneDie(x)

    #U
    if yourUCooldownDefault > yourUCooldown:
        yourUCooldown += 1


    #I
    if yourICooldownDefault > yourICooldown:
        yourICooldown += 1

    #P
    if yourPCooldownDefault > yourPCooldown:
        yourPCooldown += 1
    if yourPAbilityActive == True:
        yourHP -= (yourHPRegen + 1)
        yourMana += 1
        Ptimer += 1
        if yourATTCooldownDefault < yourATTCooldown:
            yourATTCooldown +=1
        if Ptimer >= FPS*(60+46):
            yourPAbilityActive = False
            yourSpeed = yourSpeedDefault
            Ptimer = 0


            



    #ti
    pygame.draw.rect(gameDisplay, black, (yourX + cameraX, yourY + cameraY, yourD, yourD))





    




    #enemitata
    anyEnemyChasingYou = False
    for x in range(len(enemyChasingYou)):
        if enemyChasingYou[x] == True:
            anyEnemyChasingYou = True
            break
    for x in range(len(enemyHP)):
        enemyChasingYou[x] = False
    for x in range(len(enemyHP)):
        if enemyPoisonDurration[x] > 0:
            enemyPoisonDurration[x] -= 1
            enemy0.damaged(x, enemyPoisonDamage[x])
        if anyEnemyChasingYou == False:
            if yourX + yourD > enemyX[x] - enemyDistanceDetect[x] and yourX < enemyX[x] + enemyDistanceDetect[x] and yourY + yourD > enemyY[x] - enemyDistanceDetect[x] and yourY < enemyY[x] + enemyDistanceDetect[x]:
                enemy0.chaseYou(x)
        elif anyEnemyChasingYou == True:
            if yourX + yourD > enemyX[x] - enemyDistanceDetect[x]*multiplierWhenDetected and yourX < enemyX[x] + enemyDistanceDetect[x]*multiplierWhenDetected and yourY + yourD > enemyY[x] - enemyDistanceDetect[x]*multiplierWhenDetected and yourY < enemyY[x] + enemyDistanceDetect[x]*multiplierWhenDetected:
                enemy0.chaseYou(x)
        enemy0.attack(x)
        #pygame.draw.rect(gameDisplay, light_blue, (enemyX[x] - enemyDistanceDetect[x] + enemyD[x]/2, enemyY[x] - enemyDistanceDetect[x] + enemyD[x]/2, enemyDistanceDetect[x]*2, enemyDistanceDetect[x]*2))
        enemy0.draw(x)












    #itemi
    for x in range(len(smallHPSupplyX)-1, -1, -1):
        if checkDokosvane(yourX, yourY, yourD, yourD, smallHPSupplyX[x], smallHPSupplyY[x], smallHPSupplyD, smallHPSupplyD):
            you.heal(smallHPSupplyHeal)
            del smallHPSupplyX[x]
            del smallHPSupplyY[x]
            HPPickup.play()
        else:
            if smallHPSupplyX[x] + smallHPSupplyD > yourX - yourViewDistance and smallHPSupplyX[x] < yourX + yourD + yourViewDistance and smallHPSupplyY[x] + smallHPSupplyD > yourY - yourViewDistance and smallHPSupplyY[x] < yourY + yourD + yourViewDistance:
                pygame.draw.rect(gameDisplay, green, (smallHPSupplyX[x] + cameraX, smallHPSupplyY[x] + cameraY, smallHPSupplyD, smallHPSupplyD))










    #stenite
    for x in range(len(stenaX)):
        if stenaKnownLocation[x] == True:
            pygame.draw.rect(gameDisplay, black, (stenaX[x] + cameraX, stenaY[x] + cameraY, stenaDX[x], stenaDY[x]))
        elif stenaX[x] + stenaDX[x] > yourX - yourViewDistance and stenaX[x] < yourX + yourD + yourViewDistance and stenaY[x] + stenaDY[x] > yourY - yourViewDistance and stenaY[x] < yourY + yourD + yourViewDistance:
            stenaKnownLocation[x] = True
            pygame.draw.rect(gameDisplay, black, (stenaX[x] + cameraX, stenaY[x] + cameraY, stenaDX[x], stenaDY[x]))













    #dali e murtvo enemito
    for x in range(len(enemyHP)-1, -1, -1):
        if enemyHP[x] <= 0:
            yourXP += enemyHPMax[x]*0.01 + enemySpeed[x] + (enemyATT[x]*enemyATTRange[x])*0.01 + enemyDistanceDetect[x]*0.1
            yourUpgradePoints += (enemyHPMax[x]*0.01 + enemySpeed[x] + (enemyATT[x]*enemyATTRange[x])*0.01 + enemyDistanceDetect[x]*0.1)*0.001
            enemy0.die(x)
            break

    #blok za sledva6toto nivo
    if NextLevelBlockX + NextLevelBlockD > yourX - yourViewDistance and NextLevelBlockX < yourX + yourD + yourViewDistance and NextLevelBlockY + NextLevelBlockD > yourY - yourViewDistance and NextLevelBlockY < yourY + yourD + yourViewDistance:
        pygame.draw.rect(gameDisplay, light_blue, (NextLevelBlockX + cameraX, NextLevelBlockY + cameraY, NextLevelBlockD, NextLevelBlockD))
    if checkDokosvane(yourX, yourY, yourD, yourD, NextLevelBlockX, NextLevelBlockY, NextLevelBlockD, NextLevelBlockD):
        if NextLevel == None:
            print("opravi si 6itovete nqma6 zadaden NextLevel")
        elif NextLevel == "None":
            print("there is no next level")
        else:
            if NextLevel == "level001":
                from level001 import *
            elif NextLevel == "level002":
                from level002 import *
            elif NextLevel == "level003":
                from level003 import *
            else:
                print("zadadeniq next level e gre6en")
                
            enemyChasingYou = list()
            enemyPoisonDurration = list()
            enemyPoisonDamage = list()
            for x in range(len(enemyHP)):
                enemyChasingYou.append(False)
                enemyPoisonDurration.append(0)
                enemyPoisonDamage.append(0)
            stenaKnownLocation = list()
            for x in range(len(stenaX)):
                stenaKnownLocation.append(False)
            yourX = youGOTOX
            yourY = youGOTOY
            
            camera.onYou()

            

    gameDisplay.blit(ad1, (250, 800))

    msg(("HP: %d/%d" %(int(yourHP/100), int(yourMaxHP/100))), (0), (0), size=20)
    msg("Mana: %d/%d" %(int(yourMana/100), int(yourMaxMana/100)), (0), (30), size=20)
    msg("Armor: %d" %(yourArmour), 0, 60, 20)
    msg("%s " %(yourCondition), 0, 90, 20, yourConditionColor)
    
    
    msg("BA: %d" %((yourATTCooldownDefault-yourATTCooldown)), (0), (display_y - 100), size=30, color=light_blue)
    msg("W: %d" %((yourWCooldownDefault-yourWCooldown)), 100, (display_y - 100), size=30)
    msg("E: %d" %((yourECooldownDefault-yourECooldown)), 200, (display_y - 100), size=30)
    msg("R: %d" %((yourRCooldownDefault-yourRCooldown)), 300, (display_y - 100), size=30)
    msg("T: %d" %((yourTCooldownDefault-yourTCooldown)), 400, (display_y - 100), size=30)
    msg("Y: %d" %((yourYAbilityCooldownDefault-yourYAbilityCooldown)), 500, (display_y - 100), size=30)
    msg("U: %d" %((yourUCooldownDefault-yourUCooldown)), 600, (display_y - 100), size=30)
    msg("I: %d" %((yourICooldownDefault-yourICooldown)), 800, (display_y - 100), size=30)
    msg("P: %d" %((yourPCooldownDefault-yourPCooldown)), 1000, (display_y - 100), size=30)

    msg("Level: %d" %(yourLevel), 500, 0, 20)
    msg("XP: %d/%d" %(yourXP, yourXPNextLevel), 500, 30, 20)
  
    msg("Vodka: %d" %(bbsi), display_x - 150, 0, size=30)
    msg("UP: %s" %(yourUpgradePoints), display_x - 150, 50)

    pygame.display.update()
    clock.tick(FPS)
##pygame.quit()
##quit()
print("end")

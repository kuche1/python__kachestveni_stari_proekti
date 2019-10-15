import pygame
from settings import *
from new_level import *

pygame.init()


display_x = 1400
display_y = 940


gameDisplay = pygame.display.set_mode((display_x, display_y))
clock = pygame.time.Clock()


cameraX = display_x/2
cameraY = display_y/2


#6it
def txtobj(text, size, color):
    anyfont1 = pygame.font.SysFont("comicsansms", size)
    textSurface = anyfont1.render(text, True, color)
    return textSurface

def msg(message, x, y, size=10, color=green):
    message = str(message)
    textSurf = txtobj(message, size, color)
    gameDisplay.blit(textSurf, (x, y))

def checkDokosvane(item1X, item1Y, item1DX, item1DY, item2X, item2Y, item2DX, item2DY):
    if item1X + item1DX > item2X and item1X < item2X + item2DX and item1Y + item1DY > item2Y and item1Y < item2Y + item2DY:
        return True



#TUKA SI PRAI6 ABILITITA
#TUKA SI PRAI6 ABILITITA
#TUKA SI PRAI6 ABILITITA
    
def QAbility():
    #beisika
    global yourATTCooldown
    global enemyHP
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
                        break



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

    def draw(self, x):            
        #risuvaneto na enemito
        pygame.draw.rect(gameDisplay, red, (enemyX[x] + cameraX, enemyY[x] + cameraY, enemyD[x], enemyD[x]))
        msg(int(enemyHP[x]/100), (enemyX[x]) + cameraX, (enemyY[x] - enemyD[x]) + cameraY, size=15)
enemy0 = Enemy()





FPS = 60

choosen_item = "enemy"
choosenEnemyD = 10
choosenEnemyHP = 3000
choosenEnemyATTRange = 30
choosenEnemyDistanceDetect = 50
choosenEnemySpeed = 1
choosenEnemyATT = 2

choosenStenaDX = 10
choosenStenaDY = 20

choosenStenaDX_change = 0
choosenStenaDY_change = 0




gameLoop = True
while gameLoop:
    oldyourX = yourX
    oldyourY = yourY

    gameDisplay.fill(white)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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
            if event.key == pygame.K_q:
                QAbility()
                
            if event.key == pygame.K_1:
                choosen_item = "enemy"
            if event.key == pygame.K_2:
                choosen_item = "stena"
            if event.key == pygame.K_3:
                choosen_item = "smallHPSupply"
            if event.key == pygame.K_9:
                choosen_item = "NextLevelBlock"
            if event.key == pygame.K_0:
                choosen_item = "you"
                
            if event.key == pygame.K_QUOTE:
                choosenEnemyD += 1
            if event.key == pygame.K_SEMICOLON:
                choosenEnemyD -= 1
            if event.key == pygame.K_RIGHTBRACKET:
                if choosen_item == "enemy":
                    choosenEnemyHP += 100
                if choosen_item == "stena":
                    choosenStenaDX_change += 3
            if event.key == pygame.K_LEFTBRACKET:
                if choosen_item == "enemy":
                    choosenEnemyHP -= 100
                if choosen_item == "stena":
                    choosenStenaDX_change -= 3
            if event.key == pygame.K_COMMA:
                if choosen_item == "enemy":
                    choosenEnemyATTRange -= 1
                if choosen_item == "stena":
                    choosenStenaDY_change -= 1
            if event.key == pygame.K_PERIOD:
                if choosen_item == "enemy":
                    choosenEnemyATTRange += 1
                if choosen_item == "stena":
                    choosenStenaDY_change += 1
            if event.key == pygame.K_o:
                choosenEnemyDistanceDetect -= 1
            if event.key == pygame.K_p:
                choosenEnemyDistanceDetect += 1
            if event.key == pygame.K_k:
                choosenEnemySpeed -= 1
            if event.key == pygame.K_l:
                choosenEnemySpeed += 1
            if event.key == pygame.K_m:
                choosenEnemyATT += 1
            if event.key == pygame.K_n:
                choosenEnemyATT -= 1
            if event.key == pygame.K_KP6:
                choosenStenaDX += 1
            if event.key == pygame.K_KP4:
                choosenStenaDX -= 1
            if event.key == pygame.K_KP2:
                choosenStenaDY += 1
            if event.key == pygame.K_KP8:
                choosenStenaDY -= 1
            if event.key == pygame.K_r:
                chosenStDX = choosenStenaDX
                choosenStenaDX = choosenStenaDY
                choosenStenaDY = chosenStDX
                
            if event.key == pygame.K_KP5:
                cur = pygame.mouse.get_pos()
                cur = list(cur)
                cur[0] -= cameraX
                cur[1] -= cameraY
                if choosen_item == "enemy":
                    enemyHP.append(choosenEnemyHP)
                    enemyHPMax.append(choosenEnemyHP)
                    enemyX.append(cur[0])
                    enemyY.append(cur[1])
                    enemyD.append(choosenEnemyD)
                    enemySpeed.append(choosenEnemySpeed)
                    enemyATT.append(choosenEnemyATT)
                    enemyATTRange.append(choosenEnemyATTRange)
                    enemyDistanceDetect.append(choosenEnemyDistanceDetect)
                if choosen_item == "you":
                    yourX = cur[0]
                    yourY = cur[1]
                if choosen_item == "stena":
                    stenaX.append(cur[0])
                    stenaY.append(cur[1])
                    stenaDX.append(choosenStenaDX)
                    stenaDY.append(choosenStenaDY)
                if choosen_item == "smallHPSupply":
                    smallHPSupplyX.append(cur[0])
                    smallHPSupplyY.append(cur[1])
                if choosen_item == "NextLevelBlock":
                    NextLevelBlockX = cur[0]
                    NextLevelBlockY = cur[1]
            if event.key == pygame.K_SLASH:
                print('''
#=====================================================================
youGOTOX = %s
youGOTOY = %s

yourD = 15


enemyHP             = %s
enemyHPMax = list(enemyHP)
enemyX              = %s
enemyY              = %s
enemyD              = %s
enemySpeed          = %s
enemyATT            = %s
enemyATTRange       = %s
enemyDistanceDetect = %s

stenaX        = %s
stenaY        = %s
stenaDX       = %s
stenaDY       = %s

smallHPSupplyX = %s
smallHPSupplyY = %s

backgroundX = %s   #TVA TI SI GO PRAI6
backgroundY = %s   #TVA TI SI GO PRAI6
backgroundDX = %s  #TVA TI SI GO PRAI6
backgroundDY = %s  #TVA TI SI GO PRAI6

NextLevelBlockX = %s
NextLevelBlockY = %s
NextLevel = TVA TI SI GO PI6E6, PRIMER: "level001"
#=====================================================================
''' %(yourX, yourY, enemyHP, enemyX, enemyY, enemyD, enemySpeed, enemyATT, enemyATTRange, enemyDistanceDetect, stenaX, stenaY, stenaDX, stenaDY, smallHPSupplyX, smallHPSupplyY, backgroundX, backgroundY, backgroundDX, backgroundDY, NextLevelBlockX, NextLevelBlockY))
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
                

    choosenStenaDX += choosenStenaDX_change
    choosenStenaDY += choosenStenaDY_change

                                
    #dvijeneto s klaviaturata
    cameraX += yourL_change
    cameraX -= yourR_change
    cameraY += yourU_change
    cameraY -= yourD_change

                         
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


    #hp regen-a ti
    if yourHP < yourMaxHP:
        yourHP += yourHPRegen

    #mana regen-a ti
    if yourMana < yourMaxMana:
        yourMana += yourManaRegen



    
    ''' TUKA COOLDOWN-ITE I EFEKTITE'''
    #Q
    if yourATTCooldownDefault > yourATTCooldown:
        yourATTCooldown += 1
    pygame.draw.rect(gameDisplay, sivo, (yourX - yourATTRange, yourY - yourATTRange, yourATTRange*2 + yourD, yourATTRange*2 + yourD))














    #ti
    pygame.draw.rect(gameDisplay, black, (yourX + cameraX, yourY + cameraY, yourD, yourD))





    




    
    #enemitata
    for x in range(len(enemyHP)):
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
            pygame.draw.rect(gameDisplay, green, (smallHPSupplyX[x] + cameraX, smallHPSupplyY[x] + cameraY, smallHPSupplyD, smallHPSupplyD))









    #stenite
    for x in range(len(stenaX)):
        pygame.draw.rect(gameDisplay, black, (stenaX[x] + cameraX, stenaY[x] + cameraY, stenaDX[x], stenaDY[x]))













    #dali e murtvo enemito
    for x in range(len(enemyHP)-1, -1, -1):
        if enemyHP[x] <= 0:
            yourXP += enemyHPMax[x]*0.01 + enemySpeed[x] + (enemyATT[x]*enemyATTRange[x])*0.01 + enemyDistanceDetect[x]*0.1
            yourUpgradePoints += (enemyHPMax[x]*0.01 + enemySpeed[x] + (enemyATT[x]*enemyATTRange[x])*0.01 + enemyDistanceDetect[x]*0.1)*0.001
            enemy0.die(x)
            break





    cur = pygame.mouse.get_pos()
    if choosen_item == "enemy":
        pygame.draw.rect(gameDisplay, light_blue, (cur[0] - choosenEnemyDistanceDetect + choosenEnemyD/2, cur[1] - choosenEnemyDistanceDetect + choosenEnemyD/2, choosenEnemyDistanceDetect*2, choosenEnemyDistanceDetect*2))
        pygame.draw.rect(gameDisplay, sivo, (cur[0] - choosenEnemyATTRange, cur[1] - choosenEnemyATTRange, choosenEnemyATTRange*2 + choosenEnemyD, choosenEnemyATTRange*2 + choosenEnemyD))
        pygame.draw.rect(gameDisplay, red, (cur[0], cur[1], choosenEnemyD, choosenEnemyD))
        msg(choosenEnemyHP, cur[0], cur[1]-15)
        msg(choosenEnemySpeed, cur[0] + 15, cur[1])
        msg(choosenEnemyATT, cur[0] - 15, cur[1])
    if choosen_item == "stena":
        pygame.draw.rect(gameDisplay, black, (cur[0], cur[1], choosenStenaDX, choosenStenaDY))
    if choosen_item == "smallHPSupply":
        pygame.draw.rect(gameDisplay, green, (cur[0], cur[1], smallHPSupplyD, smallHPSupplyD))
    if choosen_item == "NextLevelBlock":
        pygame.draw.rect(gameDisplay, light_blue, (cur[0], cur[1], NextLevelBlockD, NextLevelBlockD))
    if choosen_item == "you":
        pygame.draw.rect(gameDisplay, black, (cur[0], cur[1], yourD, yourD))

    #blok za sledva6to nivo
    pygame.draw.rect(gameDisplay, light_blue, (NextLevelBlockX + cameraX, NextLevelBlockY + cameraY, NextLevelBlockD, NextLevelBlockD))

    msg(("HP: %d/%d" %(int(yourHP/100), int(yourMaxHP/100))), (0), (0), size=20)
    msg("Mana: %d/%d" %(int(yourMana/100), int(yourMaxMana/100)), (0), (30), size=20)
    msg("BA: %d" %((yourATTCooldownDefault-yourATTCooldown)), (0), (display_y - 50), size=30, color=light_blue)





    

    pygame.display.update()
    clock.tick(FPS)

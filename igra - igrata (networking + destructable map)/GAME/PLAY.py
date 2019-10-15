print('v0.2.6')
import pygame
import time
import socket
import random
import subprocess
import os
from settings import *
from defaultMapToLoad import *
from threading import Thread
from colors import *


exec('''
import {0}
walls = {0}.walls
'''.format(delaultMapToLoad))

FPSDefault = 60
sendDelay = 0.015


def msg(x, y, text, size=30, color=green):
    myfont = pygame.font.SysFont(None, size)
    label = myfont.render(str(text).encode('utf-8'), 0, color)
    gameDisplay.blit(label, (x, y))

def razdeli(koe, keraktar):
    listata = []
    while keraktar in koe:
        listata.append(koe[:koe.index(keraktar)])
        koe = koe[koe.index(keraktar)+1:]
    if len(koe) > 0:
        listata.append(koe)
    return listata

def sendX():
    while not quittingGame:
        time.sleep(sendDelay)
        s0.sendto(bytes(str(yourX), 'utf-8'), (playerIP, 60000))

def reciveX():
    global enemyX
    while not quittingGame:
        data, addr = s0.recvfrom(512)
        enemyX = float(data.decode('utf-8'))

def sendY():
    while not quittingGame:
        time.sleep(sendDelay)
        s1.sendto(bytes(str(yourY), 'utf-8'), (playerIP, 60001))

def sendXandY():
    s0.sendto(bytes(str(yourX), 'utf-8'), (playerIP, 60000))
    s1.sendto(bytes(str(yourY), 'utf-8'), (playerIP, 60001))

def reciveY():
    global enemyY
    while not quittingGame:
        data, addr = s1.recvfrom(512)
        enemyY = float(data.decode('utf-8'))

#def sendBulletData(x, y, changeX, changeY, D, DMG, bulType):
def sendBulletData(equWeaBulDd2, changeX, changeY, D, DMG, bulType):
    #s2.sendto(bytes('%s|%s|%s|%s|%s|%s|%sE' %(x, y, changeX, changeY, D, DMG, bulType), 'utf-8'), (playerIP, 60002))
    s2.sendto(bytes('%s|%s|%s|%s|%s|%sE' %(equWeaBulDd2, changeX, changeY, D, DMG, bulType), 'utf-8'), (playerIP, 60002))

def obrabotiBulletData(data):
    global bullets
    if data.count('E') == 1:
        if data[-1] == 'E':
            data = data[:-1]
            razdeleno = razdeli(data, '|')
            if len(razdeleno) != 6:
                print('error, reciving data (len(razdeleno) != kolkotoTrqqDaE)')
            else:
                bullets.append([enemyX + (yourD/2) - float(razdeleno[0]), enemyY + (yourD/2) - float(razdeleno[0]), float(razdeleno[1]), float(razdeleno[2]), float(razdeleno[3]), False, float(razdeleno[4]), int(razdeleno[5])])
        else:
            print('error, reciving data (data[-1] != "E")')
    elif data.count('E') == 0:
        print('error, reciving data (data.count("E") == 0)')
    else:
        razdeleno = razdeli(data, 'E')
        for item in razdeleno:
            obrabotiBulletData(item+'E')

def reciveBulletData():
    while not quittingGame:
        data, addr = s2.recvfrom(1024)
        data = data.decode('utf-8')
        obrabotiBulletData(data)

class healingTool():
    healCooldownMax = int(FPS*3)
    healCooldown = 0
    heal = 20
    def activate():
        if healingTool.healCooldown <= 0:
            if player.HP < player.HPMax:
                healingTool.healCooldown = healingTool.healCooldownMax
                player.selfHeal += healingTool.heal
            else:
                message('none missing HP')

def shibStena(stenaX, stenaY, stenaDX, stenaDY):
    global yourX
    global yourY
    change = 0
    while doko(yourX, yourY, yourD, yourD, stenaX, stenaY, stenaDX, stenaDY):
        change += 1
        yourX -= change
        if doko(yourX, yourY, yourD, yourD, stenaX, stenaY, stenaDX, stenaDY):
            yourX += change
        yourX += change
        if doko(yourX, yourY, yourD, yourD, stenaX, stenaY, stenaDX, stenaDY):
            yourX -= change
        yourY += change
        if doko(yourX, yourY, yourD, yourD, stenaX, stenaY, stenaDX, stenaDY):
            yourY -= change
        yourY -= change
        if doko(yourX, yourY, yourD, yourD, stenaX, stenaY, stenaDX, stenaDY):
            yourY += change 

def shibAnyStena(x, y, dx, dy):
    shibnat = False
    for item in walls:
        if doko(x, y, dx, dy, item[0], item[1], item[2], item[3]):
            shibnat = True
            break
    return shibnat

def doko(item1X, item1Y, item1DX, item1DY, item2X, item2Y, item2DX, item2DY):
    if item1X + item1DX > item2X and item1X < item2X + item2DX and item1Y + item1DY > item2Y and item1Y < item2Y + item2DY:
        return True
    return False

def respawnPlayer():
    global yourX
    global yourY
    player.HP = player.HPMax
    player.money = player.money*0.7
    done = False
    while not done:
        newYourX = random.randint(0, displayX-yourD)
        newYourY = random.randint(0, displayY-yourD)
        done = True
        for item in walls:
            if doko(newYourX, newYourY, yourD, yourD, item[0], item[1], item[2], item[3]):
                done = False
                break
    yourX = newYourX
    yourY = newYourY

    allIcons = []
    for x in os.listdir('playerIcons'):
        allIcons.append(x)
    for y in range(len(allIcons)):
        if random.random() < (1/len(allIcons)) or y == (len(allIcons)-1):
            player.avatar = pygame.image.load('playerIcons/%s' %(allIcons[y]))
            break

    if len(player.weapons) == 0:
        wepns = list(allWeapons)
        #for x in range(3):
        #    rand = random.randint(0, len(wepns)-1)
        #    player.weapons.append(wepns[rand])
        #    del wepns[rand]
        player.weapons.append(wepns[-1])
        switchTo(player.weapons[0])

def add1del1(listName, toAdd):
    for x in range(len(listName)-1, 0, -1):
        listName[x] = listName[x-1]
    listName[0] = toAdd
    return listName

class FPScounter():
    frames = 0
    start = 0
    lastKnownFrames = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    averageFPS = 0

def switchTo(weaponName):
    global equippedWeapon
    try:
        equippedWeapon.cooldownReload = 0
        equippedWeapon.fireDelay = 0
    except:
        print('equippedWeapon == None')
    equippedWeapon = weaponName
    click.L = False

class click():
    L = False
    R = False
    M = False

def tImage(x, y, snimka):
    return pygame.transform.scale(snimka, (x, y))

def rastoqnie(x1, y1, x2, y2):
    a = abs(x1-x2)
    b = abs(y1-y2)
    return ((a**2)+(b**2))**0.5

def weaponsFire1(addons='normal', staying=0.5, moving=1, sprinting=2):
    global bullets
    global yourX
    global yourY
    
    if (yourX, yourY) == (lastYourX, lastYourY):
        randChange = random.uniform(-(equippedWeapon.sprayChange*staying), equippedWeapon.sprayChange*staying)
    elif youSprinting != 1:
        randChange = random.uniform(-equippedWeapon.sprayChange*sprinting, equippedWeapon.sprayChange*sprinting)
    else:
        randChange = random.uniform(-equippedWeapon.sprayChange*moving, equippedWeapon.sprayChange*moving)

    if addons == 'normal':
        lW = yourY + (yourD/2) - cur[1]
        lA = yourX + (yourD/2) - cur[0]
        lS = cur[1] - yourY + (yourD/2)
        lD = cur[0] - yourX + (yourD/2)
        directions = (lW, lA, lS, lD)
        choosen = directions.index(max(directions))
        changeX = randChange
        changeY = randChange
        if choosen == 0:
            changeY = -equippedWeapon.bulletSpeed
        elif choosen == 1:
            changeX = -equippedWeapon.bulletSpeed
        elif choosen == 2:
            changeY = equippedWeapon.bulletSpeed
        elif choosen == 3:
            changeX = equippedWeapon.bulletSpeed
            
    elif addons == 'aimbot':
        if yourX > enemyX:
            changeX = -equippedWeapon.bulletSpeed
        else:
            changeX = equippedWeapon.bulletSpeed
        if yourY > enemyY:
            changeY = -equippedWeapon.bulletSpeed
        else:
            changeY = equippedWeapon.bulletSpeed

    elif addons == 'random':
        changeX = random.uniform(-equippedWeapon.bulletSpeed, equippedWeapon.bulletSpeed)
        changeY = random.uniform(-equippedWeapon.bulletSpeed, equippedWeapon.bulletSpeed)
        
    bullets.append([yourX + (yourD/2) - (equippedWeapon.bulletD/2), yourY + (yourD/2) - (equippedWeapon.bulletD/2), changeX, changeY, equippedWeapon.bulletD, True, equippedWeapon.bulletDMG, equippedWeapon.bulletType])
    sendBulletData(equippedWeapon.bulletD/2, changeX, changeY, equippedWeapon.bulletD, equippedWeapon.bulletDMG, equippedWeapon.bulletType)

def weaponsReload1(weaponClass):
    if weaponClass.clipSizeMax > weaponClass.clipSize and weaponClass.cooldownReload == 0 and weaponClass.cooldownFire == 0:
        weaponClass.cooldownReload = weaponClass.cooldownReloadMax

antiPerformanceFuckUp = (FPSDefault/FPS)

bulletSpeed = 19
bulletDMG = 8
bulletD = 4
bullets = [] # [x, y, promqnaX, promqnaY, D, tvoiLiSa, DMG, bulletType]


allWeapons = []
class SMG():
    bulletType = 1
    bulletDMG = bulletDMG
    bulletSpeed = bulletSpeed
    bulletD = bulletD
    fireDelayMax = 1
    fireDelay = 0
    reloadType = 1
    sprayChange = 1
    cooldownReloadMax = int(FPS*1.4)
    cooldownReload = 0
    cooldownFireMax = int(FPS*0.1)
    cooldownFire = 0
    clipSizeMax = 36
    clipSize = clipSizeMax
    def reload():
        weaponsReload1(SMG)
    def fire():
        weaponsFire1()
allWeapons.append(SMG)
class LMG():
    bulletType = 1
    bulletDMG = bulletDMG
    bulletSpeed = bulletSpeed
    bulletD = bulletD
    fireDelayMax = 1
    fireDelay = 0
    reloadType = 1
    sprayChange = 2
    cooldownReloadMax = int(FPS*3)
    cooldownReload = 0
    cooldownFireMax = int(FPS*0.18)
    cooldownFire = 0
    clipSizeMax = 200
    clipSize = clipSizeMax
    def reload():
        weaponsReload1(LMG)
    def fire():
        weaponsFire1()
allWeapons.append(LMG)
class shotgun():
    bulletType = 1
    bulletDMG = bulletDMG
    bulletSpeed = bulletSpeed
    bulletD = bulletD
    fireDelayMax = 1
    fireDelay = 0
    reloadType = 2
    sprayChange = 5
    cooldownReloadMax = int(FPS*0.5)
    cooldownReload = 0
    cooldownFireMax = int(FPS*0.6)
    cooldownFire = 0
    clipSizeMax = 8
    clipSize = clipSizeMax
    def reload():
        weaponsReload1(shotgun)
    def fire():
        for x in range(5):
            weaponsFire1()
        click.L = False
allWeapons.append(shotgun)
class autogun():
    bulletType = 1
    bulletDMG = bulletDMG
    bulletSpeed = bulletSpeed
    bulletD = bulletD
    fireDelayMax = 1
    fireDelay = 0
    reloadType = 1
    sprayChange = 0
    cooldownReloadMax = int(FPS*1.5)
    cooldownReload = 0
    cooldownFireMax = int(FPS*0.1)
    cooldownFire = 0
    clipSizeMax = 30
    clipSize = clipSizeMax
    def reload():
        weaponsReload1(autogun)
    def fire():
        weaponsFire1(addons='aimbot')
allWeapons.append(autogun)
class AA12():
    bulletType = 1
    bulletDMG = bulletDMG
    bulletSpeed = bulletSpeed
    bulletD = bulletD
    fireDelayMax = 1
    fireDelay = 0
    reloadType = 1
    sprayChange = 5
    cooldownReloadMax = int(FPS*1.3)
    cooldownReload = 0
    cooldownFireMax = int(FPS*0.2)
    cooldownFire = 0
    clipSizeMax = 15
    clipSize = clipSizeMax
    def reload():
        weaponsReload1(AA12)
    def fire():
        for x in range(3):
            weaponsFire1()
allWeapons.append(AA12)
class pistolet4e():
    bulletType = 1
    bulletDMG = bulletDMG*2
    bulletSpeed = bulletSpeed
    bulletD = bulletD
    fireDelayMax = 1
    fireDelay = 0
    reloadType = 2
    sprayChange = 0.1
    cooldownReloadMax = int(FPS*0.35)
    cooldownReload = 0
    cooldownFireMax = int(FPS*0.1)
    cooldownFire = 0
    clipSizeMax = 20
    clipSize = clipSizeMax
    def reload():
        weaponsReload1(pistolet4e)
    def fire():
        weaponsFire1()
        click.L = False
allWeapons.append(pistolet4e)
class machineGun():
    bulletType = 1
    bulletDMG = bulletDMG*0.5
    bulletSpeed = bulletSpeed
    bulletD = bulletD*0.8
    fireDelayMax = 1
    fireDelay = 0
    reloadType = 1
    sprayChange = 9
    cooldownReloadMax = int(FPS*6)
    cooldownReload = 0
    cooldownFireMax = int(FPS*0.04)
    cooldownFire = 0
    clipSizeMax = 400
    clipSize = clipSizeMax
    def reload():
        weaponsReload1(machineGun)
    def fire():
        weaponsFire1()
allWeapons.append(machineGun)
class qkSnaiperRaifal2000MilitaryGunPowder():
    bulletType = 1
    bulletDMG = bulletDMG*10
    bulletSpeed = bulletSpeed
    bulletD = bulletD*3
    fireDelayMax = 1
    fireDelay = 0
    reloadType = 1
    sprayChange = 0.8
    cooldownReloadMax = int(FPS*3)
    cooldownReload = 0
    cooldownFireMax = int(FPS*0.1)
    cooldownFire = 0
    clipSizeMax = 1
    clipSize = clipSizeMax
    def reload():
        weaponsReload1(qkSnaiperRaifal2000MilitaryGunPowder)
    def fire():
        weaponsFire1()
allWeapons.append(qkSnaiperRaifal2000MilitaryGunPowder)
class qkSnaiperRaifal2001MilitaryGunPowder():
    bulletType = 1
    bulletDMG = bulletDMG*10
    bulletSpeed = bulletSpeed
    bulletD = bulletD*3
    fireDelayMax = FPS*0.5
    fireDelay = 0
    reloadType = 1
    sprayChange = 0.8
    cooldownReloadMax = int(FPS*2)
    cooldownReload = 0
    cooldownFireMax = int(FPS*0.1)
    cooldownFire = 0
    clipSizeMax = 1
    clipSize = clipSizeMax
    def reload():
        weaponsReload1(qkSnaiperRaifal2001MilitaryGunPowder)
    def fire():
        weaponsFire1()
allWeapons.append(qkSnaiperRaifal2001MilitaryGunPowder)
class yni6tyjutil():
    bulletType = 1
    bulletDMG = bulletDMG*20
    bulletSpeed = bulletSpeed/11
    bulletD = bulletD*15
    fireDelayMax = 1
    fireDelay = 0
    reloadType = 2
    sprayChange = 0
    cooldownReloadMax = int(FPS*2)
    cooldownReload = 0
    cooldownFireMax = int(FPS*0.4)
    cooldownFire = 0
    clipSizeMax = 3
    clipSize = 1
    def reload():
        weaponsReload1(yni6tyjutil)
    def fire():
        weaponsFire1()
allWeapons.append(yni6tyjutil)
class heavyWeapon():
    bulletType = 1
    bulletDMG = bulletDMG
    bulletSpeed = bulletSpeed
    bulletD = bulletD*2
    fireDelayMax = 1
    fireDelay = 0
    reloadType = 2
    sprayChange = 5
    cooldownReloadMax = int(FPS*0.1)
    cooldownReload = 0
    cooldownFireMax = int(0)
    cooldownFire = 0
    clipSizeMax = 280
    clipSize = int(clipSizeMax/2)
    def reload():
        weaponsReload1(heavyWeapon)
    def fire():
        weaponsFire1(addons='random')
allWeapons.append(heavyWeapon)
class bazuka():
    bulletType = 2
    bulletDMG = 70
    bulletSpeed = bulletSpeed*0.7
    bulletD = bulletD*3
    fireDelayMax = 1
    fireDelay = 0
    reloadType = 1
    sprayChange = 0.5
    cooldownReloadMax = int(FPS*2)
    cooldownReload = 0
    cooldownFireMax = int(FPS*0.5)
    cooldownFire = 0
    clipSizeMax = 1
    clipSize = clipSizeMax
    def reload():
        weaponsReload1(bazuka)
    def fire():
        weaponsFire1()
allWeapons.append(bazuka)
class grenadePistol():
    bulletType = 2
    bulletDMG = bulletDMG
    bulletSpeed = bulletSpeed*0.6
    bulletD = bulletD*2
    fireDelayMax = 1
    fireDelay = 0
    reloadType = 1
    sprayChange = 5
    cooldownReloadMax = int(FPS*0.8)
    cooldownReload = 0
    cooldownFireMax = int(FPS*0.1)
    cooldownFire = 0
    clipSizeMax = 1
    clipSize = clipSizeMax
    def reload():
        weaponsReload1(grenadePistol)
    def fire():
        for x in range(3):
            weaponsFire1()
allWeapons.append(grenadePistol)
class flameThrower():
    bulletType = 3
    bulletDMG = bulletDMG
    bulletSpeed = bulletSpeed*0.45
    bulletD = bulletD*1.3
    fireDelayMax = 1
    fireDelay = 0
    reloadType = 1
    sprayChange = 1
    cooldownReloadMax = int(FPS*2)
    cooldownReload = 0
    cooldownFireMax = int(FPS*0.1)
    cooldownFire = 0
    clipSizeMax = 200
    clipSize = clipSizeMax
    def reload():
        weaponsReload1(flameThrower)
    def fire():
        weaponsFire1()
allWeapons.append(flameThrower)


class message():
    messagesToDisplay = []
    messageTimeOnScreen = int(FPS*5)
    def __init__(self, message):
        self.messagesToDisplay.append([message, self.messageTimeOnScreen])

class player():
    avatar = None#pygame.image.load('%s/%s' %('playerIcons', 'pIkona0.png'))
    weapons = []
    HPMax = 200
    HP = HPMax
    selfHeal = 0
    money = 0
    buyGunPrice = 100
    burningTimeLeftMax = FPS*6
    burningTimeLeft = 0
    burnDamageTaken = 0.01 * antiPerformanceFuckUp
    
    


pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Lutenica baceeeee")
displayX = 900
displayY = 650
gameDisplay = pygame.display.set_mode((displayX, displayY))
s0 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #player x
s0.bind(('', 60000))
s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #player y
s1.bind(('', 60001))
s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #bullet info
s2.bind(('', 60002))

yourX = 0
yourY = 0

enemyX = 50
enemyY = 50

moveW = 0
moveA = 0
moveS = 0
moveD = 0
youSprinting = 1

yourSpeed = 5 * antiPerformanceFuckUp
yourD = 50

respawnPlayer()
quittingGame = False
#Thread(target=sendX).start()
#Thread(target=sendY).start()
Thread(target=reciveX).start()
Thread(target=reciveY).start()
Thread(target=reciveBulletData).start()
while not quittingGame:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quittingGame = True
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moveA = yourSpeed
            elif event.key == pygame.K_d:
                moveD = yourSpeed
            elif event.key == pygame.K_w:
                moveW = yourSpeed
            elif event.key == pygame.K_s:
                moveS += yourSpeed
            elif event.key == pygame.K_r:
                equippedWeapon.reload()
            elif event.key == pygame.K_LSHIFT:
                youSprinting = 1.3
            elif event.key == pygame.K_q:
                healingTool.activate()
            elif event.key == pygame.K_b:
                if len(allWeapons) == len(player.weapons):
                    message('you have every weapon')
                else:
                    notAvailableWeapons = list(allWeapons)
                    for item in player.weapons:
                        if item in notAvailableWeapons:
                            del notAvailableWeapons[notAvailableWeapons.index(item)]
                    newWep = notAvailableWeapons[random.randrange(0, len(notAvailableWeapons))]
                    if player.money >= player.buyGunPrice:
                        player.money -= player.buyGunPrice
                        player.buyGunPrice = player.buyGunPrice*1.5
                        player.weapons.append(newWep)
                        if len(player.weapons) > 9:
                            print('you have too much weapons, please discard some of them')
                            while True:
                                for x in range(len(player.weapons)):
                                    print('%s/%s' %(x, player.weapons[x]))
                                try:
                                    choise = int(input('>'))
                                except:
                                    print('invalid choise')
                                    continue
                                if choise > 0 and choise < len(player.weapons):
                                    del player.weapons[choise]
                                    break
                    else:
                        message('not enough money')
            elif event.key == pygame.K_p:
                while True:
                    print('pick your poison:')
                    for x in range(len(allWeapons)):
                        print('%s/%s' %(x, allWeapons[x]))
                    choise = input('>')
                    try:
                        choise = int(choise)
                    except:
                        print('invalid option')
                    else:
                        switchTo(allWeapons[choise])
                        break
            else:
                for x in range(len(player.weapons)):
                    exec('''
if event.key == pygame.K_%s:
    switchTo(%s)''' %(x+1, player.weapons[x].__name__))
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moveA = 0
            elif event.key == pygame.K_d:
                moveD = 0
            elif event.key == pygame.K_w:
                moveW = 0
            elif event.key == pygame.K_s:
                moveS = 0
            elif event.key == pygame.K_LSHIFT:
                youSprinting = 1

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click.L = True
            elif event.button == 5:
                if player.weapons.index(equippedWeapon) == len(player.weapons)-1:
                    switchTo(player.weapons[0])
                else:
                    switchTo(player.weapons[player.weapons.index(equippedWeapon)+1])
            elif event.button == 4:
                if player.weapons.index(equippedWeapon) == 0:
                    switchTo(player.weapons[-1])
                else:
                    switchTo(player.weapons[player.weapons.index(equippedWeapon)-1])

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                click.L = False

    cur = pygame.mouse.get_pos()



    

    if FPScounter.start+1 <= time.time() or FPScounter.start == 0:
        FPScounter.lastKnownFrames = add1del1(FPScounter.lastKnownFrames, FPScounter.frames)
        sbor = 0
        for item in FPScounter.lastKnownFrames:
            sbor += item
        FPScounter.averageFPS = sbor/len(FPScounter.lastKnownFrames)
        FPScounter.frames = 0
        if FPScounter.averageFPS < FPS and FPScounter.lastKnownFrames[-1] != 0:
            #print('reducing your FPS to %s is recommend' %(FPScounter.averageFPS))
            pass
        FPScounter.start = time.time()
    FPScounter.frames += 1


    for x in range(len(message.messagesToDisplay)-1, -1, -1):
        message.messagesToDisplay[x][1] -= 1
        if message.messagesToDisplay[x][1] == 0:
            del message.messagesToDisplay[x]
        
    

    lastYourX = yourX
    lastYourY = yourY

    yourY -= moveW*youSprinting
    yourY += moveS*youSprinting
    yourX -= moveA*youSprinting
    yourX += moveD*youSprinting

    
    for x in range(len(walls)):
        shibStena(walls[x][0], walls[x][1], walls[x][2], walls[x][3])

    sendXandY()
            

    if yourX < 0:
        yourX = 0
    elif yourX + yourD > displayX:
        yourX = displayX - yourD
    if yourY < 0:
        yourY = 0
    elif yourY + yourD > displayY:
        yourY = displayY - yourD

    if click.L:
        if equippedWeapon.cooldownFire == 0 and ((equippedWeapon.cooldownReload == 0 and equippedWeapon.reloadType == 1) or equippedWeapon.reloadType == 2) and equippedWeapon.fireDelay == 0:
            if equippedWeapon.clipSize > 0:
                if equippedWeapon.reloadType == 2:
                    equippedWeapon.cooldownReload = 0
                equippedWeapon.fireDelay = equippedWeapon.fireDelayMax
            else:
                equippedWeapon.reload()

    if equippedWeapon.fireDelay > 0:
        equippedWeapon.fireDelay -= 1
        if equippedWeapon.fireDelay <= 0:
            equippedWeapon.fireDelay = 0
            equippedWeapon.cooldownFire = equippedWeapon.cooldownFireMax
            equippedWeapon.clipSize -= 1
            equippedWeapon.fire()
                
    if equippedWeapon.cooldownFire > 0:
        equippedWeapon.cooldownFire -= 1
    if equippedWeapon.reloadType == 1:
        if equippedWeapon.cooldownReload > 0:
            if youSprinting == 1:
                equippedWeapon.cooldownReload -= 1
                if equippedWeapon.cooldownReload == 0:
                    equippedWeapon.clipSize = equippedWeapon.clipSizeMax
            else:
                equippedWeapon.cooldownReload = 0
    else:
        if equippedWeapon.cooldownReload > 0:
            if youSprinting == 1:
                equippedWeapon.cooldownReload -= 1
                if equippedWeapon.cooldownReload == 0:
                    equippedWeapon.clipSize += 1
                    if equippedWeapon.clipSize < equippedWeapon.clipSizeMax:
                        equippedWeapon.cooldownReload = equippedWeapon.cooldownReloadMax
            else:
                equippedWeapon.cooldownReload = 0

    if healingTool.healCooldown > 0:
        healingTool.healCooldown -= 1

    for x in range(len(bullets)-1, -1, -1):
        if bullets[x][0]+bullets[x][4] < 0 or bullets[x][0] > displayX or bullets[x][1]+bullets[x][4] < 0 or bullets[x][1] > displayY:
            del bullets[x]
            continue

        dokosnalNe6to = False
        if bullets[x][5] == True:
            if doko(bullets[x][0], bullets[x][1], bullets[x][4], bullets[x][4], enemyX, enemyY, yourD, yourD):
                player.money += bullets[x][6]
                dokosnalNe6to = True 
        else:
            if doko(bullets[x][0], bullets[x][1], bullets[x][4], bullets[x][4], yourX, yourY, yourD, yourD):
                player.HP -= bullets[x][6]
                if bullets[x][7] == 3:
                    player.burningTimeLeft = player.burningTimeLeftMax
                dokosnalNe6to = True
                
        for y in range(len(walls)-1, -1, -1):
            if doko(walls[y][0], walls[y][1], walls[y][2], walls[y][3], bullets[x][0], bullets[x][1], bullets[x][4], bullets[x][4]):
                walls[y][4] -= bullets[x][6]
                dokosnalNe6to = True

        if bullets[x][7] == 3:
            bullets[x][6] -= 0.2 * antiPerformanceFuckUp
            if bullets[x][6] <= 0:
                del bullets[x]
                continue
            bullets[x][4] += 1 * antiPerformanceFuckUp
                
        if dokosnalNe6to:
            if bullets[x][7] == 2:
                for y in range(len(walls)-1, -1, -1):
                    #if doko(walls[y][0], walls[y][1], walls[y][2], walls[y][3], bullets[x][0]-bullets[x][4], bullets[x][1]-bullets[x][4], bullets[x][4]*3, bullets[x][4]*3):
                    rastoqnieto = rastoqnie(walls[y][0]+(walls[y][2]/2), walls[y][1]+(walls[y][3]/2), bullets[x][0]+(bullets[x][4]/2), bullets[x][1]+(bullets[x][4]/2))
                    if rastoqnieto < bullets[x][6] and rastoqnieto > 0:
                        walls[y][4] -= bullets[x][6] - rastoqnieto

                if bullets[x][5] == True:
                    rastoqnieto = rastoqnie(bullets[x][0]+(bullets[x][4]/2), bullets[x][1]+(bullets[x][4]/2), enemyX+(yourD/2), enemyY+(yourD/2))
                    if rastoqnieto < bullets[x][6] and rastoqnieto > 0:
                        player.money += bullets[x][6] - rastoqnieto
                else:
                    rastoqnieto = rastoqnie(bullets[x][0]+(bullets[x][4]/2), bullets[x][1]+(bullets[x][4]/2), yourX+(yourD/2), yourY+(yourD/2))
                    if rastoqnieto < bullets[x][6] and rastoqnieto > 0:
                        player.HP -= bullets[x][6] - rastoqnieto
                
            del bullets[x]
            continue
            
        bullets[x][0] += bullets[x][2] * antiPerformanceFuckUp
        bullets[x][1] += bullets[x][3] * antiPerformanceFuckUp

    for x in range(len(walls)-1, -1, -1):
        if walls[x][4] <= 0:
            del walls[x]


    if player.burningTimeLeft > 0:
        player.burningTimeLeft -= 1
        player.HP -= player.burnDamageTaken


    if player.selfHeal > 0:
        player.HP += 1
        player.selfHeal -= 1    

    if player.HP < 0:
        respawnPlayer()
    elif player.HP < player.HPMax:
        player.HP += 0.01 * antiPerformanceFuckUp
        
    if player.HP > player.HPMax:
        player.HP = player.HPMax


    backgroundColor = (220-((player.HP/player.HPMax)*220), 0, 0)
    gameDisplay.fill(backgroundColor)
    for item in bullets:
        pygame.draw.rect(gameDisplay, yellow, (item[0], item[1], item[4], item[4]))
    for item in walls:
        pygame.draw.rect(gameDisplay, (255, 255, (item[4]/item[5])*255), (item[0], item[1], item[2], item[3]))
    pygame.draw.rect(gameDisplay, red, (enemyX, enemyY, yourD, yourD))
    gameDisplay.blit(tImage(yourD, yourD, player.avatar), (yourX, yourY))
    pygame.draw.rect(gameDisplay, yellow, (0, 0, (equippedWeapon.clipSize/equippedWeapon.clipSizeMax)*displayX, 5))
    if equippedWeapon.cooldownReload != 0 :
        pygame.draw.rect(gameDisplay, purple, (0, 0, (1-(equippedWeapon.cooldownReload/equippedWeapon.cooldownReloadMax))*displayX, 5))
    pygame.draw.rect(gameDisplay, yellow, (0, 5, (equippedWeapon.fireDelay/equippedWeapon.fireDelayMax)*displayX, 5))
    msg(0, 0, '%s|%s' %(FPScounter.lastKnownFrames[0], FPScounter.averageFPS), size=30)
    msg(0, 30, equippedWeapon, size=30)
    if player.money >= player.buyGunPrice:
        color = green
    elif player.money >= player.buyGunPrice/2:
        color = yellow
    else:
        color = red
    msg(0, displayY - 60, 'money=%s, %s/9, %s' %(player.money, len(player.weapons), player.burningTimeLeft), size=30, color=color)
    msg(0, displayY - 30, '%s, %s' %(int(player.HP), healingTool.healCooldown), size=30)
    for item in message.messagesToDisplay:
        msg(yourX-yourD, yourY - ((message.messageTimeOnScreen-item[1])/4), item[0], size=25)

    
    
    pygame.display.update()
    clock.tick(FPS)
    
        

pygame.quit()
quit()


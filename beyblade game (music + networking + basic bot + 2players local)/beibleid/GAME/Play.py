print('v1.3')
import pygame
import random
import copy
import socket
import time
import os
import settings
import chooseBeyblade
from threading import Thread
from colors import *
from funcs import *




pygame.init()

displayX = settings.displayX
displayY = settings.displayY
displayR = settings.displayR
if settings.fullScreen:
    gameDisplay = pygame.display.set_mode((displayX, displayY), pygame.FULLSCREEN)
else:
    gameDisplay = pygame.display.set_mode((displayX, displayY))
    
clock = pygame.time.Clock()

pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

def msg(text, x, y, color=green, size=20):
    font = pygame.font.Font(settings.font, size)
    text = font.render(str(text), 1, color)
    gameDisplay.blit(text, (x, y))

def imgTrans(snimka, x, y):
    return pygame.transform.scale(snimka, (x, y))

class player():
    x = 0
    y = 0
    r = 50

    def respawn(self):
        newBeyblade = chooseBeyblade.main()
        for item in dir(newBeyblade):
            if item[0] != '_':
                exec('self.%s = newBeyblade.%s' %(item, item))
        self.newBeyblade = None
        
        if gamemode == 'online':
            self.sendColor()

        self.vartene = copy.deepcopy(self.varteneMax)
        self.wMove = 0
        self.aMove = 0
        self.sMove = 0
        self.dMove = 0
        self.xVel = 0
        self.yVel = 0

        while True:
            self.x = random.randint(0, displayX)
            self.y = random.randint(0, displayY)
            if (not rast(self.x, self.y, displayX//2, displayY//2) > displayR - self.r) and (not rast(self.x, self.y, enemy.x, enemy.y) < (self.r + enemy.r)):
                break

    def shibArena(self):
        if enemy.connected():
            self.vartene -= (abs(self.xVel) + abs(self.yVel)) * self.arenaPenalty
        self.x = self.lastX
        self.y = self.lastY
        self.xVel *= -self.otbluskvaneArena
        self.yVel *= -self.otbluskvaneArena

    def shibEnemy(self, enemyXVel, enemyYVel):
        if enemy.connected():
            self.vartene -= (abs(enemyXVel) + abs(enemyYVel)) * self.enemyPenalty
            if gamemode.get() != 'online':
                enemy.vartene -= (abs(self.xVel) + abs(self.yVel)) * enemy.enemyPenalty
                enemy.x = enemy.lastX
                enemy.y = enemy.lastY
                enemy.xVel = player.xVel
                enemy.yVel = player.yVel
        self.x = self.lastX
        self.y = self.lastY
        self.xVel = enemyXVel
        self.yVel = enemyYVel

    def sendX(self):
        s1.sendto(str(self.x).encode('utf-8'), (settings.playerIP, 60000))
    def sendY(self):
        s2.sendto(str(self.y).encode('utf-8'), (settings.playerIP, 60001))
    def sendXVel(self):
        s3.sendto(str(self.xVel).encode('utf-8'), (settings.playerIP, 60002))
    def sendYVel(self):
        s4.sendto(str(self.yVel).encode('utf-8'), (settings.playerIP, 60003))
    def sendVartene(self):
        s5.sendto(str(self.vartene).encode('utf-8'), (settings.playerIP, 60004))
    def sendPointToEnemy(self):
        s6.sendto(('%s'%(score.enemy)).encode('utf-8'), (settings.playerIP, 60005))
    def sendColor(self):
        s7.sendto(('%s|%s|%s'%(self.color[0], self.color[1], self.color[2])).encode('utf-8'), (settings.playerIP, 60006))
player = player()


class enemy():
    x = 400
    y = 500
    r = player.r
    color = red
    #xVel = 0
    #Vel = 0
    vartene = 10

    lastVarteneRecived = 0

    def connected(self):
        if time.time() - self.lastVarteneRecived < 0.1 or gamemode.get() != 'online':
            return True
        return False

    def respawn(self):
        newBeyblade = chooseBeyblade.main('Choose SECOND beyblade')
        for item in dir(newBeyblade):
            if item[0] != '_':
                exec('self.%s = newBeyblade.%s' %(item, item))

        self.vartene = copy.deepcopy(self.varteneMax)
        self.wMove = 0
        self.aMove = 0
        self.sMove = 0
        self.dMove = 0
        self.xVel = 0
        self.yVel = 0

        while True:
            self.x = random.randint(0, displayX)
            self.y = random.randint(0, displayY)
            if (not rast(self.x, self.y, displayX//2, displayY//2) > displayR - self.r) and (not rast(self.x, self.y, player.x, player.y) < (self.r + player.r)):
                break

    def shibArena(self):
        self.vartene -= (abs(self.xVel) + abs(self.yVel)) * self.arenaPenalty
        self.x = self.lastX
        self.y = self.lastY
        self.xVel *= -self.otbluskvaneArena
        self.yVel *= -self.otbluskvaneArena
enemy = enemy()


class score():
    enemy = 0
    player = 0
    def playerPoint(self):
        self.player += 1
    def enemyPoint(self):
        self.enemy += 1
    def updatePlayerScore(self, newScore):
        self.player = int(newScore)
    def draw(self):
        msg('%s:%s' %(score.player, score.enemy), displayX/2 - ((pygame.font.Font(settings.font, 50).size('%s:%s' %(score.player, score.enemy)))[0]/2), 0, size=50)
score = score()

class fps():
    lastFrame = 0
    def get(self):
        newFrame = time.time()
        speed = newFrame - self.lastFrame
        self.lastFrame = newFrame
        return 1/speed
fps = fps()

class soundtrack():
    allSongs = []
    playedSongs = []
    def loadAllSongs(self):
        for (folderName, nz, files) in os.walk('music'):
            for file in files:
                self.addSong(file)
            break
        print('%s songs loaded' %(len(self.allSongs)))
    def addSong(self, fileName):
        try:
            self.allSongs.append(pygame.mixer.Sound(os.path.join('music', fileName)))
        except pygame.error:
            print('ERROR: unable to load file: %s' %(fileName))
    def playRandomSong(self):
        if len(self.allSongs) > 0:
            if len(self.playedSongs) == len(self.allSongs):
                self.playedSongs = []
            while True:
                choosenSong = random.randrange(0, len(self.allSongs))
                if choosenSong not in self.playedSongs:
                    break
            self.playedSongs.append(choosenSong)
            self.allSongs[choosenSong].play()
soundtrack = soundtrack()


def reciveEnemyX():
    global enemy
    while True:
        data, addr = s1.recvfrom(1024)
        data = data.decode('utf-8')
        enemy.x = float(data)

def reciveEnemyY():
    global enemy
    while True:
        data, addr = s2.recvfrom(1024)
        data = data.decode('utf-8')
        enemy.y = float(data)

def reciveEnemyXVel():
    global enemy
    while True:
        data, addr = s3.recvfrom(1024)
        data = data.decode('utf-8')
        data = float(data)
        enemy.xVel = data

def reciveEnemyYVel():
    global enemy
    while True:
        data, addr = s4.recvfrom(1024)
        data = data.decode('utf-8')
        data = float(data)
        enemy.yVel = data

def reciveEnemyVartene():
    global enemy
    while True:
        data, addr = s5.recvfrom(1024)
        data = data.decode('utf-8')
        data = float(data)
        enemy.vartene = data
        enemy.lastVarteneRecived = time.time()

def reciveYourPoint():
    #global score
    while True:
        data, addr = s6.recvfrom(1024)
        data = data.decode('utf-8')
        #score.player += 1
        #score.player = data
        score.updatePlayerScore(data)
        player.respawn()

def reciveEnemyColor():
    global score
    while True:
        data, addr = s7.recvfrom(1024)
        data = data.decode('utf-8')
        data = data.split('|')
        enemy.color = (int(data[0]), int(data[1]), int(data[2]))


class gamemode():
    gamemode = None
    def get(self):
        return self.gamemode
    
    def shutDownCurrentGamemode(self):
        if self.gamemode == 'online':
            s1.close()
            s2.close()
            s3.close()
            s4.close()
            s5.close()
            s6.close()
            s7.close()

        

    def restart(self):
        player.respawn()
        if self.gamemode != 'online':
            enemy.respawn()
        
    def setOnline(self):
        global s1
        global s2
        global s3
        global s4
        global s5
        global s6
        global s7
        
        self.shutDownCurrentGamemode()

        s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s5 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s6 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s7 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        s1.bind(('', 60000)) #sendvane na x
        s2.bind(('', 60001)) #sendvane na y
        s3.bind(('', 60002)) #sendvane na xVel
        s4.bind(('', 60003)) #sendvane na yVel
        s5.bind(('', 60004)) #sendvane na vartene
        s6.bind(('', 60005)) #sendvane na +1 to4ka
        s7.bind(('', 60006)) #sendvane na cveta

        Thread(target=reciveEnemyX).start()
        Thread(target=reciveEnemyY).start()
        Thread(target=reciveEnemyXVel).start()
        Thread(target=reciveEnemyYVel).start()
        Thread(target=reciveEnemyVartene).start()
        Thread(target=reciveYourPoint).start()
        Thread(target=reciveEnemyColor).start()

        self.gamemode = 'online'
        self.restart()
        
    def setBot(self):
        self.shutDownCurrentGamemode()
        self.gamemode = 'bot'
        self.restart()
        
    def setLan(self):
        self.shutDownCurrentGamemode()
        self.gamemode = 'lan'
        self.restart()

    def setBotVsBot(self):
        self.shutDownCurrentGamemode()
        self.gamemode = 'botvsbot'
        self.restart()
gamemode = gamemode()




soundtrack.loadAllSongs()

gamemode.setBotVsBot()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.wMove = player.speed
            elif event.key == pygame.K_a:
                player.aMove = player.speed
            elif event.key == pygame.K_s:
                player.sMove = player.speed
            elif event.key == pygame.K_d:
                player.dMove = player.speed
                
            elif event.key == pygame.K_UP:
                enemy.wMove = enemy.speed
            elif event.key == pygame.K_LEFT:
                enemy.aMove = enemy.speed
            elif event.key == pygame.K_DOWN:
                enemy.sMove = enemy.speed
            elif event.key == pygame.K_RIGHT:
                enemy.dMove = enemy.speed
                
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
                
            elif event.key == pygame.K_b:
                gamemode.setBot()
            elif event.key == pygame.K_n:
                gamemode.setLan()
            elif event.key == pygame.K_m:
                gamemode.setOnline()
            elif event.key == pygame.K_COMMA:
                gamemode.setBotVsBot()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player.wMove = 0
            elif event.key == pygame.K_a:
                player.aMove = 0
            elif event.key == pygame.K_s:
                player.sMove = 0
            elif event.key == pygame.K_d:
                player.dMove = 0

            elif event.key == pygame.K_UP:
                enemy.wMove = 0
            elif event.key == pygame.K_LEFT:
                enemy.aMove = 0
            elif event.key == pygame.K_DOWN:
                enemy.sMove = 0
            elif event.key == pygame.K_RIGHT:
                enemy.dMove = 0


    if pygame.mixer.get_busy() == False:
        soundtrack.playRandomSong()



            


    player.lastX = player.x
    player.lastY = player.y

    if gamemode.get() == 'botvsbot':
        if player.x < enemy.x:
            player.xVel += abs(player.speed)
        elif player.x > enemy.x:
            player.xVel -= abs(player.speed)
        if player.y < enemy.y:
            player.yVel += abs(player.speed)
        elif player.y > enemy.y:
            player.yVel -= abs(player.speed)
    else:
        player.xVel += player.dMove - player.aMove
        player.yVel += player.sMove - player.wMove

    player.xVel += random.uniform(-player.randomness, player.randomness)
    player.yVel += random.uniform(-player.randomness, player.randomness)

    if player.x < displayX/2:
        player.xVel += player.privli4aneCentur
    elif player.x > displayX/2:
        player.xVel -= player.privli4aneCentur
    if player.y < displayY/2:
        player.yVel += player.privli4aneCentur
    elif player.y > displayY/2:
        player.yVel -= player.privli4aneCentur

    player.x += player.xVel
    player.y += player.yVel

    if gamemode.get() == 'online':
                #send your x and y
                player.sendX()
                player.sendY()
                #send xVel and yVel
                player.sendXVel()
                player.sendYVel()
                #send vartene
                player.sendVartene()

    if enemy.connected():
        player.vartene -= ((player.vartenePenalty * abs(player.xVel)) + (player.vartenePenalty * abs(player.yVel)))
        player.vartene -= player.vartenePenalty


    #ako se 6ibne v enemito
    if rast(player.x, player.y, enemy.x, enemy.y) < (player.r + enemy.r):
        player.shibEnemy(enemy.xVel, enemy.yVel)

    #ako se 6ibne v arenata
    if rast(player.x, player.y, displayX//2, displayY//2) > displayR - player.r:
        player.shibArena()

    
    


    if player.vartene <= 0:
        score.enemyPoint()
        if gamemode.get() == 'online':
            for x in range(3):
                player.sendPointToEnemy()
                time.sleep(0.2)
            player.respawn()
        else:
            player.respawn()
            enemy.respawn()

    if gamemode.get() != 'online':

            enemy.lastX = enemy.x
            enemy.lastY = enemy.y

            if gamemode.get() == 'bot':
                if player.x < enemy.x:
                    enemy.xVel -= abs(enemy.speed)
                elif player.x > enemy.x:
                    enemy.xVel += abs(enemy.speed)
                if player.y < enemy.y:
                    enemy.yVel -= abs(enemy.speed)
                elif player.y > enemy.y:
                    enemy.yVel += abs(enemy.speed)
            elif gamemode.get() == 'lan':
                enemy.xVel += enemy.dMove - enemy.aMove
                enemy.yVel += enemy.sMove - enemy.wMove

            enemy.xVel += random.uniform(-enemy.randomness, enemy.randomness)
            enemy.yVel += random.uniform(-enemy.randomness, enemy.randomness)

            if enemy.x < displayX/2:
                enemy.xVel += enemy.privli4aneCentur
            elif enemy.x > displayX/2:
                enemy.xVel -= enemy.privli4aneCentur
            if enemy.y < displayY/2:
                enemy.yVel += enemy.privli4aneCentur
            elif enemy.y > displayY/2:
                enemy.yVel -= enemy.privli4aneCentur

            enemy.x += enemy.xVel
            enemy.y += enemy.yVel

            enemy.vartene -= (enemy.vartenePenalty * abs(enemy.xVel)) + (enemy.vartenePenalty * abs(enemy.yVel))
            enemy.vartene -= enemy.vartenePenalty

            #ako se 6ibne v aranata
            if rast(enemy.x, enemy.y, displayX//2, displayY//2) > displayR - enemy.r:
                enemy.shibArena()

            

            if enemy.vartene <= 0:
                #score.player += 1
                score.playerPoint()
                player.respawn()
                enemy.respawn()




    
    gameDisplay.fill(black)
    pygame.draw.circle(gameDisplay, white, (displayX//2, displayY//2), displayR)
    #temp = (255*(player.vartene/player.varteneMax), 255*(player.vartene/player.varteneMax), 255*(player.vartene/player.varteneMax))
    #pygame.draw.line(gameDisplay, temp, (0, displayY//2), (displayX, displayY//2)) 
    
    pygame.draw.circle(gameDisplay, player.color, (int(player.x), int(player.y)), player.r)
    #pygame.draw.circle(gameDisplay, [abs(255*(player.vartene/player.varteneMax))]*3, (int(player.x), int(player.y)), player.r//2)

    pygame.draw.circle(gameDisplay, enemy.color, (int(enemy.x), int(enemy.y)), enemy.r)

    msg(player.vartene, 0, 0, size=50)
    msg(int(abs(player.xVel) + abs(player.yVel)), 0, 50, size=40)
    msg(player.xVel, 0, 90, size=20)
    msg(player.yVel, 0, 110, size=20)
    msg(time.time() - enemy.lastVarteneRecived, 0, 140, size=20)
    msg('FPS=%s'%(int(fps.get())), 0, 160, size=40)

    msg(enemy.vartene, displayX - 200, 0, size=50, color=red)
    msg(int(abs(enemy.xVel) + abs(enemy.yVel)), displayX - 200, 50, size=40, color=red)
    msg(enemy.xVel, displayX - 200, 90, color=red, size=20)
    msg(enemy.yVel, displayX - 200, 110, color=red, size=20)
    msg(gamemode.get(), displayX - 200, 140, color=red, size=40)

    score.draw()


    pygame.display.update()
    clock.tick(settings.FPS)


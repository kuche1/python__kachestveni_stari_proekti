print('v0.1.5')
import pygame
import time
import copy
import random
import guns
import perks
from colors import *
#
import os
from funcs import *

import Play


class MAP():
    #name = None
    spawn = [0,0]
    end = [100,100]
    endd = Play.MAP.endd
    def load(self, fname):
        f = open('maps//%s//1.py' %(fname))
        fcont = f.read().split('\n')
        f.close()

        enemyspawns.remall()
        enemies.remall()
        walls.remall()
        traders.remall()

        self.name = fname

        self.spawn = eval(fcont[0])#spawn
        for item in eval(fcont[1]):#enemy spawns
            enemyspawns.add(item[0], item[1])
        for item in eval(fcont[2]):#enemies
            enemies.add(item[0], item[1], item[2], item[3], item[4], item[5])
        for item in eval(fcont[3]):#walls
            if item[2] == 0 or item[3] == 0:
                print('A wall with no length has been detected and removed')
            else:
                for number in [2,3]:
                    if item[number] < 0:
                        item[number-2] += item[number]
                        item[number] *= -1
                        print('A wall with negative length has been detected and repaired')
                if item[4] != None and item[4] <= 0:
                    print('A wall with hp <= 0 has been detected and replaced with a wall with infinite hp')
                    item[4] = None
                walls.add(item[0], item[1], item[2], item[3], item[4])
        self.end = eval(fcont[4])#map end
        for item in eval(fcont[5]):#treidari
            traders.add(item[0], item[1])

    def save(self):
        f = open('maps//%s//1.py' %(MAP.name), 'w')
        f.write('%s\n' %(MAP.spawn))#spawna
        f.write('[')
        for x in range(len(enemyspawns.x)):#enemi spawnovete
            f.write('[%s,%s]' %(enemyspawns.x[x], enemyspawns.y[x]))
            if x != len(enemyspawns.x)-1: f.write(',')
        f.write(']\n')
        f.write('[')
        for x in range(len(enemies.x)):#enemitata
            f.write('[%s,%s,%s,%s,%s,%s]' %(enemies.x[x], enemies.y[x], enemies.d[x], enemies.speed[x], enemies.hp[x], enemies.dmg[x]))
            if x != len(enemies.x)-1: f.write(',')
        f.write(']\n')
        f.write('[')
        for x in range(len(walls.x)):#stenite
            f.write('[%s,%s,%s,%s,%s]' %(walls.x[x], walls.y[x], walls.dx[x], walls.dy[x], walls.hp[x]))
            if x != len(walls.x)-1: f.write(',')
        f.write(']\n')
        f.write('%s\n' %(MAP.end))#kraq na mapa
        f.write('[')
        for x in range(len(traders.x)):#treidarite:
            f.write('[%s,%s]' %(traders.x[x], traders.y[x]))
            if x != len(traders.x)-1: f.write(',')
        f.write(']\n')
        f.close()
    def savebackup(self):
        originalname = copy.deepcopy(self.name)
        self.name = '_' + self.name + '_' + str(time.time())
        self.save()
        self.name = originalname
    def drawspawn(self, a=None):
        if a == None:
            pygame.draw.rect(screen, Play.player.color, (self.spawn[0]-camera.x, self.spawn[1]-camera.y, Play.player.d, Play.player.d))
        else:
            pygame.draw.rect(screen, Play.player.color, (cur[0], cur[1], Play.player.d, Play.player.d))
    def drawend(self, a=None):
        if a == None:
            pygame.draw.rect(screen, Play.MAP.endcolor, (self.end[0] - camera.x, self.end[1] - camera.y, self.endd, self.endd))
        else:
            pygame.draw.rect(screen, Play.MAP.endcolor, (cur[0], cur[1], self.endd, self.endd))
MAP = MAP()



def doko(item1X, item1Y, item1DX, item1DY, item2X, item2Y, item2DX, item2DY):
    if item1X + item1DX > item2X and item1X < item2X + item2DX and item1Y + item1DY > item2Y and item1Y < item2Y + item2DY:
        return True
    return False

def tImage(x, y, snimka):
    return pygame.transform.scale(snimka, (x, y))

def rast(x1, y1, x2, y2):
    a = abs(x1-x2)
    b = abs(y1-y2)
    return ((a**2)+(b**2))**0.5
    

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("hos map editor")
screenx = 1000
screeny = 1000
screen = pygame.display.set_mode((screenx, screeny))

FPS = 60

myfont = list([pygame.font.SysFont(None, x) for x in range(1, 100)])
def msg(text, x, y, size=30, color=green):
    #myfont = pygame.font.SysFont(None, size)
    label = myfont[size].render(str(text), 0, color)
    screen.blit(label, (x, y))
    #screen.blit(pygame.font.SysFont(None, size).render(str(text), 0, color), (x,y))




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

class fps():
    lastrecord = 0
    current = 0
    def count(self):
        try:
            self.current = 1 / (time.time() - self.lastrecord)
        except ZeroDivisionError:
            self.current = '-1'
        self.lastrecord = time.time()
    def get(self):
        return self.current
fps = fps()

class camera():
    x = 0
    y = 0
    def followplayer(self):
        try:
            change = getchange(self.x, self.y, player.x - (screenx/2), player.y - (screeny/2))
        except ZeroDivisionError:
            print('', end='')
        else:
            beforex = player.x-camera.x-(screenx/2)
            beforey = player.y-camera.y-(screeny/2)
            change[0] *= player.camspeed
            change[1] *= player.camspeed
            self.x += change[0]
            self.y += change[1]
            afterx = player.x-camera.x-(screenx/2)
            aftery = player.y-camera.y-(screeny/2)
            if beforex < 0 and afterx > 0 or beforex > 0 and afterx < 0:
                self.focusx()
            if beforey < 0 and aftery > 0 or beforey > 0 and aftery < 0:
                self.focusy()
    def focusonplayer(self):
        self.focusx()
        self.focusy()
    def focusx(self):
        self.x = player.x - (screenx/2)
    def focusy(self):
        self.y = player.y - (screeny/2)
camera = camera()

def openconsolemsg():
        screen.fill(black)
        msg('OPEN YOUR CONSOLE', 0, 0, size=60)
        pygame.display.update()


class hud():
    y = 0
    def addtext(self, text, size=30):
        msg(text, 0, self.y, size)
        self.y += size
    def draw(self):
        self.addtext('FPS:%s' %(int(fps.get())))
        self.addtext('CameraX: %s' %(camera.x))
        self.addtext('CameraY: %s' %(camera.y))
        self.addtext('SelectedTool: %s' %(tool.selected))
        
        self.y = 0
hud = hud()

class enemyspawns():
    x = []
    y = []
    d = 20
    def add(self, x ,y):
        self.x.append(x)
        self.y.append(y)
    def rem(self, number):
        del self.x[number]
        del self.y[number]
    def remall(self):
        for x in range(len(self.x)):
            self.rem(0)
    def draw(self, a=None):
        if a == None:
            for x in range(len(self.x)):
                pygame.draw.rect(screen, yellow, (self.x[x] - camera.x, self.y[x] - camera.y, self.d, self.d))
        else:
            pygame.draw.rect(screen, yellow, (cur[0], cur[1], self.d, self.d))
enemyspawns = enemyspawns()

class enemies():
    x = []
    y = []
    d = []
    speed = []
    hp = []
    dmg = []
    def dokowall(self, number):
        for x in range(len(walls.x)):
            if doko(self.x[number], self.y[number], self.d[number], self.d[number], walls.x[x], walls.y[x], walls.dx[x], walls.dy[x]):
                return True
        return False
    def add(self, x ,y ,d ,speed, hp, dmg):
        self.x.append(x)
        self.y.append(y)
        self.d.append(d)
        self.speed.append(speed)
        self.hp.append(hp)
        self.dmg.append(dmg)
    def rem(self, number):
        del self.x[number]
        del self.y[number]
        del self.d[number]
        del self.speed[number]
        del self.hp[number]
        del self.dmg[number]
    def remall(self):
        for x in range(len(self.x)):
            self.rem(0)
    def draw(self, a=None):
        if a == None:
            for x in range(len(self.x)):
                pygame.draw.rect(screen, red, (self.x[x] - camera.x, self.y[x] - camera.y, self.d[x], self.d[x]))
                msg(self.hp[x], self.x[x] - camera.x, self.y[x] - camera.y)
        else:
            pygame.draw.rect(screen, red, (cur[0], cur[1], tool.d, tool.d))
            msg(tool.hp, cur[0], cur[1])
enemies = enemies()

class walls():
    x = []
    y = []
    dx = []
    dy = []
    hp = []
    color = Play.walls.color
    wallwithhpcolor = Play.walls.wallwithhpcolor
    def add(self, x ,y ,dx ,dy, hp):
        self.x.append(x)
        self.y.append(y)
        self.dx.append(dx)
        self.dy.append(dy)
        self.hp.append(hp)
    def rem(self, number):
        del self.x[number]
        del self.y[number]
        del self.dx[number]
        del self.dy[number]
        del self.hp[number]
    def remall(self):
        for x in range(len(self.x)):
            self.rem(0)
    def draw(self, a=None):
        if a == None:
            for x in range(len(self.x)):
                if doko(camera.x, camera.y, screenx, screeny, self.x[x], self.y[x], self.dx[x], self.dy[x]):
                    if self.hp[x] == None:
                        pygame.draw.rect(screen, self.color, (self.x[x] - camera.x, self.y[x] - camera.y, self.dx[x], self.dy[x]))
                    else:
                        pygame.draw.rect(screen, self.wallwithhpcolor, (self.x[x] - camera.x, self.y[x] - camera.y, self.dx[x], self.dy[x]))
                        msg(self.hp[x], self.x[x]-camera.x, self.y[x]-camera.y)
        else:
            if tool.wallhp == None or tool.wallhp <= 0:
                pygame.draw.rect(screen, self.color, (cur[0], cur[1], tool.dx, tool.dy))
            else:
                pygame.draw.rect(screen, self.wallwithhpcolor, (cur[0], cur[1], tool.dx, tool.dy))
                msg(tool.wallhp, cur[0], cur[1])
walls = walls()

class traders():
    x = []
    y = []
    d = Play.traders.d
    color = Play.traders.color
    def add(self, x, y):
        self.x.append(x)
        self.y.append(y)
    def remall(self):
        for x in range(len(self.x)):
            self.rem(0)
    def rem(self, number):
        del self.x[number]
        del self.y[number]
    def draw(self, a=None):
        if a == None:
            for x in range(len(self.x)):
                pygame.draw.rect(screen, self.color, (self.x[x]-camera.x, self.y[x]-camera.y, self.d, self.d))
        else:
            pygame.draw.rect(screen, self.color, (cur[0], cur[1], self.d, self.d))
traders = traders()        

class player():
    movea = 0
    moves = 0
    moved = 0
    movew = 0
    movex = 0
    movey = 0
    speed = 20
    x = 0
    y = 0
    d = Play.player.d
    def dokowall(self):
        for x in range(len(walls.x)):
            if doko(self.x, self.y, self.d, self.d, walls.x[x], walls.y[x], walls.dx[x], walls.dy[x]):
                return True
        return False
    def draw(self, kade=None):
        if kade == None:
            pygame.draw.rect(screen, green, (self.x - camera.x, self.y - camera.y, self.d, self.d))
        else:
            pygame.draw.rect(screen, green, (cur[0], cur[1], self.d, self.d))
player = player()





print('HOS map editor')
print()
while True:
    print('==========')
    print('1/Make new map')
    print('2/Load existing map')
    print('3/Exit')
    choise = ch(1, 3)
    if choise == False:
        print('Invalid choise')
    elif choise == 1:
        choise = input('Enter Name: ')
        folders = list(os.walk('maps'))[0][1]
        if choise not in folders:
            os.mkdir('maps//' + choise)
            MAP.name = choise
            MAP.save()
            print('Succ')
            break
        else:
            print('A map with this name already exists')
    elif choise == 2:
        folders = list(os.walk('maps'))[0][1]
        for x, folder in enumerate(folders):
            print('%s/%s' %(x, folder))
        choise = ch(0, len(folders)-1)
        if choise is False:
            print('Invalid choise')
        else:
            MAP.load(folders[choise])
            break
    elif choise == 3:
        quit()


class tool():
    selected = 'spawn'
    d = 10
    dx = 30
    dy = 30
    hp = 50
    wallhp = 0
    dmg = 5
    speed = 3
    #
    changespeed = 5
    changea = 0
    changew = 0
    changes = 0
    changed = 0

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.movea = player.speed
            elif event.key == pygame.K_d:
                player.moved = player.speed
            elif event.key == pygame.K_w:
                player.movew = player.speed
            elif event.key == pygame.K_s:
                player.moves = player.speed
            elif event.key == pygame.K_1:
                tool.selected = 'spawn'
            elif event.key == pygame.K_2:
                tool.selected = 'enemyspawn'
            elif event.key == pygame.K_3:
                tool.selected = 'enemy'
            elif event.key == pygame.K_4:
                tool.selected = 'wall'
            elif event.key == pygame.K_5:
                tool.selected = 'endofmap'
            elif event.key == pygame.K_6:
                tool.selected = 'trader'
            elif event.key == pygame.K_q:
                tool.dx, tool.dy = tool.dy, tool.dx
            elif event.key == pygame.K_t:
                try:
                    Play.main()
                except KeyboardInterrupt:
                    pass
            elif event.key == pygame.K_e:
                if tool.selected == 'spawn':
                    MAP.spawn = rcur
                    [player.x, player.y] = rcur
                elif tool.selected == 'enemyspawn':
                    enemyspawns.add(rcur[0], rcur[1])
                elif tool.selected == 'enemy':
                    enemies.add(rcur[0], rcur[1], tool.d, tool.speed, tool.hp, tool.dmg)
                elif tool.selected == 'wall':
                    if tool.dx > 0:
                        x = copy.deepcopy(rcur[0])
                        dx = copy.deepcopy(tool.dx)
                    else:
                        x = copy.deepcopy( rcur[0] + tool.dx )
                        dx = copy.deepcopy( tool.dx * -1)
                    if tool.dy > 0:
                        y = copy.deepcopy(rcur[1])
                        dy = copy.deepcopy(tool.dy)
                    else:
                        y = copy.deepcopy( rcur[1] + tool.dy )
                        dy = copy.deepcopy( tool.dy * -1)
                    walls.add(x, y, dx, dy, (None if (tool.wallhp == None or tool.wallhp <= 0) else tool.wallhp))
                elif tool.selected == 'endofmap':
                    MAP.end = [rcur[0], rcur[1]]
                elif tool.selected == 'trader':
                    traders.add(rcur[0], rcur[1])
                else:
                    print('Unknown tool to spawn: %s' %(tools.selected))
            elif event.key == pygame.K_r:
                for x in range(len(enemyspawns.x)):
                    if doko(enemyspawns.x[x], enemyspawns.y[x], enemyspawns.d, enemyspawns.d, rcur[0], rcur[1], 1, 1):
                        enemyspawns.rem(x)
                        print('removed an enemy spawner')
                        break
                else:
                    for x in range(len(enemies.x)):
                        if doko(enemies.x[x], enemies.y[x], enemies.d[x], enemies.d[x], rcur[0], rcur[1], 1, 1):
                            enemies.rem(x)
                            print('removed an enemy')
                            break
                    else:
                        for x in range(len(traders.x)):
                            if doko(traders.x[x], traders.y[x], traders.d, traders.d, rcur[0], rcur[1], 1, 1):
                                traders.rem(x)
                                print('removed a trader')
                                break
                        else:
                            for x in range(len(walls.x)):
                                if doko(walls.x[x], walls.y[x], walls.dx[x], walls.dy[x], rcur[0], rcur[1], 1, 1):
                                    walls.rem(x)
                                    print('removed a wall')
                                    break
                            else:
                                print('There is nothing to remove here')
            elif event.key == pygame.K_f:
                print('Detecting:')
                for x in range(len(enemies.x)):
                    if doko(enemies.x[x], enemies.y[x], enemies.d[x], enemies.d[x], rcur[0], rcur[1], 1, 1):
                        print('Enemy/%shp/%sspeed/%sdmg/%sd' %(enemies.hp[x], enemies.speed[x], enemies.dmg[x], enemies.d[x]))
                for x in range(len(walls.x)):
                    if doko(walls.x[x], walls.y[x], walls.dx[x], walls.dy[x], rcur[0], rcur[1], 1, 1):
                        print('Wall/%sdx/%sdy/%shp' %(walls.dx[x], walls.dy[x], walls.hp[x]))
            elif event.key == pygame.K_c:
                if tool.selected == 'enemy':
                    while True:
                        print('===')
                        print('0/change hp (%s)' %(tool.hp))
                        print('1/change speed (%s)' %(tool.speed))
                        print('2/change dmg (%s)' %(tool.dmg))
                        print('3/change d (%s)' %(tool.d))
                        print('4/go back')
                        choise = ch(0, 4)
                        if type(ch) == bool:
                            print('invalid choise')
                        elif choise == 4:
                            break
                        else:
                            while True:
                                try:
                                    newvalue = int(input('>'))
                                except:
                                    print('Enter a number')
                                else:
                                    break
                            if choise == 0:
                                tool.hp = newvalue
                            elif choise == 1:
                                tool.speed = newvalue
                            elif choise == 2:
                                tool.dmg = newvalue
                            elif choise == 3:
                                tool.d = newvalue                        
                elif tool.selected == 'wall':
                    while True:
                        print('===')
                        print('-1/go back')
                        print('0/change dx (%s)' %(tool.dx))
                        print('1/change dy (%s)' %(tool.dy))
                        print('2/change hp (%s) [ne6to po-malko ili ravno na nula za beskrai kruf]' %(tool.wallhp))
                        choise = ch(-1,2)
                        if type(ch) == bool:
                            print('invalid choise')
                        elif choise == -1:
                            break
                        else:
                            while True:
                                try:
                                    newvalue = int(input('>'))
                                except:
                                    print('Enter a number')
                                else:
                                    break
                            if choise == 0:
                                tool.dx = newvalue
                            elif choise == 1:
                                tool.dy = newvalue
                            elif choise == 2:
                                if choise <= 0:
                                    tool.wallhp = None
                                else:
                                    tool.wallhp = newvalue
                else:
                    print('This shit is not customizable')
            elif event.key == pygame.K_LEFT:
                tool.changea = tool.changespeed
            elif event.key == pygame.K_RIGHT:
                tool.changed = tool.changespeed
            elif event.key == pygame.K_UP:
                tool.changew = tool.changespeed
            elif event.key == pygame.K_DOWN:
                tool.changes = tool.changespeed
            elif event.key == pygame.K_p:
                for (x, folders, x) in os.walk('maps'): break
                if MAP.name in folders:
                    print('Overwrite "%s"? (y/n)' %(MAP.name))
                    choise = input('>')
                    if choise == 'y':
                        #originalMAP = copy.deepcopy(MAP)
                        #MAP.load(MAP.name)
                        #MAP.savebackup()
                        #MAP = originalMAP
                        MAP.save()
                else:
                    MAP.save()
                    
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.movea = 0
            elif event.key == pygame.K_d:
                player.moved = 0
            elif event.key == pygame.K_s:
                player.moves = 0
            elif event.key == pygame.K_w:
                player.movew = 0
            elif event.key == pygame.K_LEFT:
                tool.changea = 0
            elif event.key == pygame.K_RIGHT:
                tool.changed = 0
            elif event.key == pygame.K_UP:
                tool.changew = 0
            elif event.key == pygame.K_DOWN:
                tool.changes = 0

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                #player.holdm1 = True
                pass

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                #player.holdm1 = False
                pass

    cur = pygame.mouse.get_pos()

    rcur = list(cur)
    rcur[0] += camera.x
    rcur[1] += camera.y


    tool.dx += tool.changed-tool.changea
    tool.dy += tool.changes-tool.changew


    player.movex = player.moved - player.movea
    player.movey = player.moves - player.movew
    camera.x += player.movex
    camera.y += player.movey


    screen.fill(white)

    if tool.selected == 'spawn':
        #player.draw(1)
        MAP.drawspawn(1)
    elif tool.selected == 'enemyspawn':
        enemyspawns.draw(1)
    elif tool.selected == 'enemy':
        enemies.draw(1)
    elif tool.selected == 'wall':
        walls.draw(1)
    elif tool.selected == 'endofmap':
        MAP.drawend(1)
    elif tool.selected == 'trader':
        traders.draw(1)
    else:
        print('Unknown tool to draw')

    walls.draw()
    #player.draw()
    MAP.drawspawn()
    traders.draw()
    MAP.drawend()
    enemyspawns.draw()
    enemies.draw()
    hud.draw()
    
    pygame.display.update()
    clock.tick(FPS)
    fps.count()


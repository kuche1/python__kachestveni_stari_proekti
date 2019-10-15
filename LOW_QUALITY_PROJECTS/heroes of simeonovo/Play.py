if __name__ == '__main__': print('v0.1.4.0')
import pygame
import time
import copy
import random
import os
from funcs import *
import guns
import perks
import zombies
from colors import *





def tImage(x, y, snimka):
    return pygame.transform.scale(snimka, (x, y))

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("hos")
screenx = 800
screeny = 600
screen = pygame.display.set_mode((screenx, screeny))

FPS = 60

myfont = list([pygame.font.SysFont(None, x) for x in range(1, 100)])
def msg(text, x, y, size=30, color=green):
    #myfont = pygame.font.SysFont(None, size)
    label = myfont[size].render(str(text), 0, color)
    screen.blit(label, (x, y))
    #screen.blit(pygame.font.SysFont(None, size).render(str(text), 0, color), (x,y))

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

class MAP():
    endd = 30
    endcolor = (0, 255, 255)
    start = 0
    def gettime(self):
        return time.time() - self.start
    def starttimer(self):
        self.start = time.time()
    def load(self, fname):
        f = open('maps//%s//1.py' %(fname))
        fcont = f.read().split('\n')
        f.close()

        enemyspawns.remall()
        enemies.remall()
        walls.remall()
        bullets.remall()
        traders.remall()

        self.name = fname
        
        self.spawn = eval(fcont[0])#player spawn
        for item in eval(fcont[1]):#enemy spawns
            enemyspawns.add(item[0], item[1])
        for item in eval(fcont[2]):#enemies
            enemies.add(item[0], item[1], item[2], item[3], item[4], item[5])
        for item in eval(fcont[3]):#walls
            walls.add(item[0], item[1], item[2], item[3], item[4])
        self.end = eval(fcont[4])#end of map
        for item in eval(fcont[5]):#treidari
            traders.add(item[0], item[1])

        player.respawn()
        self.starttimer()
    def changelevel(self):
        openconsolemsg()
        for (x, folders, x) in os.walk('maps'): break
        for x in range(len(folders)-1,-1,-1):
            if folders[x][0] == '_': del folders[x]
        while True:
            print('=====')
            print('Choose next map')
            print()
            for x, folder in enumerate(folders):
                print('%s/%s' %(x, folder))
            choise = ch(0, len(folders)-1)
            if type(choise) == bool:
                print('Invalid choise')
            else:
                MAP.load(folders[choise])
                break
    def drawend(self):
        pygame.draw.rect(screen, self.endcolor, (self.end[0] - camera.x, self.end[1] - camera.y, self.endd, self.endd))
MAP = MAP()

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

class shop():
    def printgundata(self, gun):
        print(' %s' %(gun.name))
        print(' -clip:                 %s' %(gun.clipmax))
        print(' -ammo:                 %s' %(gun.ammomax))
        print(' -reload:               %s' %(gun.rl))
        print(' -fire rate:            %s' %(gun.fr))
        print(' -damage:               %s' %(gun.dmg))
        print(' -bullets per shot:     %s' %(gun.bps))
        print(' -explade radius:       %s' %(gun.explrad))
        print(' -mele attack damage:   %s' %(gun.meledmg))
        print(' -mele attack fire rate:%s' %(gun.melefr))
        print(' -mele attack range:    %s' %(gun.melespeed + gun.meled))
        print(' -cost:                 %s' %(gun.cost))
    def main(self):
        openconsolemsg()
        while True:
            print('============')
            print('Money: %s' %(player.money))
            print('1/Buy guns')
            print('2/Buy ammo')
            print('3/Buy hp')
            print('4/Go back')
            choise = ch(1,4)
            if choise == False:
                print('invalid choise')
            elif choise == 1:
                weps = []
                perkweps = []
                for x, wep in enumerate(copy.deepcopy(guns.al)):
                    for attribute in player.guns:
                        if attribute in wep.types or attribute == 'all':
                            wep.clipmax = int(wep.clipmax * player.clipmult)
                            wep.ammomax = int(wep.ammomax * player.ammomult)
                            wep.rl *= player.rlmult
                            wep.fr *= player.frmult
                            wep.dmg *= player.dmgmult
                            wep.bps = int(wep.bps * player.bpsmult)
                            wep.explrad *= player.explradmult
                            wep.cost = int(wep.cost * player.costmult)
                            wep.meledmg *= player.meledmgmult
                            wep.melefr *= player.melefrmult

                            perkweps.append(wep)
                            break
                    else:
                        weps.append(wep)
                allweps = perkweps + weps
                #number = 0
                while True:
                    print('=====')
                    print('Money: %s' %(player.money))
                    print()
                    print('Current gun:')
                    self.printgundata(player.gun)
                    print()
                    print('Perk guns:')
                    x = 0
                    for item in perkweps:
                        print('%s/%s' %(x, item.name))
                        x += 1
                    print()
                    print('Off-perk guns:')
                    for item in weps:
                        print('%s/%s' %(x, item.name))
                        x += 1
                    print()
                    print('Enter number of gun to look at it')
                    print('Enter %s to go back' %(len(allweps)))
                    choise = ch(0, len(allweps))
                    if type(choise) == bool:
                        print('invalid choise')
                        continue
                    elif choise == len(allweps):
                        break
                    else:
                        choosengun = allweps[choise]
                        while True:
                            print('=====')
                            print('Money: %s' %(player.money))
                            print()
                            print('Current gun:')
                            self.printgundata(player.gun)
                            print()
                            print('Choosen gun:')
                            self.printgundata(choosengun)
                            print('Enter 0 to buy the gun')
                            print('Enter 1 to go back')
                            choise = ch(0,1)
                            if type(choise) == bool:
                                print('invalid choise')
                            elif choise == 0:
                                if player.money < choosengun.cost:
                                    print('You dont have enough money')
                                else:
                                    player.money += int(player.gun.cost/2.5)
                                    player.gun.ammo = 0
                                    player.gun.clip = 0
                                    player.gun.rlding = False
                                    player.gun = copy.deepcopy(choosengun)
                                    player.money -= choosengun.cost
                                    break
                            elif choise == 1:
                                break
            elif choise == 2:
                while True:
                    print('=====')
                    print('Money: %s' %(player.money))
                    print('Ammo: %s/%s' %(player.gun.ammo, player.gun.ammomax))
                    print('Clip: %s bullets / %s $' %(player.gun.clipmax, player.gun.clipcost))
                    print()
                    print('1/Buy 1 clip')
                    print('2/Go back')
                    choise = ch(1,2)
                    if choise == False:
                        continue
                    elif choise == 1:
                        if player.money >= player.gun.clipcost:
                            if player.gun.ammo < player.gun.ammomax:
                                player.money -= player.gun.clipcost
                                player.gun.ammo += player.gun.clipmax
                            else: print('You cant carry any more ammo')
                        else: print('You dont have enough money')
                    elif choise == 2:
                        break
            elif choise == 3:
                print('Go Fuck Yourself')
            elif choise == 4:
                break
            
shop = shop()

class hud():
    y = 0
    def addtext(self, text, size=30):
        msg(text, 0, self.y, size)
        self.y += size
    def draw(self):
        self.addtext('FPS:%s' %(int(fps.get())))
        self.addtext('Class:%s' %(player.name))
        self.addtext('HP:%s/%s' %(player.hp, player.hpmax))
        self.addtext('Money:%s' %(player.money))
        self.addtext('Radar:%s' %(int(rast(player.x, player.y, MAP.end[0], MAP.end[1]))))
        self.addtext('XP:%s' %(int(player.xp)))
        self.addtext('')
        self.addtext('Weapon:%s' %(player.gun.name))
        self.addtext('%s/%s' %(player.gun.clip, player.gun.ammo))
        self.addtext(player.gun.rldat - time.time() if player.gun.rlding else '')
        self.addtext((player.gun.melefrat - time.time()) if (player.gun.melefrat - time.time() > 0) else '')
        self.addtext('')
        self.addtext('%s ; %s' %(int(player.x), int(player.y)))
        self.addtext(len(bullets.x))
        self.addtext(len(enemies.x))
        self.addtext('')
        self.addtext(int(MAP.gettime()))
        
        self.y = 0
hud = hud()

class enemyspawns():
    x = []
    y = []
    nextspawn = []
    cd = 2
    d = 20
    def main(self):
        if fps.get() > 60:
            for x in range(len(self.x)):
                #if rast(self.x[x], self.y[x], player.x, player.y) < player.detectrange and self.nextspawn[x] <= time.time():
                if player.inrange(self.x[x], self.y[x]) and self.nextspawn[x] <= time.time():
                    #enemies.add(self.x[x], self.y[x], random.randint(10, 30), random.randint(1, 4), random.randint(1, 20), random.randint(1, 10))
                    for item in zombies.al:
                        if random.random() < 0.6:
                            enemies.add(self.x[x], self.y[x], item.d, item.speed, item.hp, item.dmg, item.color)
                            break
                    else:
                        enemies.add(self.x[x], self.y[x], item.d, item.speed, item.hp, item.dmg, item.color)
                    self.nextspawn[x] = time.time() + self.cd
        #else:
        #    for x in range(len(enemies.x)-1, -1, -1):
        #        if not player.inrange(enemies.x[x], enemies.y[x]):
        #            enemies.rem(x)
    def add(self, x ,y):
        self.x.append(x)
        self.y.append(y)
        self.nextspawn.append(0)
    def rem(self, number):
        del self.x[number]
        del self.y[number]
        del self.nextspawn[number]
    def remall(self):
        for x in range(len(self.x)):
            self.rem(0)
    def draw(self):
        for x in range(len(self.x)):
            if doko(camera.x, camera.y, screenx, screeny, self.x[x], self.y[x], self.d, self.d):
                pygame.draw.rect(screen, yellow, (self.x[x] - camera.x, self.y[x] - camera.y, self.d, self.d))
enemyspawns = enemyspawns()

class enemies():
    x = []
    y = []
    d = []
    speed = []
    hp = []
    hpmax = []
    dmg = []
    color = []
    stunend = []
    ar = 1
    def damage(self, number, damage):
        self.hp[number] -= damage
        if self.hp[number] <= 0:
            formula = self.dmg[number] * self.speed[number] * self.hpmax[number]
            player.xp += formula
            player.money += formula * 0.1
            self.rem(number)
    def collision(self):
        for x in range(len(self.x)-1,-1,-1):
            if self.stunend[x] < time.time() and doko(player.x, player.y, player.d, player.d, self.x[x], self.y[x], self.d[x], self.d[x]):
                player.damage(self.dmg[x])
                self.move(-1)
                self.stunend[x] = time.time() + self.ar
    def move(self, atplayer=1):
        for x in range(len(self.x)):
            if self.stunend[x] < time.time():
                [movx, movy] = getchange(self.x[x] + (self.d[x]/2), self.y[x] + (self.d[x]/2), player.x + (player.d/2), player.y + (player.d/2))
                movx *= self.speed[x]
                movy *= self.speed[x]
                    
                if self.dokowall(x):
                    movx /= 3
                    movy /= 3

                self.x[x] += movx*atplayer
                self.y[x] += movy*atplayer
    def dokowall(self, number):
        #for x in range(len(walls.x)):
        for x in walls.getvisible():
            if doko(self.x[number], self.y[number], self.d[number], self.d[number], walls.x[x], walls.y[x], walls.dx[x], walls.dy[x]):
                return True
        return False
    def add(self, x ,y ,d ,speed, hp, dmg, color):
        self.x.append(x)
        self.y.append(y)
        self.d.append(d)
        self.speed.append(speed)
        self.hp.append(hp)
        self.hpmax.append(copy.deepcopy(hp))
        self.dmg.append(dmg)
        self.color.append(color)
        self.stunend.append(0)
    def rem(self, number):
        del self.x[number]
        del self.y[number]
        del self.d[number]
        del self.speed[number]
        del self.hp[number]
        del self.hpmax[number]
        del self.dmg[number]
        del self.color[number]
        del self.stunend[number]
    def remall(self):
        for x in range(len(self.x)):
            self.rem(0)
    def draw(self):
        for x in range(len(self.x)):
            if doko(camera.x, camera.y, screenx, screeny, self.x[x], self.y[x], self.d[x], self.d[x]):
                #pygame.draw.rect(screen, red, (self.x[x] - camera.x, self.y[x] - camera.y, self.d[x], self.d[x]))
                pygame.draw.rect(screen, self.color[x], (self.x[x] - camera.x, self.y[x] - camera.y, self.d[x], self.d[x]))
                msg(self.hp[x], self.x[x] - camera.x, self.y[x] - camera.y)
enemies = enemies()

class walls():
    x = []
    y = []
    dx = []
    dy = []
    hp = []
    visible = []
    color = black
    wallwithhpcolor = (188,143,143)
    def damage(self, number, damage):
        self.hp[number] -= damage
        if self.hp[number] <= 0:
            self.rem(number)
    def refreshvisible(self):
        self.visible = []
        for x in range(len(self.x)):
            if doko(camera.x-player.speed, camera.y-player.speed, screenx+(player.speed*2), screeny+(player.speed*2), self.x[x], self.y[x], self.dx[x], self.dy[x]):
                self.visible.append(x)
    def getvisible(self):
        return self.visible
    def add(self, x, y, dx, dy, hp):
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
    def draw(self):
        #for x in range(len(self.x)):
        for x in self.getvisible():
            if doko(camera.x, camera.y, screenx, screeny, self.x[x], self.y[x], self.dx[x], self.dy[x]):
                if self.hp[x] == None:
                    pygame.draw.rect(screen, self.color, (self.x[x] - camera.x, self.y[x] - camera.y, self.dx[x], self.dy[x]))
                else:
                    pygame.draw.rect(screen, self.wallwithhpcolor, (self.x[x] - camera.x, self.y[x] - camera.y, self.dx[x], self.dy[x]))
                    #msg(self.hp[x], self.x[x]-camera.x, self.y[x]-camera.y)
walls = walls()

class sentry():
    color = (100,100,0)
    x = []
    y = []
    d = 40
    bulletd = 10
    frat = []#
    fr = []
    dmg = []
    radius = []
    remafter = 5
    speed = []
    def place(self):
        self.x.append(player.x)
        self.y.append(player.y)
        self.frat.append(0)
        self.fr.append(0.4)
        self.dmg.append(4)
        self.radius.append(300)
        self.speed.append(7)
    def upgrade(self, number):
        pass
    def shoot(self):
        for x in range(len(self.x)):
            if self.frat[x] <= time.time():
                for y in range(len(enemies.x)):
                    if rast(self.x[x], self.y[x], enemies.x[y], enemies.y[y]) <= self.radius[x]:
                        self.frat[x] = self.fr[x] + time.time()
                        CHANGE = getchange(self.x[x]+(self.d/2), self.y[x]+(self.d/2), enemies.x[y]+(enemies.d[y]/2), enemies.y[y]+(enemies.d[y]/2))
                        for a in [0,1]: CHANGE[a] = CHANGE[a] * self.speed[x]
                        bullets.add(self.x[x]+(self.d/2), self.y[x]+(self.d/2), self.bulletd, CHANGE, self.dmg[x], self.remafter+time.time(), 0)
                        self.upgrade(x)
                        break
    def draw(self):
        for x in range(len(self.x)):
            if doko(camera.x, camera.y, screenx, screeny, self.x[x], self.y[x], self.d, self.d):
                pygame.draw.circle(screen, self.color, (int(self.x[x]+(self.d/2)-camera.x), int(self.y[x]+(self.d/2)-camera.y)), self.radius[x], 3)
                pygame.draw.rect(screen, self.color, (self.x[x] - camera.x, self.y[x] - camera.y, self.d, self.d))
sentry = sentry()

class bullets():
    x = []
    y = []
    d = []
    change = []
    dmg = []
    remat = []
    explrad = []
    def collision(self):
        for x in range(len(self.x)-1,-1,-1):
            for y in range(len(enemies.x)-1, -1, -1):
                if doko(self.x[x], self.y[x], self.d[x], self.d[x], enemies.x[y], enemies.y[y], enemies.d[y], enemies.d[y]):
                    enemies.damage(y, self.dmg[x])
                    for z in range(len(enemies.x)-1,-1,-1):
                        rastoqnie = rast(self.x[x]+self.d[x]/2, self.y[x]+self.d[x]/2, enemies.x[z]+enemies.d[z]/2, enemies.y[z]+enemies.d[z]/2)
                        if rastoqnie < self.explrad[x]:
                            enemies.damage(z, self.dmg[x]*((self.explrad[x]-rastoqnie)/self.explrad[x]))
                    self.rem(x)
                    break
            else:
                #for y in range(len(walls.x)):
                for y in walls.getvisible():
                #for y in (walls.getvisible() if self.explrad[x] > 0 else range(len(walls.x))):
                    if doko(self.x[x], self.y[x], self.d[x], self.d[x], walls.x[y], walls.y[y], walls.dx[y], walls.dy[y]):
                        if self.explrad != 0:
                            for z in range(len(enemies.x)-1,-1,-1):
                                rastoqnie = rast(self.x[x]+self.d[x]/2, self.y[x]+self.d[x]/2, enemies.x[z]+enemies.d[z]/2, enemies.y[z]+enemies.d[z]/2)
                                if rastoqnie < self.explrad[x]:
                                    enemies.damage(z, self.dmg[x]*(self.explrad[x]/rastoqnie))
                            if walls.hp[y] != None: walls.damage(y, self.dmg[x]*2)
                        else:
                            if walls.hp[y] != None: walls.damage(y, self.dmg[x])
                        self.rem(x)
                        break
                else:
                    if self.remat[x] < time.time():
                        self.rem(x)
                    #    break
                    #if doko(camera.x, camera.y, screenx, screeny, self.x[x], self.y[x], self.d[x], self.d[x]):
                    #    self.rem(x)
    def move(self):
        for x in range(len(self.x)):
            self.x[x] += self.change[x][0]
            self.y[x] += self.change[x][1]
    def remall(self):
        for x in range(len(self.x)):
            self.rem(0)
    def add(self, x, y, d, change, dmg, remat, explrad):
        self.x.append(x)
        self.y.append(y)
        self.d.append(d)
        self.change.append(change)
        self.dmg.append(dmg)
        self.remat.append(remat)
        self.explrad.append(explrad)
    def rem(self, number):
        del self.x[number]
        del self.y[number]
        del self.d[number]
        del self.change[number]
        del self.dmg[number]
        del self.remat[number]
        del self.explrad[number]
    def draw(self):
        for x in range(len(self.x)):
            if doko(camera.x, camera.y, screenx, screeny, self.x[x], self.y[x], self.d[x], self.d[x]):
                pygame.draw.rect(screen, yellow, (self.x[x] - camera.x, self.y[x] - camera.y, self.d[x], self.d[x]))
bullets = bullets()

class traders():
    x = []
    y = []
    d = 20
    color = (0,0,255)
    def main(self):
        shop.main()
    def add(self, x, y):
        self.x.append(x)
        self.y.append(y)
    def remall(self):
        for x in range(len(self.x)):
            self.rem(0)
    def rem(self, number):
        del self.x[number]
        del self.y[number]
    def draw(self):
        for x in range(len(self.x)):
            pygame.draw.rect(screen, self.color, (self.x[x]-camera.x, self.y[x]-camera.y, self.d, self.d))
traders = traders()        

class player():
    movea = 0
    moves = 0
    moved = 0
    movew = 0
    movex = 0
    movey = 0
    holdm1 = False
    color = green
    #x = 500
    #y = 300
    d = 30
    money = 8000
    #gun = None
    def use(self):
        for x in range(len(traders.x)):
            if doko(player.x, player.y, player.d, player.d, traders.x[x], traders.y[x], traders.d, traders.d):
                traders.main()
                break
    def inrange(self, x, y):
        return rast(self.x, self.y, x, y) < self.detectrange
    def loadxp(self):
        try:
            f = open('data.txt', 'r')
        except FileNotFoundError:
            self.xp = 0
            return None
        fcont = list(f.read())
        f.close()
        for x in range(len(fcont)):
            fcont[x] = chr(ord(fcont[x])+30)
        self.xp = int(''.join(fcont))
    def savexp(self):
        f = open('data.txt', 'w')
        for char in str(int(self.xp)):
            f.write(chr(ord(char)-30))
        f.close()
    def usemele(self):
        if self.gun.melefrat <= time.time():
            #bullets.add
            change = getchange(player.x, player.y, cur[0], cur[1])
            change[0] = (change[0])*self.gun.melespeed
            change[1] = (change[1])*self.gun.melespeed
            bullets.add(self.x+(self.d/2)-(self.gun.meled/2), self.y+(self.d/2)-(self.gun.meled/2), self.gun.meled, change, self.gun.meledmg, 0, 0)
            self.gun.melefrat = time.time() + self.gun.melefr
    def shoot(self):
        if self.gun.rldat < time.time() or (self.gun.rldt == 'one' and self.gun.clip != 0):
            self.gun.rlding = False
            if self.gun.clip > 0 or self.gun.rldt == 'mele':
                if self.gun.frat <= time.time():
                    self.gun.firesound.play()
                    #pygame.mixer.Sound.play(self.gun.firesound)
                    #pygame.mixer.Channel.play(self.gun.firesound)
                    changeoriginal = getchange(player.x, player.y, cur[0], cur[1])
                    for x in range(self.gun.bps):
                        recoil = random.uniform(-player.gun.inacc, player.gun.inacc)
                        change = [0,0]
                        change[0] = (changeoriginal[0]+recoil)*self.gun.speed
                        change[1] = (changeoriginal[1]-recoil)*self.gun.speed
                        bullets.add(self.x + (self.d/2) - (self.gun.d/2), self.y + (self.d/2) - (self.gun.d/2), self.gun.d, change, self.gun.dmg, time.time() + self.gun.remat, self.gun.explrad)

                    if self.gun.frt == 'semi':
                        self.holdm1 = False
                    
                    self.gun.clip -= 1
                    self.gun.frat = time.time() + self.gun.fr
            else:
                if self.gun.ammo > 0: self.reload()
    def reload(self):
        if self.gun.clip != self.gun.clipmax and self.gun.rlding == False and self.gun.ammo > 0:
            self.gun.rlding = True
            self.gun.rldat = time.time() + self.gun.rl
    def damage(self, amount):
        self.hp -= amount
    def dokowall(self):
        #for x in range(len(walls.x)):
        for x in walls.getvisible():
            if doko(self.x, self.y, self.d, self.d, walls.x[x], walls.y[x], walls.dx[x], walls.dy[x]):
                return True
        return False
    def dokoenemy(self):
        for x in range(len(enemies.x)):
            if doko(self.x, self.y, self.d, self.d, enemies.x[x], enemies.y[x], enemies.d[x], enemies.d[x]):
                return True
        return False
    def changeclass(self, klas=None):
        if klas != None:
            for item in dir(klas):
                if item[0] != '_':
                    exec('self.%s = klas.%s' %(item, item))
            return None
        openconsolemsg()
        while True:
            print('==========')
            print('Choose a class')
            print()
            for x, item in enumerate(perks.al):
                print('%s: %s\n -%s' %(x, item.name, item.desc))
                print()
            choise = ch(0, len(perks.al)-1)
            if type(choise) == bool:
                print('invalid choise')
                continue
            else:
                self.changeclass(copy.deepcopy(perks.al[choise]))
                break
    def respawn(self):
        self.changeclass()
        self.gun = copy.deepcopy(guns.al[-1])
        self.gun.ammo = copy.deepcopy(player.gun.ammomax)
        self.hp = copy.deepcopy(self.hpmax)
        [self.x, self.y] = MAP.spawn
        camera.focusonplayer()
    def move(self):
        if self.movex != 0:
            self.x += self.movex
            if self.dokowall() or self.dokoenemy():
                self.x -= self.movex
            if player.x-camera.x-screenx+player.d > 0:
                player.x = camera.x+screenx-player.d
            elif player.x-camera.x < 0:
                player.x = camera.x      
        if self.movey != 0:
            self.y += self.movey
            if self.dokowall() or self.dokoenemy():
                self.y -= self.movey
            if player.y-camera.y-screeny+player.d > 0:
                player.y = camera.y+screeny-player.d
            elif player.y-camera.y < 0:
                player.y = camera.y  

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x - camera.x, self.y - camera.y, self.d, self.d))
player = player()

def main():
    global cur

    for x in range(len(guns.al)):
        guns.al[x].firesound = pygame.mixer.Sound( os.path.join('sounds', 'fire', guns.al[x].firesound))
        

    player.loadxp()
    MAP.changelevel()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player.savexp()
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
                elif event.key == pygame.K_r:
                    player.reload()
                elif event.key == pygame.K_q:
                    player.holdm1 = True
                elif event.key == pygame.K_SPACE:
                    camera.focusonplayer()
                elif event.key == pygame.K_0:
                    MAP.changelevel()
                elif event.key == pygame.K_e:
                    player.use()
                elif event.key == pygame.K_f:
                    player.usemele()
                elif event.key == pygame.K_g:
                    sentry.place()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.movea = 0
                elif event.key == pygame.K_d:
                    player.moved = 0
                elif event.key == pygame.K_s:
                    player.moves = 0
                elif event.key == pygame.K_w:
                    player.movew = 0
                elif event.key == pygame.K_q:
                    player.holdm1 = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.holdm1 = True
                elif event.button == 3:
                    player.usemele()

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    player.holdm1 = False

        if doko(player.x, player.y, player.d, player.d, MAP.end[0], MAP.end[1], MAP.endd, MAP.endd):
            openconsolemsg()
            print('=====')
            print('You Succ Escaped "%s" in %s seconds' %(MAP.name, MAP.gettime()))
            print('=====')
            player.savexp()
            MAP.changelevel()

        if player.hp < 0:
            openconsolemsg()
            print('=====')
            print('You Died')
            print('Time wasted: %s seconds' %(MAP.gettime()))
            print('=====')
            player.loadxp()
            MAP.changelevel()

        walls.refreshvisible()

        cur = list(pygame.mouse.get_pos())
        cur[0] += camera.x
        cur[1] += camera.y
        
        if player.gun.rlding:
            if player.gun.rldat <= time.time():
                if player.gun.rldt == 'all':
                    player.gun.rlding = False
                    if player.gun.ammo > player.gun.clipmax:
                        player.gun.ammo -= player.gun.clipmax - player.gun.clip
                        player.gun.clip = copy.deepcopy(player.gun.clipmax)
                    else:
                        player.gun.clip = copy.deepcopy(player.gun.ammo)
                        player.gun.ammo = 0
                else:
                    if player.gun.ammo > 0:
                        player.gun.ammo -= 1
                        player.gun.clip += 1
                        player.gun.rldat = time.time() + player.gun.rl
                        if player.gun.clip == player.gun.clipmax:
                            player.gun.rlding = False
                    else:
                        player.gun.rlding = False

        if player.holdm1:
            player.shoot()

        sentry.shoot()

        player.movex = player.moved - player.movea
        player.movey = player.moves - player.movew
        player.move()

        camera.followplayer()

        bullets.move()
        bullets.collision()

        enemies.move()
        enemies.collision()
        
        enemyspawns.main()


        screen.fill(white)

        walls.draw()
        player.draw()
        traders.draw()
        sentry.draw()
        enemyspawns.draw()
        enemies.draw()
        MAP.drawend()
        bullets.draw()
        hud.draw()
        
        pygame.display.update()
        clock.tick(FPS)
        fps.count()

if __name__ == '__main__':
    main()

gameversion = '0.5.14'
print(gameversion)
import copy
import os
import pygame
import random

import stuff
from net import net

from beyblades import beyblades as allBeyblades
from colors import *

def rast(x1,y1,x2,y2):
	return (abs(x1-x2)**2+abs(y1-y2)**2)**0.5

getchange = stuff.getchange

def getchangetosplit(x1,y1,d1,x2,y2,d2):
	nabito = -rast(x1,y1,x2,y2)+d1+d2
	cx,cy = getchange(x2,y2,x1,y1)
	return cx*nabito,cy*nabito

f = open('settings.txt','r')
resolution = f.readline()
fullscreen = f.readline()
opponentip = f.readline()
f.close()
resolution = int(resolution.split('#')[0])
fullscreen = fullscreen.split('#')[0]
opponentip = opponentip.split('#')[0]
framespersecond = 60

class draw():
	baseres = 800
	formula = resolution/baseres
	textsizey = 20
	#printy
	printcolor = copy.deepcopy(GREEN)
	def __init__(self):
		self.myfont = pygame.font.SysFont('monospace',int(self.f(self.textsizey)))	
	def circle(self,color,x,y,d):
		pygame.draw.circle(screen,color,(int(self.f(x)),int(self.f(y))),int(self.f(d)))
	def f(self,num):
		return num*self.formula
	def print(self,msg):
		self.text(msg,0,self.printy,self.printcolor)
		self.printy += self.textsizey
	def rect(self,color,x,y,dx,dy):
		pygame.draw.rect(screen,color,(self.f(x),self.f(y),self.f(dx),self.f(dy)))
	def startprint(self,y,color=GREEN):
		self.printy = y
		self.printcolor = color
	def text(self,message,x,y,color=GREEN):
		label = draw.myfont.render(message,0,color)
		screen.blit(label,(draw.f(x),draw.f(y)))

class map():
	d = 400
	gravityforce = 0.0003
	def collision(self,x,y,d):
		return rast(400,400,x,y)+d>=self.d
	def gravity_func(self,player):
		rast_player = rast(player.x,player.y,400,400)
		changex,changey = getchange(player.x,player.y,400,400)
		player.velx += changex*self.gravityforce*player.arenaGravityMultiplier*rast_player
		player.vely += changey*self.gravityforce*player.arenaGravityMultiplier*rast_player
map = map()

pygame.init()
draw = draw()
clock = pygame.time.Clock()
if fullscreen=='True':
	screen = pygame.display.set_mode((resolution,resolution),pygame.FULLSCREEN)
else:
	screen = pygame.display.set_mode((resolution,resolution))
del resolution,fullscreen

def chooseGamemode():
	def gamemode_check_end_func(player,enemy):
		if player.hp <= 0:
			return 'You loose'
		if enemy.hp <= 0:
			return 'You win'
	def gamemode_collision_func(player,enemy):#...
		cx,cy = getchangetosplit(player.x,player.y,player.d,enemy.x,enemy.y,enemy.d)
		player.x += cx
		player.y += cy

		player.hp -= (abs(enemy.velx)+abs(enemy.vely))*player.recvDamageMultiplier*enemy.giveDamageMultiplier
		player_velx_old = player.velx
		player_vely_old = player.vely
		player.velx = enemy.velx*player.recvKnockbackMultiplier*enemy.giveKnockbackMultiplier
		player.vely = enemy.vely*player.recvKnockbackMultiplier*enemy.giveKnockbackMultiplier
		#enemy.x = enemy.lastx
		#enemy.y = enemy.lasty
		cx,cy = getchangetosplit(enemy.x,enemy.y,enemy.d,player.x,player.y,player.d)
		enemy.x += cx
		enemy.y += cy

		enemy.hp -= (abs(player.velx)+abs(player.vely))*enemy.recvDamageMultiplier*player.giveDamageMultiplier
		enemy.velx = player_velx_old*player.giveKnockbackMultiplier*enemy.recvKnockbackMultiplier
		enemy.vely = player_vely_old*player.giveKnockbackMultiplier*enemy.recvKnockbackMultiplier
	def gamemode_map_collision_func(player):#...
		#if map.collision(player.x,player.y,player.d):
		rastoqnie = rast(player.x,player.y,400,400)
		if rastoqnie+player.d >= map.d:
			player.hp -= player.arenaDamageMultiplier*(abs(player.velx)+abs(player.vely))
			cx, cy = getchange(player.x,player.y,400,400)
			rastoqnie = rastoqnie - map.d + player.d
			cx,cy = cx*rastoqnie,cy*rastoqnie
			player.x += cx
			player.y += cy
			player.velx *= -player.arenaKnockbackMultiplier
			player.vely *= -player.arenaKnockbackMultiplier
	def gamemode_preplay_func():
		enemy = copy.deepcopy(random.choice(allBeyblades))
		enemy = enemy()
		enemy.adjustVel = lambda:enemy.adjustVelToObject(player)
		player = chooseBeyblade()()
		player.adjustVel = lambda:player.adjustVelToKeyboard()
		return player,enemy
	def gamemode_respawn_func(player,enemy):
		while True:
			player.x = draw.f(random.randint(0,800))
			player.y = draw.f(random.randint(0,800))
			if map.collision(player.x,player.y,player.d)==False:
				break
		player.hp = copy.deepcopy(player.maxHp)
		player.velx=player.vely=0
		player.apressed=player.spressed=player.dpressed=player.wpressed=False
		while True:
			enemy.x = draw.f(random.randint(0,800))
			enemy.y = draw.f(random.randint(0,800))
			if map.collision(enemy.x,enemy.y,enemy.d)==False:
				if rast(player.x,player.y,enemy.x,enemy.y)>player.d+enemy.d:
					break
		enemy.hp = copy.deepcopy(enemy.maxHp)
		enemy.velx=enemy.vely=0
		enemy.apressed=enemy.spressed=enemy.dpressed=enemy.wpressed=False
	while True:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_0: 
					pygame.quit();quit()
				elif event.key == pygame.K_1: pass
				elif event.key == pygame.K_2:
					def gamemode_check_end(player,enemy):
						if player.hp <=0:
							if enemy.hp <= 0:
								return 'draw'
							return 'player2 wins'
						if enemy.hp <= 0:
							return 'player1 wins'
					def gamemode_preplay_func():
						enemy = chooseBeyblade()()
						enemy.adjustVel = lambda:enemy.adjustVelToKeyboard()
						player = chooseBeyblade()()
						player.adjustVel = lambda:player.adjustVelToKeyboard()
						return player,enemy
				elif event.key == pygame.K_3:
					def gamemode_check_end_func(player,enemy):
						if player.hp <= 0:
							if player.hp < enemy.hp: return 'robot2 wins'
							if player.hp > enemy.hp: return 'robot1 wins'
						if enemy.hp <= 0:
							if enemy.hp < player.hp: return 'robot1 wins'
							if enemy.hp > player.hp: return 'robot2 wins'
					def gamemode_preplay_func():
						player = random.choice(allBeyblades)()
						player.adjustVel = lambda:player.adjustVelToObject(enemy)
						enemy = random.choice(allBeyblades)()
						enemy.adjustVel = lambda:enemy.adjustVelToObject(player)
						return player,enemy
				elif event.key == pygame.K_4:
					def gamemode_check_end(player,enemy):
						if player.hp <= 0:
							if player.hp < enemy.hp: return 'robot2 wins'
							elif player.hp > enemy.hp: return 'robot1 wins'
							else: return 'draw'
						if enemy.hp <= 0:
							if enemy.hp < player.hp: return 'robot1 wins'
							elif enemy.hp > player.hp: return 'robot2 wins'
							else: return 'draw'
					def gamemode_preplay_func():
						player = chooseBeyblade()()
						player.adjustVel = lambda:player.adjustVelToObject(enemy)
						enemy = chooseBeyblade()()
						enemy.adjustVel = lambda:enemy.adjustVelToObject(player)
						return player,enemy
				elif event.key == pygame.K_5:
					def gamemode_preplay_func():
						player = chooseBeyblade()()
						player.adjustVel = lambda:player.adjustVelToKeyboard()
						enemy = chooseBeyblade()()
						enemy.adjustVel = lambda:enemy.adjustVelToObject(player)
						return player,enemy
				elif event.key == pygame.K_6:
					def gamemode_preplay_func():
						player = allBeyblades[0]()
						if os.path.isfile('specialniqBeibleidNaAlex.pishka'):
							player = stuff.fileToObj(player,'specialniqBeibleidNaAlex.pishka')
						player.adjustVel = lambda:player.adjustVelToKeyboard()
						enemy = allBeyblades[0]()
						if os.path.isfile('specialniqProtivnikNaAlex.pishka'):
							enemy = stuff.fileToObj(enemy,'specialniqProtivnikNaAlex.pishka')
						enemy.adjustVel = lambda:enemy.adjustVelToObject(player)
						return player,enemy
					def gamemode_check_end_func(player,enemy):
						if player.hp <= 0:
							if os.path.isfile('specialniqProtivnikNaAlex.pishka'):
								os.remove('specialniqProtivnikNaAlex.pishka')
							player.upgrades = 0
							stuff.objToFile(player,'specialniqBeibleidNaAlex.pishka')
							return 'Umrq si'
						elif enemy.hp <= 0:

							upgradable = player.getupgradable()
							while len(upgradable)>3:
								del upgradable[random.randrange(len(upgradable))]
							done = False
							while not done:
								for event in pygame.event.get():
									if event.type == pygame.KEYDOWN:
										if event.key == pygame.K_0:
											choice = 0
										elif event.key == pygame.K_1:
											choice = 1
										elif event.key == pygame.K_2:
											choice = 2
										else:
											continue
										upgradable[choice]()
										done = True
										break
									elif event.type == pygame.QUIT:
										pygame.quit()
										quit()

								screen.fill(WHITE)
								draw.startprint(0)
								for x,item in enumerate(upgradable):
									draw.print('%s: %s'%(x,item.__name__))
								pygame.display.update()
								clock.tick(framespersecond)
							stuff.objToFile(player,'specialniqBeibleidNaAlex.pishka')
							upgradable = enemy.getupgradable()
							for x in range(player.upgrades):
								random.choice(upgradable)()
							stuff.objToFile(enemy,'specialniqProtivnikNaAlex.pishka')
							return 'pi6tki'
				elif event.key == pygame.K_7:
					def gamemode_preplay_func():
						player = chooseBeyblade()()
						player.adjustVel = lambda:player.adjustVelToKeyboard()
						def send_recv_data():
							self = player
							net.send('x',str(self.x))
							net.send('y',str(self.y))
							net.send('hp',str(self.hp))
							net.send('velx',str(self.velx))
							net.send('vely',str(self.vely))
						player.send_recv_data = copy.deepcopy(send_recv_data)
						net.close_all()
						net.set_ip(opponentip)
						
						net.listen('gameversion')
						net.listen('beybladename')
						net.listen('startgame')
						net.listen('x')
						net.listen('y')
						net.listen('hp')
						net.listen('velx')
						net.listen('vely')
						recived_game_version = False
						recived_beyblade_name = False
						recived_startgame = False
						screen.fill(BLACK)
						draw.startprint(0)
						draw.print('Connecting... Press enter to close')
						#pygame.display.update()
						while not (recived_game_version and recived_beyblade_name and recived_startgame):
							for event in pygame.event.get():
								if event.type == pygame.KEYDOWN:
									if event.key == pygame.K_RETURN:
										net.close_all()
										return False,False
							net.send('gameversion',str(gameversion))
							net.send('beybladename',str(player.name))
							if (recived_game_version and recived_beyblade_name):
								net.send('startgame','OK')
							
							pygame.display.update()
							clock.tick(0.5)

							if not recived_game_version:
								data = net.recv('gameversion')
								if data:
									#data = data[-1]
									if data == gameversion:
										recived_game_version = True
										draw.print('Recived game version')
									else:
										draw.print('ERROR:game versions do not match (%s)(%s)'%(gameversion,data))
										#return False,False
							if not recived_beyblade_name:
								data = net.recv('beybladename')
								if data:
									#data = data[-1]
									for beyblade in allBeyblades:
										if beyblade.name == data:
											recived_beyblade_name = True
											draw.print('Recived beyblade')
											break
									else:
										draw.print("ERROR:resivnatiq beibleid ne e v listata")
										#return False,False
							if not recived_startgame:
								data = net.recv('startgame')
								if data:
									if data=='OK':
										recived_startgame = True
										draw.print('Recived startgame')
									else:
										draw.print('ERROR: bad startgame (%s)'%(data))
						enemy = beyblade()
						net.close('gameversion')
						net.close('beybladename')
						net.close('startgame')
						def send_recv_data():
							self = enemy
							x = net.recv('x')
							if x:
								#x=x[-1]
								self.x = float(x)
							y = net.recv('y')
							if y:
								#y = y[-1]
								self.y = float(y)
							hp = net.recv('hp')
							if hp:
								#hp = hp[-1]
								self.hp = float(hp)
							velx = net.recv('velx')
							if velx:
								#velx = velx[-1]
								self.velx = float(velx)
							vely = net.recv('vely')
							if vely:
								#vely = vely[-1]
								self.vely = float(vely)
						enemy.send_recv_data = copy.deepcopy(send_recv_data)
						return player,enemy

				else:
					continue
				return [gamemode_check_end_func,
				gamemode_collision_func,
				gamemode_map_collision_func,
				gamemode_preplay_func,
				gamemode_respawn_func]
			elif event.type == pygame.QUIT:
				pygame.quit()
				quit()

		screen.fill(BLACK)
		draw.startprint(0,WHITE)
		draw.print('Choose gamemode')
		draw.print('0/quit game')
		draw.print('1/vs random bot/cuka6 si sre6tu kompa')
		draw.print('2/local/cuka6 si sre6tu 4ovek')
		draw.print('3/random bot vs random bot/gleda6 kak 2 bota igraqt')
		draw.print('4/choosen bot vs choosen bot/gleda6 kak 2 bota cukat')
		draw.print('5/vs choosen bot/cuka6 si sre6tu kompa')
		draw.print('6/tam prograsva6 si i si se bie6 mnogo')
		draw.print('7/online')
		pygame.display.update()
		clock.tick(framespersecond)
def chooseBeyblade():
	choosenBeyblade = 0
	while True:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					return copy.deepcopy(b)
				elif event.key == pygame.K_a:
					choosenBeyblade -= 1
					if choosenBeyblade < 0:
						choosenBeyblade = len(allBeyblades)-1
				elif event.key == pygame.K_d:
					choosenBeyblade += 1
					if choosenBeyblade == len(allBeyblades):
						choosenBeyblade = 0
			elif event.type == pygame.QUIT:
				pygame.quit()
				quit()

		b = copy.deepcopy(allBeyblades[choosenBeyblade])()
		screen.fill(b.color)
		draw.startprint(0,b.rcolor)
		draw.print('Name: %s'%(b.name))
		draw.print('Description: %s'%(b.desc))
		draw.print('Thiccness: %s'%(b.d))
		draw.print('Stamina loss: %s'%(b.hpLossOverTime))
		draw.print('Random movement: %s'%(b.randomMovement))
		draw.print('Acceleration: %s'%(b.speed))
		draw.print('Max speed: %s'%(b.maxVel))
		draw.print('Damage: %s'%(b.giveDamageMultiplier))
		draw.print('Damage vunerability: %s'%(b.recvDamageMultiplier))
		draw.print('Knockback: %s'%(b.giveKnockbackMultiplier))
		draw.print('Knockback vunerability: %s'%(b.recvKnockbackMultiplier))
		draw.print('Arena damage vunerability: %s'%(b.arenaDamageMultiplier))
		draw.print('Arena knockback vunerability: %s'%(b.arenaKnockbackMultiplier))
		draw.print('Arena gravity vunerability: %s'%(b.arenaGravityMultiplier))
		b = copy.deepcopy(allBeyblades[choosenBeyblade])
		pygame.display.update()
		clock.tick(framespersecond)


def gameLoop():
	player,enemy = gamemode_preplay_func()
	if player == enemy == False:return False
	gamemode_respawn_func(player,enemy)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a:
					player.apressed = True
				elif event.key == pygame.K_s:
					player.spressed = True
				elif event.key == pygame.K_d:
					player.dpressed = True
				elif event.key == pygame.K_w:
					player.wpressed = True
				elif event.key == pygame.K_LEFT:
					enemy.apressed = True
				elif event.key == pygame.K_DOWN:
					enemy.spressed = True
				elif event.key == pygame.K_RIGHT:
					enemy.dpressed = True
				elif event.key == pygame.K_UP:
					enemy.wpressed = True
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_a:
					player.apressed = False
				elif event.key == pygame.K_s:
					player.spressed = False
				elif event.key == pygame.K_d:
					player.dpressed = False
				elif event.key == pygame.K_w:
					player.wpressed = False
				elif event.key == pygame.K_LEFT:
					enemy.apressed = False
				elif event.key == pygame.K_DOWN:
					enemy.spressed = False
				elif event.key == pygame.K_RIGHT:
					enemy.dpressed = False
				elif event.key == pygame.K_UP:
					enemy.wpressed = False
			elif event.type == pygame.QUIT:
				pygame.quit()
				quit()

		for obj in [player,enemy]:
			obj.looseHpOverTime()
			obj.adjustVel()
			obj.random_movement_func()
			map.gravity_func(obj)
			gamemode_map_collision_func(obj)
			obj.adjustVelToMaxVel()
			obj.move()
			obj.send_recv_data()

		if rast(player.x,player.y,enemy.x,enemy.y) <= player.d+enemy.d:
			gamemode_collision_func(player,enemy)

		gameResult = gamemode_check_end_func(player,enemy)
		if gameResult:
			break

		enemy.saveLastPos()

		screen.fill(player.color)
		draw.circle(player.rcolor,400,400,map.d)

		draw.circle(enemy.rcolor,enemy.last_pos_x.pop(0),enemy.last_pos_y.pop(0),enemy.d)

		draw.rect(player.color,0,0,400*player.hp/player.maxHp,15)
		draw.rect(player.rcolor,0,15,400*player.hp/player.maxHp,15)
		draw.rect(player.color,0,30,400*(abs(player.velx)+abs(player.vely))/player.maxVel,15)
		draw.rect(player.rcolor,0,45,400*(abs(player.velx)+abs(player.vely))/player.maxVel,15)
		
		draw.rect(enemy.color,800,0,-400*enemy.hp/enemy.maxHp,15)
		draw.rect(enemy.color,800,30,-400*(abs(enemy.velx)+abs(enemy.vely))/enemy.maxVel,15)
		
		draw.circle(player.color,player.x,player.y,player.d)
		draw.circle(player.rcolor,player.x,player.y,player.d/2)
		draw.circle(player.color,player.x-(player.d/4)+(player.x/1600*player.d),player.y-(player.d/4)+((player.y/1600)*player.d),1)
		draw.circle(enemy.color,player.x-(player.d/4)+(enemy.x/1600*player.d),player.y-(player.d/4)+((enemy.y/1600)*player.d),1)

		draw.circle(enemy.color,enemy.x,enemy.y,enemy.d)
		pygame.display.update()
		clock.tick(framespersecond)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:return None
			elif event.type == pygame.QUIT: pygame.quit();quit()

		screen.fill(BLACK)

		draw.startprint(0,WHITE)
		draw.print(str(gameResult))
		draw.print('Press ENTER to continue')
		pygame.display.update()
		clock.tick(framespersecond)


while True:
	[gamemode_check_end_func,
	gamemode_collision_func,
	gamemode_map_collision_func,
	gamemode_preplay_func,
	gamemode_respawn_func] = chooseGamemode()
	gameLoop()

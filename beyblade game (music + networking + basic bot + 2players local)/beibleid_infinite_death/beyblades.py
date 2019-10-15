import copy
import random
from stuff import getchange

def adjToMax(x,y,m):
	avg=(abs(x)+abs(y))
	if avg==0:
		return 0,0
	return (x*m)/avg,(y*m)/avg

class b():
	name = 'ERROR'
	desc = 'ERROR'
	color=(0,255,0)

	hp=1000#
	velx = 0#
	vely = 0#

	d=40

	hpLossOverTime = 0.1
	randomMovement = 0.01

	speed = 0.04
	maxVel = 10

	giveDamageMultiplier = 6
	recvDamageMultiplier = 1

	giveKnockbackMultiplier = 1
	recvKnockbackMultiplier = 1

	arenaDamageMultiplier = 1
	arenaKnockbackMultiplier = 0.6
	arenaGravityMultiplier = 1

	upgrades = 0
	last_pos_x = [0]*30
	last_pos_y = [0]*30
	#apressed = False
	#spressed = False
	#dpressed = False
	#wpressed = False
	def __init__(self):
		self.maxHp = copy.deepcopy(self.hp)
		self.rcolor = tuple(255-x for x in self.color)
	def adjustVel(self):
		pass
	def adjustVelToMaxVel(self):
		if abs(self.velx)+abs(self.vely)>self.maxVel:
			self.velx,self.vely = adjToMax(self.velx,self.vely,self.maxVel)
	def adjustVelToKeyboard(self):
		changex = changey = 0
		if self.apressed:
			changex -= self.speed
		if self.spressed:
			changey += self.speed
		if self.dpressed:
			changex += self.speed
		if self.wpressed:
			changey -= self.speed
		changex,changey = adjToMax(changex,changey,self.speed)
		self.velx += changex
		self.vely += changey
	def adjustVelToObject(self,player):
		'''changex = changey = 0
		if self.x < player.x:
			changex += abs(self.speed)
		else:
			changex -= abs(self.speed)
		if self.y < player.y:
			changey += abs(self.speed)
		else:
			changey -= abs(self.speed)
		changex,changey = adjToMax(changex,changey,self.speed)'''
		changex,changey = getchange(self.x,self.y,player.x,player.y)
		self.velx+=changex*self.speed
		self.vely+=changey*self.speed
	def getupgradable(self):
		upgradable =[]
		for item in dir(self):
			if item[:8]=='upgrade_':
				if eval('type(self.%s).__name__'%(item))=='method':
					upgradable.append(eval('self.%s'%(item)))
		self.upgrades += 1
		return upgradable
	def looseHpOverTime(self):
		self.hp -= self.hpLossOverTime
	def move(self):
		self.x += self.velx
		self.y += self.vely
	def random_movement_func(self):
		cx,cy = adjToMax(random.random(),random.random(),self.randomMovement)
		self.velx += cx
		self.vely += cy
	def saveLastPos(self):
		self.last_pos_x.append(self.x)
		self.last_pos_y.append(self.y)
	def send_recv_data(self):
		pass
	def upgrade_change_color(self):
		self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
		self.rcolor = (255-x for x in self.color)
	def upgrade_maxHp(self):
		self.maxHp *= 1.01
	def upgrade_increase_d(self):
		self.d *= 1.01
	def upgrade_decrease_d(self):
		self.d /= 1.01
	def upgrade_decrease_hpLossOverTime(self):
		self.hpLossOverTime /= 1.01
	def upgrade_increase_randomMovement(self):
		self.randomMovement *= 1.01
	def upgrade_decrease_randomMovement(self):
		self.randomMovement /= 1.01
	def upgrade_speed(self):
		self.speed *= 1.01
	def upgrade_maxVel(self):
		self.maxVel *= 1.01
	def upgrade_giveDamageMultiplier(self):
		self.giveDamageMultiplier *= 1.01
	def upgrade_recvDamageMultiplier(self):
		self.recvDamageMultiplier /= 1.01
	def upgrade_increase_giveKnockbackMultiplier(self):
		self.giveKnockbackMultiplier *= 1.01
	def upgrade_decrease_giveKnockbackMultiplier(self):
		self.giveKnockbackMultiplier /= 1.01
	def upgrade_increase_recvKnockbackMultiplier(self):
		self.recvKnockbackMultiplier *= 1.01
	def upgrade_decrease_recvKnockbackMultiplier(self):
		self.recvKnockbackMultiplier /= 1.01
	def upgrade_arenaDamageMultiplier(self):
		self.arenaDamageMultiplier /= 1.01
	def upgrade_increase_arenaKnockbackMultiplier(self):
		self.arenaKnockbackMultiplier *= 1.01
	def upgrade_decrease_arenaKnockbackMultiplier(self):
		self.arenaKnockbackMultiplier /= 1.01
	def upgrade_increase_arenaGravityMultiplier(self):
		self.arenaGravityMultiplier *= 1.01
	def upgrade_decrease_arenaGravityMultiplier(self):
		self.arenaGravityMultiplier /= 1.01
beyblades = []

class a(b):
	name = 'Ni6to specialno'
	desc = 'Default beibleida'
beyblades.append(a)

class a(b):
	color=(0,0,255)
	name = 'lada'
	desc = 'Po bavno se zaburzva ama moje da stane po-burs'
	speed = 0.08
	maxVel = 12
beyblades.append(a)

class a(b):
	color=(255,255,0)
	name = 'nisan'
	desc = 'Po burzo se zaburzva ama e po-baven overall'
	speed = 0.12
	maxVel = 8
beyblades.append(a)

class a(b):
	color=(100,100,100)
	name = 'jip'
	desc = 'bie < demi4 ama buta pove4e'
	giveDamageMultiplier = 0.8
	giveKnockbackMultiplier = 1.2
beyblades.append(a)

class a(b):
	color = (123,123,123)
	name = 'deba'
	desc = 'mnogo lud'
	arenaKnockbackMultiplier = 8
	arenaDamageMultiplier = 0.2
beyblades.append(a)	

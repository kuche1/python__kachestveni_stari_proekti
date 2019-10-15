from colors import *
import settings

formula = 60/settings.FPS

class b():
    name = 'Gosho'
    color = green
    speed = 0.1 * formula
    randomness = 0.09 * formula
    privli4aneCentur = 0.09 * formula
    varteneMax = 100
    vartenePenalty = 0.0005 * formula
    arenaPenalty = 0.1
    enemyPenalty = 0.1
    otbluskvaneArena = 0.2
allBeyblades = []


class a(b):
	def __init__(self):
		self.name = 'Gosho'
		self.color = (100, 100, 100)
		self.speed *= 1
		self.randomness *= 1
		self.privli4aneCentur *= 1
		self.varteneMax *= 1
		self.vartenePenalty *= 1
		self.arenaPenalty *= 1
		self.enemyPenalty *= 1
		self.otbluskvaneArena *= 1
allBeyblades.append(a())

class a(b):
	def __init__(self):
		self.name = 'Atak klasik'
		self.color = red
		self.speed *= 1.2
		self.randomness *= 1.2
		self.privli4aneCentur *= 1
		self.varteneMax *= 1
		self.vartenePenalty *= 1.4
		self.arenaPenalty *= 0.8
		self.enemyPenalty *= 1
		self.otbluskvaneArena *= 1.2
allBeyblades.append(a())

class a(b):
	def __init__(self):
		self.name = 'Difens klasik'
		self.color = blue
		self.speed *= 0.6
		self.randomness *= 0.6
		self.privli4aneCentur *= 1
		self.varteneMax *= 1.2
		self.vartenePenalty *= 1.8
		self.arenaPenalty *= 0.6
		self.enemyPenalty *= 0.4
		self.otbluskvaneArena *= 1
allBeyblades.append(a())

class a(b):
	def __init__(self):
		self.name = 'Stamina klasik'
		self.color = green
		self.speed *= 1
		self.randomness *= 0.4
		self.privli4aneCentur *= 0.4
		self.varteneMax *= 1
		self.vartenePenalty *= 0.4
		self.arenaPenalty *= 1.2
		self.enemyPenalty *= 1.2
		self.otbluskvaneArena *= 1
allBeyblades.append(a())

class a(b):
	def __init__(self):
		self.name = 'Nqkav Deto E Mnogo Burs Ma Ima Malko Ei4 Pi'
		self.color = (100, 100, 100)
		self.speed *= 2
		self.randomness *= 3
		self.privli4aneCentur *= 2
		self.varteneMax *= 0.5
		self.vartenePenalty *= 1 
		self.arenaPenalty *= 1
		self.enemyPenalty *= 0.3
		self.otbluskvaneArena *= 1
allBeyblades.append(a())

class a(b):
	def __init__(self):
		self.name = 'nenormalen'
		self.color = (100, 100, 100)
		self.speed *= 0.9
		self.randomness *= 0.6
		self.privli4aneCentur *= 1.2
		self.varteneMax *= 1
		self.vartenePenalty *= 2
		self.arenaPenalty *= 1
		self.enemyPenalty *= -1
		self.otbluskvaneArena *= 1
allBeyblades.append(a())

class a(b):
	def __init__(self):
		self.name = 'takuv koito si poema mnou ataka za6tita stamina i atakata mu e golqma'
		self.color = (100, 255, 100)
		self.speed *= 0.5
		self.randomness *= 0.5
		self.privli4aneCentur *= 1.5
		self.varteneMax *= 0.2
		self.vartenePenalty *= -1
		self.arenaPenalty *= 5
		self.enemyPenalty *= 5
		self.otbluskvaneArena *= 5
allBeyblades.append(a())


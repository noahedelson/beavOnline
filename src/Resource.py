#from WorldObject import WorldObject, Position
from random import random as rand
from Structure import *
from Position import * 


resource_types 				= ['ore', 'gas']
cargospace_multipliers		= {'ore':1.0, 'gas':2.6}
RESOURCE_GROWTH_RATE = 1
MAX_RESOURCES = 1.4


class Resource(WorldObject):
	def __init__(self, type, sublocale, amount=1.0):
		WorldObject.__init__(self, sublocale)
		self.type   = type
		self.amount = amount
		
		if self.type=='RANDOM':
			self.type = resource_types[ int(rand() * len(resource_types))]
			if amount == 1.0: self.amount = rand() * 100
		self.cargospace = self.amount*cargospace_multipliers[self.type]

	def idle(self, deltaT):
		if self.amount < MAX_RESOURCES:
			self.amount += RESOURCE_GROWTH_RATE
	def makeFactory(self, sl):
		#position = Position(rand() % 1000, rand() % 1000, rand() % 1000)
		if self.type == 'ore': return NuclearOreRefinery(sl)
		if self.type == 'gas': return NuclearGasRefinery(sl)
		else: return Structure(Position(rand()*1000.0,rand()*1000.0))
		
	def radioIn(self):
		return ['resource ' + self.type + ' located: ' + str(self.amount)]
		
def random(sl):
	return Resource('RANDOM', sl)
		
		
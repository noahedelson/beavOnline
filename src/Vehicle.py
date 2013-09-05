from WorldObject import *
from Position import *
from random import random as rand
from Resource import * 
	
class Vehicle(WorldObject):
	def __init__(self, pilot, sublocale):
		WorldObject.__init__(self, sublocale, 'Vehicle')
		self.pilot = pilot
		self.goals = []
		self.startingPoint = 0
		self.cargoSpaceAvailable =  100
		self.cargoHold = []
		self.startingResources()  

	def getCargoAvailable(self):
		spaceAvail = self.cargoSpaceAvailable
		for item in self.cargoHold:
			spaceAvail -= item.cargospace
		return spaceAvail
	
	def startingResources(self):
		randomShit = random(self.sublocale)
		self.cargoHold.append( randomShit )
		
	def radioIn(self):
		return 'I am a vehicle'
			
	def getCapabilities(self):
		assert False, 'Class cannot be instantiated'
			
	def follow(self, ID): pass
	def dock(self, ID): pass
	def mine(self, ID): pass
	
	def navigate(self, targetLocation):
		self.state = 'NAVIGATING'
		self.goal  = targetLocation
		
		
class Freighter(Vehicle):
	def __init__(self, pilot, sublocale ):
		Vehicle.__init__(self, pilot, sublocale)
		self.storage_capcity = 1000.0

	def getCapabilities(self):
		return ['follow', 'dock']
	
	def radioIn(self):
		return 'I am a Freighter'
	def idle(self, deltaT):
		WorldObject.idle(self,deltaT)
		

class Miner(Vehicle):
	def __init__(self, pilot, sublocale ):
		Vehicle.__init__(self, pilot, sublocale)
		self.storage_capcity = 200.0
		self.goalMet = False

	def getCapabilities(self):
		return ['follow', 'dock', 'mine']
	
	def radioIn(self):
		return 'I am a Miner at local coordinates ' + self.position.toString()
		
	def idle(self, deltaT):
		WorldObject.idle(self,deltaT)
		if len(self.goals) > 0:
			print 'distance to goal: ' + str( self.goals[0].position.distance(self.position) )


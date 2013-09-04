from collections import deque
import pdb
from pdb import set_trace

WARNING_LEVEL = 0

class Actor:
	professions = ['miner', 'factory owner', 'police', 'pirate'] # scout, etc.
	def __init__(self, role, **kwargs):
		self.goals = []
		self.tasks = deque()
		self.highestSupply = 0
		self.highestDemand = 0
		self.activeVehicle = 0

	def setVehicle(self, vehicle):
		self.activeVehicle = vehicle
		self.capabilities  = vehicle.getCapabilities()
	def setRole(self, role):
		self.role = role
	
	def setProfession(self, profession):
		self.profession = profession 
		if profession == 'miner':
			self.activeTask = 'mine'
		
	def setPersonality(self, greed, cowardice, anger):		
		pass
		
	def getSalesPath(self):
		return self.activeVehicle.sublocale.getStationsSelling(self.activeVehicle.cargoHold)
		
	def follow(self):
		pass
	def mine(self):
		# starting point: flying through space, in their space-planes.
		self.startingPoint = self.activeVehicle.position  # TODO: will this be a shallow copy and hence I have a bug?
		if self.activeVehicle.getCargoAvailable() < 10.0: # less than 10 cubic meters of cargo left.. time to sell!
			goodGoal = self.getSalesPath()
		else:
			goodGoal = self.activeVehicle.sublocale.getNearestResource(self.activeVehicle.position)
			
		self.goals.append(goodGoal)
		self.halfwayPoint = self.startingPoint.plus(goodGoal.position.scale(0.5))
	
	def dock(self):
		pass
	def sell_cargo(self):
		pass
	def find_highest_supply(self):
		pass
	def find_highest_demand(self):
		self.findHighestDemand()
		
	def idle(self, deltaT=0.1):
		if self.goals != []:
			if self.halfwayPoint.distance(self.activeVehicle.position) > 1.0:
				self.activeVehicle.accelerate( self.goals[0].position )
			else:
				self.activeVehicle.velocity = self.activeVehicle.velocity.scale(0.7)
			
		if self.activeTask == 'find highest demand': self.findHighestDemand()
		if self.activeTask == 'find highest supply': self.findHighestSupply()
		if self.activeTask == 'follow': self.follow()
		if self.activeTask == 'mine': self.mine()
		if self.activeTask == 'dock': self.dock()
		if self.activeTask == 'sell cargo': self.sell_cargo()

	def findHighestDemand(self):
		self.activeVehicle.checkSector()
		radio_chat = self.activeVehicle.oldsector.getRadioChatter()
		for entry in radio_chat.split('\n'):
			if type(entry) == type([]):
				for subentry in entry.split(','):
					if WARNING_LEVEL >= 1: print 'evaluating subentry:' + str(subentry)
			if WARNING_LEVEL >= 1: print 'evaluating' + str(entry)
		if WARNING_LEVEL >= 1: print str(radio_chat)
		self.goal = 'find highest demand'
		#radio_chat = '' # getRadioChatter( vehicle.position ) 
		#acceptable_tasks = filter_by_buy_type(radio_chat, 
		# check radio chat, build list of 'I buy X', filter for ones that have $, ???
		
	def findHighestSupply(self, resource):
		self.goal = 'highestSupply'
		
	def getActiveTask(self):
		self.activeTask = self.tasks.popleft()
		print 'active task: ' + str(self.activeTask)
		
	def miner(self):
		self.tasks += ['find highest demand']
		self.tasks += ['find highest supply']
		self.tasks += ['follow']
		self.tasks += ['mine']
		self.tasks += ['dock']
		self.tasks += ['sell cargo']
		self.getActiveTask()

		

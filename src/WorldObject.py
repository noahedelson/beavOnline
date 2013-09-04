from Position import *
from random import random as rand
import Locale
import pdb
from pdb import set_trace

MAX_VELOCITY = 1.9
		
class WorldObject:
	def __init__(self, sublocale):
		self.sdc 				= 1
		self.mdc 				= 0
		self.sublocale 			= sublocale
		self.storage_capcity 	= 0
		self.storage_space		= 0
		self.active    			= True
		self.position  			= Position(rand() * 1000.0, rand() * 1000.0, rand() * 10.0) 
		self.velocity  			= Position(0.0, 0.0, 0.0)
		self.oldsector 			= 0
		self.mass      			= 1.0
		# position, velocity, mass 

	def RedoSector(self, oldsector):
		try:
			#print dir(oldsector.vehicles)
			self.oldsector.vehicles.remove(self)
			#oldsector.structures.remove(self)
		except:
			pass
			#print '.',
		self.oldsector = Locale.getOnly().getSectorFromXY(self.position.x,self.position.y)
	
	def checkSector(self):
		oldsector = self.oldsector
		if oldsector == 0:
			self.RedoSector(oldsector)
			return
		if self.position.x < 0.0: 	
			self.position.x += 1000.0
			self.RedoSector(oldsector)
		if self.position.y < 0.0: 
			self.position.y += 1000.0
			self.RedoSector(oldsector)
		if self.position.x > 1000.0: 
			self.position.x -= 1000.0
			self.RedoSector(oldsector)
		if self.position.y > 1000.0: 
			self.position.y -= 1000.0
			self.RedoSector(oldsector)
	
	def idle(self, deltaT):
		if not self.active: return
		self.position.x += self.velocity.x * deltaT;
		self.position.y += self.velocity.y * deltaT;
		self.position.z += self.velocity.z * deltaT;
		self.oldsector = 0 # sandbox.getSectorFromXY(self.position.x, self.position.y)
		self.checkSector()  # only need to call this occasionally.. optimize later
			
	def expire(self):
		self.active = False
			
	def takeDamage(self, sdc, mdc): # structural & mega-damage capacity
		if mdc > 0.0:
			self.mdc -= mdc
			if self.mdc < 0.0:
				self.expire()

	def accelerate(self, goal):
		factor = 0.01
		difference = Position( factor*(self.position.x-goal.x), factor*(self.position.y-goal.y), factor*(self.position.z-goal.z) )
		if difference.length() > MAX_VELOCITY:
			self.velocity.renormalize(MAX_VELOCITY)
			#print str(self.velocity.length())

		#difference = difference.renormalize(1.0)
		self.velocity.x += difference.x
		self.velocity.y += difference.y
		self.velocity.z += difference.z

from WorldObject import WorldObject
from Factory import Factory
from Position import * 
from time import time
from random import random as rand 

class effect(WorldObject):
	def __init__(self, sublocale, effectType, duration):
		WorldObject.__init__(self, sublocale, effectType)
		self.duration = duration
		
		
	def idle(self, deltaT): pass
		
	def radioIn(self): return ['bewm!']
		
	def renderMe(self): pass
		

class GroovyEffect(effect):
	def __init__(self, duration, position, sublocale):
		effect(sublocale, "GroovyEffect", duration)
		timeStart = time()
		print 'starting'
		
	def renderMe(self):
		glColor4f(1,1,1,1)
		for x in range(1,10):
			glutSolidSphere(sin(time() % 10.0) + float(x)/5.0, 20,20)
		
	def idle(self):
		if time() - timeStart >= duration:
			return false
		
		

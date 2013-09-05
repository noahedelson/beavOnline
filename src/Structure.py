from WorldObject import WorldObject
from Factory import Factory
from Position import * 
from random import random as rand 

class Structure(WorldObject):
	def __init__(self, sublocale):
		WorldObject.__init__(self, sublocale, 'Structure')
		self.ID       = ''
		self.produces = []
		self.consumes = []
		
	def idle(self, deltaT):
		pass
		
	def radioIn(self):
		radioStrings = ['I am a structure']
		for produce in self.produces: radioStrings.append(' I sell ' + str(produce))
		for consume in self.consumes: radioStrings.append(' I buy ' + str(consume))
		return radioStrings
		
class NuclearOreRefinery( Structure, Factory):
	def __init__(self, sl):
		Structure.__init__(self, sl)
		self.produces = ['metal beams']
		self.consumes = ['metals', 'isotopes', 'gas']
	
class NuclearGasRefinery( Structure, Factory ):
	def __init__(self, sl):
		Structure.__init__(self, sl)
		self.produces = ['hydrocarbons', 'nitrates']
		self.consumes = ['gas', 'isotopes']
	

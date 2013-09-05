#from WorldObject import WorldObject
from Resource import Resource
from Vehicle import *
from Actor import *
from effect import *
from random import random as rand
from time import time 

import Callbacks
from Callbacks import * 

try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print ''' Error PyOpenGL not installed properly!!'''
  sys.exit(  )


WORLD_SIZE = 3
MAX_RESOURCES_PER_SUBLOCALE = 5
UNIVERSAL_RESOURCE_UTILIZATION_FACTOR = 0.25
UNIVERSAL_SHIP_DENSITY = 2.4



only = []
def getOnly():
	global only
	return only
	

class Locale:
	def __init__(self):
		global only
		self.WORLD_SIZE = WORLD_SIZE 
		self.redSector  = 0
		self.zooming	= False
		self.zoomed		= False
		self.render = [True] * 10
		self.sl_torus = [x[:] for x in [[0]*WORLD_SIZE]*WORLD_SIZE]
		only = self
		for x in range(0,WORLD_SIZE):
		 for y in range(0,WORLD_SIZE):
		  sl = Sublocale(x,y) 
		  self.sl_torus[x][y] = sl

		for x in range(1,WORLD_SIZE-1):
		 for y in range(1,WORLD_SIZE-1):
		  sl = self.sl_torus[x][y]
		  sl.addNeighbor('EAST',  self.sl_torus[x+1][y])
		  sl.addNeighbor('WEST',  self.sl_torus[x-1][y])
		  sl.addNeighbor('NORTH', self.sl_torus[x][y+1])
		  sl.addNeighbor('SOUTH', self.sl_torus[x][y-1])
		  
		for x in range(1,WORLD_SIZE-1):
			self.sl_torus[x][0].addNeighbor( 'NORTH', self.sl_torus[x][WORLD_SIZE-1])
			self.sl_torus[x][WORLD_SIZE-1].addNeighbor( 'SOUTH', self.sl_torus[x][0])
		for y in range(1,WORLD_SIZE-1):
			self.sl_torus[0][y].addNeighbor( 'EAST', self.sl_torus[WORLD_SIZE-1][y])
			self.sl_torus[WORLD_SIZE-1][y].addNeighbor( 'WEST', self.sl_torus[0][y])

	def zoomTo(self, sector):
		self.zoomSector = sector
		self.zooming    = True
		self.zoomStart  = time()
		
	def zoomOut(self):
		self.zooming    = True
		self.zoomSector = 0
		self.zoomStart  = time()
		
			
	def renderGrid(self):
		#scale = 2.0/WORLD_SIZE
		glPushMatrix()
		#glTranslatef(-1.0,-1.0,0.0)	
		#glScalef(scale,scale,scale)
		glBegin(GL_LINES)
		glColor3f(0,1,0)
		for x in range(0,WORLD_SIZE):
		 for y in range(0,WORLD_SIZE):
			 glVertex2f(x,y)
			 glVertex2f(x,y+1)
			 glVertex2f(x+1,y)
			 glVertex2f(x,y)
		glEnd()
		glPopMatrix()
	
	def renderRedSector(self):
		for x in range(0,WORLD_SIZE):
			for y in range(0,WORLD_SIZE):
				sl = self.sl_torus[x][y]
				glPushMatrix()
				glTranslatef(x,y,0)
				if sl == self.redSector:
					glColor3f(1,0,0)
					glBegin(GL_LINES)
					glVertex2f(0,0)
					glVertex2f(1,1)
					glVertex2f(1,0)
					glVertex2f(0,1)
					glEnd()
				sl.renderGlobalMap(self.render)
				glPopMatrix()
	
			
	def renderGlobalMap(self):
		if not self.zooming and not self.zoomed:
			scale = 2.0/WORLD_SIZE
			glTranslatef(-1.0,-1.0,0.0)	
			glScalef(scale,scale,scale)
		if self.zooming and not self.zoomed:
			elapsed = time() - self.zoomStart
			if elapsed > 1.0:
				self.zooming = False
				self.zoomed  = True
			else:
				scale = 2.0/(float(WORLD_SIZE)-float(WORLD_SIZE)* elapsed)
				glTranslatef(-1.0 + elapsed * (self.zoomSector.x),-1.0 + elapsed * (self.zoomSector.x),0.0)	
				glScalef(scale,scale,scale)
		if self.zoomed:
			scale = 2.0
			glTranslatef(-1.0,-1.0,0.0)	
			glScalef(scale,scale,scale)

		self.renderGrid()
		self.renderRedSector()  # also renders sublocales
		self.renderVelocities()
		
	def renderVelocities(self):
		count = 0
		glColor4f(0,0,1,1)
		for x in range(0,WORLD_SIZE):
			for y in range(0,WORLD_SIZE):
				sl = self.sl_torus[x][y]
				for ship in sl.vehicles:
					magnitude = ship.velocity.length() + 0.5
					glBegin(GL_LINES)
					glVertex2f(-0.97, -0.9+float(count/100.0) ) 
					glVertex2f(-0.97+magnitude/10.0, -0.9+float(count/100.0) ) 
					glEnd()
					count += 1

	def getSectorFromXY(self, x, y):
		if 0.0 < x < 1000.0 and 0.0 < y < 1000.0: 
			return self.sl_torus[int(x*WORLD_SIZE/1000.0)][int(y*WORLD_SIZE/1000.0)]
		else:
			return self.sl_torus[0][0]
		
	def getSectorFromMouseXY(self,x,y):
		#print 'x,y' + str(x) + ' ' + str(y)
		if 0.0 < x < 1.0: #  and -1.0 > y > 0.0: 
			return self.sl_torus[int(x*WORLD_SIZE)][int(-y*WORLD_SIZE)-1]
		else:
			return self.sl_torus[0][0]
		
	def radioIn(self):	
		for x in range(1,WORLD_SIZE):
		 for y in range(1,WORLD_SIZE):
		  sl = self.sl_torus[x][y]
		  sl.radioIn()
	
	def idle(self, deltaT):
		for x in range(1,WORLD_SIZE):
		 for y in range(1,WORLD_SIZE):
		  sl = self.sl_torus[x][y]
		  sl.idle(deltaT)
		
class Sublocale:
	def __init__(self, x, y, **kwargs):
		self.neighbors = []
		self.vehicles   = []
		self.players    = []
		self.NPCs	    = []
		self.resources  = []
		self.structures = []
		self.actors     = []
		self.effects    = []
		self.x = x
		self.y = y
		self.radio  = []
		
		self.initRandomResources()
		self.initRandomStructures()
		self.initRandomVehicles()
		self.radioIn()
		
	def radioIn(self):
		self.radio = []
		for structure in self.structures: self.radio.append(structure.radioIn())
		for vehicle in self.vehicles:     self.radio.append(vehicle.radioIn())
		for resource in self.resources:   self.radio.append(resource.radioIn())
	
	def initRandomResources(self):
		for x in range(0, MAX_RESOURCES_PER_SUBLOCALE):
			Resource('RANDOM', self, rand() * 3.0 )
	def initRandomStructures(self):
		for resource in self.resources:
			if rand() < UNIVERSAL_RESOURCE_UTILIZATION_FACTOR:
				resource.makeFactory(self)
				
	''' includes actors '''
	def initRandomVehicles(self):
		for index in range(0, int(len(self.structures)*UNIVERSAL_SHIP_DENSITY)):
			pilot = Actor('miner')
			ship  = Miner(pilot, self)
			pilot.setVehicle(ship)
			pilot.setProfession('miner')
			self.actors.append(pilot)
		
	def getNearestResource(self, position):
		if len(self.resources) < 1: 
			return 0
		nearest = self.resources[0]
		dist = self.resources[0].position.distance(position)
		for res in self.resources:
			if res.position.distance(position) < dist:
				dist = res.position.distance(position)
				nearest = res
		#print 'nearest resource to ' + position.toString() + ' is ' + nearest.position.toString()
		return nearest

	def getStationsSelling(self, resourceList):
		stations_selling = []
		el = []
		for station in self.structures:
			el = station
			for resource_wanted in station.consumes:
				for cargoItem in resourceList:
					if cargoItem == resource_wanted:
						stations_selling.append(station)
					#print 'resource wanted ' + str(resource_wanted) + ' have: ' + str(cargoItem.type)
		if len(stations_selling) > 0:
			return stations_selling[0]  # for now, return the first one.  later this will be chosen more carefully
		else:
			return el  # go *somewhere* if you can't find people who want your resources.
	def addNeighbor(self, direction, neighbor):
		self.neighbors += (direction, neighbor)
		
	def getRadioChatter(self):
		retArr = [('SECTOR ' + str(self.x) + ":" + str(self.y) + ' REPORTING ' + str(len(self.radio)) + ' entries:\n')]
		for radioEntry in self.radio:
			retArr.append(str(radioEntry) + '\n')
		return retArr
		
	def idle(self, deltaT):
		for item in self.vehicles: 
			if not item.idle(deltaT):
				self.vehicles.remove(item)
		for item in self.structures: 
			if not item.idle(deltaT):
				self.structures.remove(item)
		for item in self.resources: 
			if not item.idle(deltaT):
				self.resources.remove(item)
		for item in self.actors: 
			if not item.idle(deltaT):
				self.actors.remove(item)
		for item in self.effects: 
			if not item.idle(deltaT):
				self.effects.remove(item)

		
	def renderWithColor(self, color, list, size=1.0):
		glColor4f(color[0],color[1],color[2], color[3])
		for item in list:
			try:
				size = item.amount
			except:
				pass
			glPushMatrix()		
			if hasattr(item, 'goals'):
				try:
					goal = item.goals[0]
				except:
					glScalef(0.001,0.001,0.001)
					glTranslated(item.position.x,item.position.y,item.position.z)
					glutSolidSphere(size/4.0, 6, 6)
					glPopMatrix()
					continue
				glBegin(GL_LINES)
				glColor3f(1,0,0)
				glVertex3f(item.position.x,item.position.y,item.position.z)
				glVertex3f(item.goals[0].position.x,item.goals[0].position.y,item.goals[0].position.z)
				glEnd()
			glScalef(0.001,0.001,0.001)
			glTranslated(item.position.x,item.position.y,item.position.z)
			glutSolidSphere(size, 6, 6)
			glPopMatrix()
		
	def renderGlobalMap(self, render):
		glPushMatrix()
		if render[2]: self.renderWithColor((0,0,1,1), self.structures, 30.0)
		if render[1]: self.renderWithColor((0,1,0.2,0.99), self.resources, 40.0)
		if render[0]: self.renderWithColor((1,0,0,1), self.vehicles, 40.1)
		glPopMatrix()
		
		for effect in self.effects:
			glPushMatrix()
			#set_trace()
			#glScalef(0.001,0.001,0.001)
			glTranslated(effect.position.x,effect.position.y,effect.position.z)
			effect.renderMe()
			glPopMatrix()

sandbox = Locale()

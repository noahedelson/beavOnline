from math import sqrt

class Position:

	def __init__(self,x,y,z=0.0):
		self.x = x
		self.y = y
		self.z = z
		
	def distance(self, position):
		xd = position.x-self.x
		yd = position.y-self.y
		zd = position.z-self.z
		dist = sqrt( xd*xd + yd*yd + zd*zd )
		return dist
	
	def scale(self,scalar):
		return Position(	self.x * scalar,
						self.y * scalar,
						self.z * scalar)
	
	def plus(self, x, y, z):
		return Position(self.x + x, self.y + y, self.z + z)
	def plus(self, pos):
		return Position(self.x + pos.x, self.y + pos.y, self.z + pos.z)

		
	def set(self, x,y,z):
		return Position(	self.x,self.y,self.z )
		
	def length(self):
		return self.distance(Position(0,0,0))
		
	def renormalize(self, length):
		eldist = self.distance(Position(0,0,0))
		self.x *= length
		self.y *= length
		self.z *= length
		self.x /= (eldist+0.1)
		self.y /= (eldist+0.1)
		self.z /= (eldist+0.1)
			
	def toString(self):
		return '(' + str(self.x) + ',' + str(self.y) + ',' + str(self.z) + ')'
			

	
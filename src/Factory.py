from WorldObject import WorldObject

#factory_types  = [ 	'metal refinery', 'silicon refinery', 'solar power plant', \
#					'orbital logistics station', 'hydroponics farm', \
#					'weapons plant', 'shipyard', 'metastation']  
		


class Factory(WorldObject):
	def defineInputs(self, inputs):
		self.inputs = inputs
	def defineOutputs(self, outputs):
		self.outputs = outputs
	def defineParamters(self, interval, rate ):
		self.interval 	= interval
		self.rate 		= rate

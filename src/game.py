#!/usr/bin/python2.7

import sys
try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print ''' Error PyOpenGL not installed properly!!'''
  sys.exit(  )

from pdb import set_trace  
from random import random as rand

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
WORLD_SIZE = 10		
MAX_RESOURCES_PER_SUBLOCALE = 3
UNIVERSAL_RESOURCE_UTILIZATION_FACTOR = 0.9
UNIVERSAL_SHIP_DENSITY = 0.5

WARNING_LEVEL = 0  #  0 = errors, 1 = warnings, 2 = log

factory_types  = [ 	'metal refinery', 'silicon refinery', 'solar power plant', \
					'orbital logistics station', 'hydroponics farm', \
					'weapons plant', 'shipyard', 'metastation']  
		
resource_types = ['ore', 'metals', 'silicon', 'isotopes', 'topsoil', 'water', 'power cells', 'protein paste']

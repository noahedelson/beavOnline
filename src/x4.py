#!/usr/bin/python2.7

import sys
try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print ''' Error PyOpenGL not installed properly!!'''
  sys.exit(  )

from random import random as rand
from Callbacks import *
import Locale
import Position
import Actor

mouse_coords = []

def registerCallbacks( ):
	"""Initialise glut settings concerning functions"""
	glutReshapeFunc( windowReshapeFunc )
	glutMouseFunc( mouseButton )
	glutMotionFunc( mouseMotion )
	glutKeyboardFunc( keyPressed )
	glutSpecialFunc( specialKeyPressed )
	glutDisplayFunc( display )
	glutIdleFunc( idle )

def init(  ):
	registerCallbacks( )
	glClearColor ( 0, 0, 0, 0 )
	glShadeModel( GL_SMOOTH )

def __main__():	
	glutInit( sys.argv )
	glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB )
	glutInitWindowSize( WIDTH, HEIGHT )
	glutInitWindowPosition( 100, 100 )
	glutCreateWindow( "Beav Online v.01a, eg Space-Tic-Tac-Toe" )
	init( )
	glutMainLoop(  )

if __name__ == "__main__": 
	__main__()

	

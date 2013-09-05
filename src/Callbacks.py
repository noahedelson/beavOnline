import Locale
import time
from time import clock

try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print ''' Error PyOpenGL not installed properly!!'''
  sys.exit(  )

  
WIDTH  = 640
HEIGHT = 480

label = ['ships', 'rsourcs', 'statns', 'trjct', ' grid',  ' fx ', ' XXX  ',  '  XYZ  ',  '  XXX  ',  '  XYZ  ']

report = ('no sector selected', 'click on a sector')

 
buttonState = 0
buttomMode  = 0
 
 
def mouseButton( button, mode, x, y ):	
	global sandbox, report, buttonState, buttonMode
	buttonState  = button
	buttonMode   = mode

	print button, mode
	if button ==  GLUT_LEFT_BUTTON: 
		sector = Locale.sandbox.getSectorFromMouseXY(float(x)/float(WIDTH),float(y)/float(HEIGHT))
		Locale.sandbox.redSector = sector 
		glutPostRedisplay( )
	if button ==  GLUT_RIGHT_BUTTON: 
		print 'getting radio chatter for sublocale: ' + str(float(x)) + ' ' +str(float(WIDTH)) + ' ' + str(y)  + ' '  + str(float(HEIGHT))
		print ' eg (' +str(float(x)/float(WIDTH)) +',' + str(float(y)/float(HEIGHT)) + ')'
		sector = Locale.sandbox.getSectorFromMouseXY(float(x)/float(WIDTH),float(y)/float(HEIGHT))
		Locale.sandbox.redSector = sector 
		report = sector.getRadioChatter()
		print report
		glutPostRedisplay( )

	
	
def mouseMotion( x, y ): 
	global mouse_coords
	mouse_coords = [x, y]
	glutPostRedisplay( )

def displayRenderState():
	print '            ',
	for x in range(0,10): 
		print str(x) + '     ',
	print '\n          ',
	for x in range(0,10): print label[x],
	print '            ',
	print '\nrendering: ' + str(Locale.sandbox.render)
	

def zoom(x,y):
	sector = Locale.sandbox.getSectorFromMouseXY(float(x)/float(WIDTH),float(y)/float(HEIGHT))
	Locale.sandbox.zoomTo(sector)

def zoomback(x,y):
	Locale.sandbox.zoomOut()
	
def keyPressed( key, x, y ):
	if key in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
		if Locale.sandbox.render[int(key)] == False: Locale.sandbox.render[int(key)] = True
		else:  Locale.sandbox.render[int(key)] = False
		displayRenderState()
	if key in ('r', 'R'):
		# radio in
		sandbox.radioIn()
	if key in ('q', 'Q', '\x1b'): sys.exit( )

	if key in ('z' 'Z') and buttonState==GLUT_DOWN and Locale.sandbox.zooming == False and Locale.sandbox.zoomed == False:
		zoom(x,y)
	if key in ('z' 'Z') and buttonState==GLUT_DOWN and Locale.sandbox.zooming == False and Locale.sandbox.zoomed == True:
		zoomback(x,y)
	
	glutPostRedisplay( )
def specialKeyPressed( key, x, y):
	if key == 27:
		sys.exit( )
	'''
	if key == GLUT_KEY_LEFT:
	elif key == GLUT_KEY_RIGHT:
	elif key == GLUT_KEY_DOWN:
	elif key == GLUT_KEY_UP:
	'''
	displayRenderState()
	glutPostRedisplay( )
	

	
def windowReshapeFunc( newWIDTH, newHEIGHT ):
  global WIDTH, HEIGHT, label
  WIDTH = newWIDTH
  HEIGHT = newHEIGHT
  print 'width: ' + str(WIDTH) + ' height: ' + str(HEIGHT)
  glViewport( 0, 0, WIDTH, HEIGHT );
  glMatrixMode( GL_PROJECTION );
  glLoadIdentity();
  gluOrtho2D( 0, GLdouble (WIDTH), 0, GLdouble (HEIGHT));
  glMatrixMode( GL_MODELVIEW )
  glLoadIdentity( )
  
def display(  ):
	global report
	"""OpenGL display function."""
	glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
	glMatrixMode( GL_PROJECTION) 
	glLoadIdentity()
	glMatrixMode( GL_MODELVIEW )
	glLoadIdentity()
	glPushMatrix()
	Locale.sandbox.renderGlobalMap()
	glPopMatrix()
	lineNum = 0
	glColor4f(1.0, 1.0, 1.0, 1.0);
	for line in report:
		glPushMatrix()
		glRasterPos2f(-0.75, 0.85-float(lineNum/12.0));
		glutBitmapString(GLUT_BITMAP_HELVETICA_12, line);
		lineNum += 1
		glPopMatrix()
	glutSwapBuffers( )

def idle():	
	Locale.sandbox.idle(0.001)   # TODO: put in actual time delta, eg getTimeOfDay
	glutPostRedisplay( )

import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/pyglet-1.2.4-py2.7.egg')

import pyglet
from math import pi, sin, cos, sqrt,exp
import numpy as np
from pyglet.gl import *
import pyglet
#import lsystem as ls

try:
    # Try and create a window with multisampling (antialiasing)
    config = Config(sample_buffers=1, samples=4, 
                    depth_size=16, double_buffer=True,)
    window = pyglet.window.Window(resizable=True, config=config)
except pyglet.window.NoSuchConfigException:
    # Fall back to no multisampling for old hardware
    window = pyglet.window.Window(resizable=True)

@window.event
def on_resize(width, height):
	global wx, wy
	wx =width
	wy =height
	# Override the default on_resize handler to create a 3D projection
	glViewport(0, 0, width, height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(60., width / float(height), .1, 1000.)
	glTranslatef(0.,0.,-10.0)
	glMatrixMode(GL_MODELVIEW)
	return pyglet.event.EVENT_HANDLED

def update(dt):
	pass
#    global rx, ry, rz
#    rx += 0
#    ry += 0
#    rz += 0*dt * 30
#    rx  = 0
#    ry  = 0
#    rz %= 360
pyglet.clock.schedule(update)

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0, -4)
    glScalef(sc,sc,sc)
    glTranslatef(tx,ty,tz)
    glRotatef(rz, 0, 0, 1)
    glRotatef(ry, 0, 1, 0)
    glRotatef(rx, 1, 0, 0)
    torus.draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
	global mx, my
	mx = x
	my = y


@window.event
def on_mouse_release(x, y, button, modifiers):
    pass

@window.event
def on_key_press(symbol, modifiers):
	if symbol==pyglet.window.key.Q:
		exit()

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
	global mx,my, rx, ry, rz, tx,ty,tz,wx,wy,sc
	dx = (float) (x - mx);
	dy = (float) (y - my);
	if (pyglet.window.mouse.LEFT==buttons):
		tx = tx + dx/wx*13.0*exp(-0.05*tz)/sc
		ty = ty + dy/wy*13.0*exp(-0.05*tz)/sc
	elif (pyglet.window.mouse.MIDDLE== buttons):
		if dy > 0:
			sc *= 1.+sqrt(dx*dx + dy*dy)/sqrt(wx*wx+wy*wy)
		else:
			sc *= 1.-sqrt(dx*dx + dy*dy)/sqrt(wx*wx+wy*wy)
		

	elif (pyglet.window.mouse.RIGHT== buttons):
		rz -= dx
		ry += dy

   	mx = x;
   	my = y;

def setup():
	# One-time GL setup
	glClearColor(0.3, 0.35, 0.4, 1)
	glLineWidth(2.0)
	glColor3f(0.98,0.98,0.94)
	glEnable(GL_DEPTH_TEST)
	#glEnable(GL_CULL_FACE)

	# Uncomment this line for a wireframe view
	#glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

	# Simple light setup.  On Windows GL_LIGHT0 is enabled by default,
	# but this is not the case on Linux or Mac, so remember to always 
	# include it.
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)
	glEnable(GL_LIGHT1)

	# Define a simple function to create ctypes arrays of floats:
	def vec(*args):
		return (GLfloat * len(args))(*args)
	glLightfv(GL_LIGHT0, GL_POSITION, vec(.5, -.5, 1, 0))
	glLightfv(GL_LIGHT0, GL_SPECULAR, vec(2.5, 2.5, 5, 1))
	glLightfv(GL_LIGHT0, GL_DIFFUSE, vec(5, 5, 5, 1))
	glLightfv(GL_LIGHT1, GL_POSITION, vec(1, 0, -.5, 0))
	glLightfv(GL_LIGHT1, GL_DIFFUSE, vec(2.5, 2.5, 2.5, 1))
	glLightfv(GL_LIGHT1, GL_SPECULAR, vec(10, 5, 5, 1))

	glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, vec(0.98,0.98,0.94, 1))
	glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, vec(1, 1, 1, 1))
	glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 20)

	#glCullFace(GL_FRONT_AND_BACK)

def deg2rad(deg):
	return (deg * pi/180.0)

class DrawTurtle(object):
	def __init__(self,turtle_data):
		#vertex_set, min_values, max_values = self.resolve_instructions(instr,X0,R0,stepsize,delta)
		vertex_set, polygons,nodes = turtle_data
        # Compile a display list
		self.list = glGenLists(1)
		glNewList(self.list, GL_COMPILE)

		glPushClientAttrib(GL_CLIENT_VERTEX_ARRAY_BIT)
		glEnableClientState(GL_VERTEX_ARRAY)

		for pVertices in vertex_set:
			vertices = (GLfloat*len(pVertices)) (*pVertices)
			glVertexPointer(3, GL_FLOAT, 0, vertices)
			glDrawArrays(GL_LINE_STRIP, 0, len(vertices)/3)

		for poly in polygons:
			vertices = (GLfloat*len(poly))(*poly)
			glVertexPointer(3, GL_FLOAT,0, vertices)
			glDrawArrays(GL_POLYGON,0,len(vertices)/3)
		glPopClientAttrib()
		glEndList()

	def draw(self):
		glCallList(self.list)
		

rx = ry = rz = 0
tx = ty = tz = 0
theta = 0
phi = 0
mx = my = 0
wx = wy=0
sc = 1.
#setup()

#X0 = np.array([0,0,0])
#R0 = np.eye(3)
#instr = 'F_R'
#rules = {'F_L':'F_R+F_L+F_R',
#'F_R':'F_L-F_R-F_L'}
#torus = None
def draw_turtle(line_list=None):
	global torus
	if (line_list!=None):
		setup()
		torus = DrawTurtle(line_list)
		pyglet.app.run()

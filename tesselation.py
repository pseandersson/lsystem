import sys

import numpy as np
import pyglet
from pyglet.gl import *
from math import pi, sin, cos, sqrt,exp

class LViewer(pyglet.window.Window):
	def __init__(self):
		try:
		    # Try and create a window with multisampling (antialiasing)
			config = Config(sample_buffers=1, samples=4,\
			 depth_size=16, double_buffer=True,)
			super(LViewer,self).__init__(resizable=True, config=config)
		except pyglet.window.NoSuchConfigException:
			# Fall back to no multisampling for old hardware
			super(LViewer,self).__init__(resizable=True)

		self.mx = 0
		self.my = 0
		self.dt = 0.
		self.l_time = 0.

		pyglet.clock.schedule(self.l_timer)

		self.setup()

	def setup(self):
		# One-time GL setup
		glClearColor(0.3, 0.35, 0.4, 1)
		glLineWidth(2.0)
		glColor3f(0.98,0.98,0.94)
		glEnable(GL_DEPTH_TEST)

	def l_timer(self,dt):
		self.dt = dt
		self.l_time += dt

	def on_draw(self):
		glClear(GL_COLOR_BUFFER_BIT |  GL_DEPTH_BUFFER_BIT)

	def on_resize(self, width,height):
		glViewport(0, 0, width, height)

if __name__=='__main__':
	lviewer = LViewer()
	pyglet.app.run()
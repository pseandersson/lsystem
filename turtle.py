import numpy as np
from math import cos, sin, pi

def deg2rad(deg):
	return (deg * pi/180.)

def turtle2d(instr,x,y,a0,d,a):
	lines = list()
	fr = [x,y];
	to = [0,0];
	mx = [10000,-10000];
	my = [10000,-10000];
	alpha = a0;
	for i in range(0,len(instr)):
		if instr[i]=='F':
			to[0] = fr[0] + d*cos(deg2rad(alpha));
			to[1] = fr[1] + d*sin(deg2rad(alpha));
			lines.append((fr[:],to[:]));
			if (to[0] < mx[0]):
				mx[0] = float (to[0]);
			if (to[0] > mx[1]):
				mx[1] = float (to[0]);
			if (to[1] < my[0]):
				my[0] = float (to[1]);
			if (to[1] > my[1]):
				my[1] = float (to[1]);
			fr = to[:]
		elif instr[i]=='-':
			alpha = alpha - a
		elif instr[i]=='+':
			alpha = alpha + a
		elif instr[i]=='f':
			to[0] = fr[0] + d*cos(deg2rad(a));
			to[1] = fr[1] + d*sin(deg2rad(a));
			fr = to[:];

	return lines,mx,my


def getHeadingRotMatrix(heading):
	return np.array([[cos(deg2rad(heading)), sin(deg2rad(heading)),0.],\
		[-sin(deg2rad(heading)), cos(deg2rad(heading)), 0.],\
		[0.,0., 1.]], dtype=float)

def getPitchRotMatrix(pitch):
	return np.array([[cos(deg2rad(pitch)),0., -sin(deg2rad(pitch))],\
		[0.,1., 0.],\
		[sin(deg2rad(pitch)), 0., cos(deg2rad(pitch))]],dtype=float)

def getRollRotMatrix(roll):
	return np.array([[1.,0., 0.],\
		[0., cos(deg2rad(roll)), -sin(deg2rad(roll))],\
		[0.,sin(deg2rad(roll)), cos(deg2rad(roll))]],dtype=float)

def turtle(instr,X0,R0,r0,stepsize, delta,dr):
	radius = 1.*r0
	pos = np.array(X0[0:3],dtype=float)
	rot = np.array(R0[:,:],dtype=float)
	new_line = True
	vertex_set = []
	vertices = None
	max_values = -100000*np.ones([1,3])
	min_values = 100000*np.ones([1,3])
	state = []
	polygons = []
	cur_polys = []
	poly = None

	for i in range(0,len(instr)):
		if instr[i]=='F':
			if new_line:
				vertex_set.append([])
				vertices = vertex_set[-1]
				vertices.extend(pos[:])
				new_line = False
	
			pos += stepsize*rot[:,0]
			vertices.extend(pos[:])

		elif instr[i]=='f':
			pos += stepsize*rot[:,0]
			if poly==None:
				new_line = True
			else:
				poly.extend(pos[:])
		elif instr[i]=='+':
			rot = rot.dot(getHeadingRotMatrix(delta))
		elif instr[i]=='-':
			rot = rot.dot(getHeadingRotMatrix(-delta))
		elif instr[i]=='&':
			rot = rot.dot(getPitchRotMatrix(delta))
		elif instr[i]=='^':
			rot = rot.dot(getPitchRotMatrix(-delta))
		elif instr[i]=='\\':
			rot = rot.dot(getRollRotMatrix(delta))
		elif instr[i]=='/':
			rot = rot.dot(getRollRotMatrix(-delta))
		elif instr[i]=='|':
			rot = rot.dot(getHeadingRotMatrix(180))
		elif instr[i]=='[':
			new_line = True
			lpos = np.array(pos[:],dtype=float)
			lrot = np.array(rot[:,:],dtype=float)
			state.append((lpos,lrot))
		elif instr[i]==']':
			new_line = True
			pos,rot = state.pop()
		elif instr[i]=='\'':
			radius += dr
		elif instr[i]=='!':
			radius -= dr
		elif instr[i]=='{':
			if poly!=None:
				cur_polys.append(poly)
			lpos = np.array(pos[:],dtype=float)
			lrot = np.array(rot[:,:],dtype=float)
			state.append((lpos,lrot))
			polygons.append([])
			poly = polygons[-1]
			poly.extend(pos[:])
		elif instr[i]=='}':
			if (len(cur_polys)>0):
				poly = cur_polys.pop()
			else:
				poly = None
			pos,rot = state.pop()



	return vertex_set,polygons

class TNode(object):
	def __init__(self,pos):
		self.pos = []
		self.pos.extend(pos[:])
		self.out_edges = []
		self.in_edges = []

	def addEdge(self, tnode):
		self.out_edges.append(tnode)
		tnode.addInEdge(self)
		return tnode

	def addInEdge(self,tnode):
		self.in_edges.append(tnode)

	def __str__(self):
		s = '@('+str(self.pos)+')'
		for node in self.out_edges:
			s += '\n' + str(node)
		s = s.replace('\n','\n  ') 
		return s

def turtle_tree(itree,X0,R0,r0,istepsize, idelta,idr):
	stepsize = float(istepsize)
	delta = float(idelta)
	dr = float(idr)
	radius = 1.*r0
	pos = np.array(X0[0:3],dtype=float)
	rot = np.array(R0[:,:],dtype=float)
	new_line = True
	vertex_set = []
	vertices = None
	max_values = -100000*np.ones([1,3])
	min_values = 100000*np.ones([1,3])
	state = []
	polygons = []
	cur_polys = []
	poly = None

	node = itree.first()
	tnodes = []
	tnode_root = None
	tnode = None

	while True:
		if node.hasArguments():
			stepsize = float(node.getArgument(0))
			delta = float(node.getArgument(0))
			dr = float(node.getArgument(0))
		else:
			stepsize = float(istepsize)
			delta = float(idelta)
			dr = float(idr)

		if node=='F':
			if new_line:
				vertex_set.append([])
				vertices = vertex_set[-1]
				vertices.extend(pos[:])
				if tnode == None:
					tnode = TNode(pos[:])
					tnode_root = tnode
				new_line = False

			pos += float(stepsize)*rot[:,0]
			vertices.extend(pos[:])
			tnode = tnode.addEdge(TNode(pos[:]))
		elif node=='f':
			pos += stepsize*rot[:,0]
			if poly==None:
				new_line = True
			else:
				poly.extend(pos[:])
		elif node=='+':
			rot = rot.dot(getHeadingRotMatrix(delta))
		elif node=='-':
			rot = rot.dot(getHeadingRotMatrix(-delta))
		elif node=='&':
			rot = rot.dot(getPitchRotMatrix(delta))
		elif node=='^':
			rot = rot.dot(getPitchRotMatrix(-delta))
		elif node=='\\':
			rot = rot.dot(getRollRotMatrix(delta))
		elif node=='/':
			rot = rot.dot(getRollRotMatrix(-delta))
		elif node=='|':
			rot = rot.dot(getHeadingRotMatrix(180))
		elif node=='[':
			new_line = True
			lpos = np.array(pos[:],dtype=float)
			lrot = np.array(rot[:,:],dtype=float)
			state.append((lpos,lrot,tnode))
		elif node==']':
			new_line = True
			pos,rot,tnode = state.pop()
		elif node=='\'':
			radius += dr
		elif node=='!':
			radius -= dr
		elif node=='{':
			if poly!=None:
				cur_polys.append(poly)
			lpos = np.array(pos[:],dtype=float)
			lrot = np.array(rot[:,:],dtype=float)
			state.append((lpos,lrot))
			polygons.append([])
			poly = polygons[-1]
			poly.extend(pos[:])
		elif node=='}':
			if (len(cur_polys)>0):
				poly = cur_polys.pop()
			else:
				poly = None
			pos,rot = state.pop()

		try:
			node = node.next()
		except StopIteration:
			break

	return vertex_set,polygons,tnode_root

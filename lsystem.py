#!/usr/bin/env python
# --------------------
# Copyright (C) 2016 Patrik Andersson
# All rights reserved
# --------------------

import numpy as np
from numpy.random import random as rand

SUBSCRIPT       = (1<<0)
LOOK_BEFORE     = (1<<1)
LOOK_AFTER      = (1<<2)
BRACKETS        = (1<<3)
BRACKET_ERROR   = (1<<4)
FUNC_DEF        = (1<<5)

class LNode(object):
	"""LNode is a node in a tree graph representing one command in the Liedermayer system.
	   The LNode knows its position in the tree, so it is possible to navigate up() and down()
	   in the branch belonging to the nodes.
	   LNode also knows its position in the string, so it is possible to know its next()
	   command and its previous command with the command prev().
	   In order to compare rules against commands in the string a tree matching functionality
	   is implemented into the node via the function match(). The logic respects context as
	   branches."""
	def __init__(self,val='',predecessor=None):
		self.childs = []
		self.predecessor = predecessor
		self.descendants = 0
		self.depth = 0
		self.val = val
		self.updateMaxDepth(1)

	"""Update the depth for the nodes predecessor"""
	def updateMaxDepth(self,depth):
		self.depth = depth
		if not self.isRoot() and not self.isBranch():
			self.predecessor.updateMaxDepth(self.depth+1)

	"""Deprecated. Keep control of how many descendants
	   there are for the LNode"""
	def increaseDescendants(self):
		self.descendants +1
		if not self.isRoot():
			self.predecessor.increaseDescendants()

	"""Deprecated. see addChild() instead"""
	def addBranch(self, val):
		self.childs.append(LNode(val,self))
		self.increaseDescendants()
		return self.childs[-1]

	"""Add a new command val as child to current node"""
	def addChild(self, val):
		self.childs.append(LNode(val,self))
		self.increaseDescendants()
		return self.childs[-1]

	"""Check whether current node is a branch node or not"""
	def isBranch(self):
		return self.val in '[]'

	"""Check if current node is a child node or not"""
	def isChild(self):
		return (not self.isBranch() and not self.isRoot())

	"""Check if current node is root or not"""
	def isRoot(self):
		return self.predecessor==None

#	def create_tree(self,instr):
#		slen = len(instr)
#		states = []
#		node = self
#		new_branch = False
#		i = 0
#		while i <slen:
#			if instr[i]=='[':
#				states.append(node)
#				node = node.addChild(instr[i],i)
#				new_branch = True
#			elif instr[i]==']':
#				node = node.addChild(instr[i],i)
#				node = states.pop()
#			else:
#				key = instr[i]
#				oi = i
#				if i+1 < slen:
#					if instr[i+1]=='_':
#						key += instr[i+1:i+3]
#						i+=2
#
#				node = node.addChild(key, oi)
#
#			i+=1
	"""Compare two different LNode-system to see if they match"""
	def match(self, b):
		if type(self)==type(b):
			#print self.val,'==',b.val
			if self.val==b.val:
				if self.hasChilds() and b.hasChilds():
					cmp_child = True
					i = 0
					j = 0
					while i < len(self.childs) and j < len(b.childs) :
						cmp_child = self.childs[i].match(b.childs[j])
						
						if not cmp_child:
							if self.childs[i].val=='[':
								j-=1
							else:
								return False
						i+=1
						j+=1

					if i==len(b.childs):
						return True
					else:
						return False
				elif self.hasChilds() and not b.hasChilds():
					return True
				elif not self.hasChilds() and b.hasChilds():
					return False
				else:
					return True
			elif b.val==']':
				return True
			elif self.val=='[':
				is_ok = False
				try:
					node = self.up().down(self)
					is_ok = node.match(b)
				except StopIteration:
					return False

				return is_ok
			else:
				return False
		elif type(b)==type(str()):
#			print 'TXT:',self.val,'==',b
			if self.val==b and not self.hasChilds():
				return True
			else:
				return False
		else:
			return False

	"""Navigate upwards in the tree structure."""
	def up(self):
		if self.isRoot():
			raise StopIteration
		else:
			if (self.predecessor.val=='['):
				return self.predecessor.up()
			else:
				return self.predecessor
	"""Navigate downwards in the tree. 
	   If last_child is given, it will go down
	   in the sibling node to last_child which is
	   ordered after last_child in childs. If
	   last_child is last item, StopIteration is raised"""
	def down(self, last_child=None):
		if len(self.childs)==0:
			raise StopIteration
		else:
			if last_child!=None:
				i = self.childs.index(last_child)
				if i+1< len(self.childs):
					return self.childs[i+1]
				else:
					raise StopIteration
			else:
				return self.childs[0]

	"""Check wheter the node has childs or not"""
	def hasChilds(self):
		return len(self.childs)>0

	"""Internal function for prev()"""
	def last_child(self):
		if self.hasChilds():
			return self.childs[-1].last_child()
		else:
			return self

	"""Go to the previous node in the string-space"""
	def prev(self,last_child=None):
		if last_child==None:
			if self.isRoot():
				raise StopIteration
			else:
				return self.predecessor.prev(self)
		else:
			i = self.childs.index(last_child)
			if i-1 <0:
				return self
			else:
				return self.childs[i-1].last_child()

	"""Internal function for next()"""
	def next_at_parent(self):
		if not self.isRoot():
			return self.predecessor.next(self)
		else:
			raise StopIteration

	"""Go to next function in the string-space"""
	def next(self,last_child=None):
		if len(self.childs)==0:
			return self.next_at_parent()
		else:
			if last_child==None and self.hasChilds():
				return self.childs[0]
			else:
				i = self.childs.index(last_child)

				if i+1< len(self.childs):
					return self.childs[i+1]
				else:
					return self.next_at_parent()


#	def getNodeAt(self,pos):
#		if self.pos == pos:
#			return self
#		elif pos < self.pos:
#			return self.predecessor.getNodeAt(pos)
#		else:
#			if len(self.childs)>1:
#				for i in range(0,len(self.childs)-1):
#					j =i+1
#					if pos < self.childs[j].pos:
#						return self.childs[i].getNodeAt(pos)
#				return self.childs[-1].getNodeAt(pos)
#
#			elif len(self.childs)>0:
#				return self.childs[0].getNodeAt(pos)
#
#			return None

	"""Returns the string, building up the node-scheme"""
	def to_string(self):
		tstr = self.val

		for node in self.childs:
			tstr += str(node.to_string())
		return tstr

	"""Display the node tree"""
	def print_tree(self, indent=0):		
		ostr = str().zfill(indent).replace('0',' ') + self.val
		ostr += " ("+ str(self.depth)+")"
		print ostr
		for node in self.childs:
			node.print_tree(indent+2)

class LTree(object):
	"""LTree is a class to organize L-System instructions into LNode's.
	After the tree has been created one can access the nodes by chop()
	function. The chop()-function gives access to the nodes and remove
	their relationship to LTree so new trees can grow up there"""
	def __init__(self):
		self.states = []
		self.root = LNode()
		self.node = self.root

	"""Push strings into the tree structure"""
	def __lshift__(self,instr):
		if type(instr)==type(str()):
			self.push(instr)
		return self
	
	"""Chopping trees to get access to its stems, branches and leaves,
	   so new tree can be planted and grow"""
	def chop(self):
		tree = None
		if len(self.root.childs)==1:
			tree = self.root.childs.pop()
			tree.predecessor=None
		else:
			tree = self.root
		self.root = LNode()
		self.node = self.root
		self.states = []
		return tree

	"""Push back literals to construct the tree"""
	def push(self, instr):
		slen = len(instr)
		i = 0

		while i <slen:
			if instr[i]=='[':
				self.states.append(self.node)
				self.node = self.node.addChild(instr[i])
				new_branch = True
			elif instr[i]==']':
				self.node = self.node.addChild(instr[i])
				self.node = self.states.pop()
			else:
				key = instr[i]
				oi = i
				if i+1 < slen:
					if instr[i+1]=='_':
						key += instr[i+1:i+3]
						i+=2

				self.node = self.node.addChild(key)

			i+=1

	"""Display the tree"""
	def print_tree(self):
		if len(self.root.childs)==1:
			self.root.childs[0].print_tree()
		else:
			self.root.print_tree()
	def to_string(self):
		if len(self.root.childs)==1:
			return self.root.childs[0].to_string()
		else:
			return self.root.to_string()

def look(instr,pos,bf_str, ldir,ignore):
	is_ok = False
	s = len(bf_str)
	i = pos
	npos = pos
	new_context = 0
	exit_context = 0
	same_con = True
	tmp_str_list = []
	tmp_str_list.append([])
	tmp_str = tmp_str_list[-1]
	
	while i > 0 and i+1 < len(instr):
		i += ldir
		tmp = str().join(tmp_str)
		ts = s-len(tmp)

		if exit_context==new_context:
			if exit_context==0:
				same_con = True
			else:
				same_con = False
		elif exit_context > new_context:
			same_con = True
		else:
			same_con = False

		if instr[i]=='[':
			npos = i
			exit_context +=1
		elif instr[i]==']':
			new_context +=1
		elif bf_str==instr[i:i+ts]+tmp:
			is_ok=True
			break
		elif instr[i] in ignore:
			continue
		elif (npos-i)<s:
			tmp_str.insert(0,instr[i])
			continue
		elif same_con:
			return False
	return is_ok

def parse_rule(instr,pos,rule,ignore=''):
	bracket_count = 0
	commas=[]
	less_pos = 0
	great_pos = 0
	flag = 0
	var_length = 1
	i = 0

	while i < len(rule):
		if rule[i]=='<':
			flag |= LOOK_BEFORE
			less_pos = i
		elif rule[i]=='>':
			flag |= LOOK_AFTER
			great_pos = i
		elif rule[i]=='(':
			flag |= BRACKETS
			flag |= BRACKET_ERROR
			bracket_count+=1
		elif rule[i]==')':
			flag &=~BRACKET_ERROR
			bracket_count-=1
		elif rule[i]==':':
			flag |= FUNC_DEF
			break;
		elif rule[i]==',':
			commas.append(i)
		elif rule[i]=='_':
			flag |= SUBSCRIPT
		i+=1

	if flag&SUBSCRIPT:
		var_length += 2

	if pos + var_length > len(instr):
		return False

	if flag&LOOK_BEFORE:
		bf_str = rule[0:less_pos]
		less_pos+=1

	if flag&LOOK_AFTER:
		af_str = rule[great_pos+1:i]

	key = rule[less_pos:(less_pos+var_length)]


	is_ok = (instr[pos:pos+var_length]==key)
	if not is_ok:
		return False

	# Check if condition is met
	if flag&LOOK_BEFORE:
		is_ok = look(instr,pos,bf_str,1,ignore)

	if not is_ok:
		return False

	if flag&LOOK_AFTER:
		#print 'Looking for', af_str, 'after', key
		is_ok = False
		s = len(af_str)
		i = pos
		while i+1 < len(instr):
			i+=1
			if af_str==instr[i:i+s]:
				is_ok =True
				break
			elif instr[i] in ignore:
				continue
			elif (i-pos)<s:
				continue
			else:
				return False

	if not is_ok:
		return False

	return True
	#Parse function definitions
	if i<len(rule):
		if rule[i]==':':
			i +=1

def parse_rule_tree(node,rule,ignore=''):
	bracket_count = 0
	commas=[]
	less_pos = 0
	great_pos = 0
	flag = 0
	var_length = 1
	i = 0
	is_ok = False

	while i < len(rule):
		if rule[i]=='<':
			flag |= LOOK_BEFORE
			less_pos = i
		elif rule[i]=='>':
			flag |= LOOK_AFTER
			great_pos = i
		elif rule[i]=='(':
			flag |= BRACKETS
			flag |= BRACKET_ERROR
			bracket_count+=1
		elif rule[i]==')':
			flag &=~BRACKET_ERROR
			bracket_count-=1
		elif rule[i]==':':
			flag |= FUNC_DEF
			break;
		elif rule[i]==',':
			commas.append(i)
		elif rule[i]=='_':
			flag |= SUBSCRIPT
		i+=1

	if flag&SUBSCRIPT:
		var_length += 2

	if flag&LOOK_BEFORE:
		bf_str = rule[0:less_pos]
		less_pos+=1

	if flag&LOOK_AFTER:
		af_str = rule[great_pos+1:i]

	key = rule[less_pos:(less_pos+var_length)]

	if flag&(LOOK_BEFORE|LOOK_AFTER)==0:
		return node.val==key

	# Check if condition is met
	if flag&LOOK_BEFORE:
		bf_rule = (LTree() << bf_str).chop()
		lnode = node
		is_ok = False
		try:
			for i in range(bf_rule.depth):
				lnode = lnode.up()

			if lnode.match(bf_rule):
				is_ok = True
		except StopIteration:
			is_ok = False


	if not is_ok:
		return False

	if flag&LOOK_AFTER:
		#print 'Looking for', af_str, 'after', key
		af_rule = (LTree() << af_str).chop()
		lnode = node.next()
		is_ok = lnode.match(af_rule)

	if not is_ok:
		return False

	return True

	#Parse function definitions
	if i<len(rule):
		if rule[i]==':':
			i +=1

def lookup(instr,pos,d,key):
	for k in d.keys():
		if key==k:
			return True, k
		else:
			if parse_rule(instr,pos,k):
				return True, k
	return False, None

def tree_lookup(itree,d):
	for k in d.keys():
		if itree==k:
			return True, k
		else:
			if parse_rule_tree(itree,k):
				return True, k
	return False, None


def resolve_prob_rule(rules):
	weight = 0.;
	itr = iter(rules)
	prob_rules = []
	cs = [0.]
	try:
		while True:
			rule = itr.next();
			prob = rules[rule]
			cs.append(prob+cs[-1])
			prob_rules.append(rule)
	except StopIteration:
		pass
	
	cs = np.array(cs,dtype=float)
	cs /= cs.max()

	r = rand(1)
	
	for k in range(0,len(cs)):
		if r < cs[k]:
			return prob_rules[k-1]

def resolve_instructions(instr,rules,nmax,figures=dict()):

	for n in range(1,nmax+1):
		oldstr = instr
		instr = ''
		sLen = len(oldstr)
		i = 0
		oi = 0
		while i < sLen:
			key = oldstr[i];
			oi=i
			if (i+2 < sLen):
				if (oldstr[i+1]=="_"):
					key = key + "_" + oldstr[i+2];
					i = i+2

			rule_exists, rkey = lookup(oldstr, oi, rules, key)

			if rule_exists:
				if type(rules[rkey])==type(str()):
					instr = instr + rules[rkey]
				elif type(rules[rkey])==type(dict()):
					instr = instr + resolve_prob_rule(rules[rkey])

			else:
				instr = instr + key
			i+=1

		#print 'n=',n,', ', instr
	if (len(figures.keys())>0):
		instr = resolve_instructions(instr,figures,1);
	return instr

def resolve_instructions_by_tree(instr,rules,nmax,figures=dict()):
	itree = LTree() << instr

	for n in range(1,nmax+1):
		#oldstr = instr
		#itree = LNode(oldstr)
		#instr = ''
		#sLen = len(oldstr)
		#i = 0
		#oi = 0
		node = itree.chop()
		while True:
			rule_exists, rkey = tree_lookup(node, rules)

			if rule_exists:
				if type(rules[rkey])==type(str()):
					itree << rules[rkey]
				elif type(rules[rkey])==type(dict()):
					itree << resolve_prob_rule(rules[rkey])

			else:
				itree << node.val

			try:
				node = node.next()
			except StopIteration:
				break
	instr = itree.to_string()
	#print 'n=',n,', ', instr
	if (len(figures.keys())>0):
		instr = resolve_instructions(instr,figures,1);
	return instr




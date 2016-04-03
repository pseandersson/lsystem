#!/usr/bin/env python
# --------------------
# Copyright (C) 2016 Patrik Andersson
# All rights reserved
# --------------------
import string
import types
import numpy as np
from numpy.random import random as rand

SUBSCRIPT       = (1<<0)
LOOK_BEFORE     = (1<<1)
LOOK_AFTER      = (1<<2)
BRACKETS        = (1<<3)
BRACKET_ERROR   = (1<<4)
FUNC_DEF        = (1<<5)

DETERMINISTIC_RULE = 0
STOCHASTIC_RULE    = (1<<0)


"""Global functions to resolve mathematical expression
   such as: 2((5e-1-2)+1)/3+2*(4)"""
def calculate(instr):
	instr += ' ' # Add end padding to simplify algo
	nums = '0123456789.'
	math_op = '+-*/^v'
	mem_val = None
	rvalue = 0.0
	last_op = ''
	val_str = ''
	bracket_start = None
	bracket_val = None
	bracket_count = 0
	
	i = 0
	
	while i < len(instr):
		lvalue = None
		cur_op = None

		# check if we are not in a bracket
		# context
		if bracket_count==0:
			# Add numerical value to the
			# value string
			if instr[i] in nums:
				val_str += instr[i]
			# if a minus sign present and
			# value string is empty use it
			# as a sign indicator
			elif instr[i]=='-' and \
			 (val_str=='' or val_str[-1]=='e') and bracket_val==None:
				if bracket_count==0:
					val_str += instr[i]
			elif instr[i]=='e' and \
				 val_str!='' and\
				 val_str[-1]!='-':
				 val_str += instr[i]
			# Otherwise try to resolve the value
			else:
				if len(val_str)>0:
					try:
						lvalue = string.atof(val_str)
						val_str = ''
					except ValueError:
						pass
				# bracket values are returned in the
				# next loop of the string so it has
				# correspondance to an operator
				elif bracket_val!=None:
					lvalue = bracket_val
					bracket_val = None

				# Store operatator 
				if instr[i] in math_op:
					cur_op=instr[i]
				# If a bracket context is
				# at beginning, enable lazy brackets
				# so it is possible to write
				# 2(3-1) = 4
				if instr[i] in '(':
					if lvalue!=None and cur_op==None:
						cur_op = '*'
					bracket_count+=1
					bracket_start=i+1
		else:
			#end bracket context
			if instr[i] in ')':
				bracket_count-=1
				if bracket_count==0:
					bracket_val =\
					calculate(instr[bracket_start:i])
			elif instr[i] in '(':
				bracket_count+=1

		# Do math operations
		if mem_val != None:
			if last_op in '+-' and lvalue!=None:
				rvalue += mem_val
				if last_op=='+':
					mem_val = lvalue
				else:
					mem_val = -lvalue
			elif last_op in '*/' and lvalue!=None:
				if last_op =='*':
					mem_val *=lvalue
				else:
					mem_val /= lvalue
			elif last_op in '^v' and lvalue!=None:
				if last_op =='^':
					mem_val = max(mem_val,lvalue)
				else:
					mem_val = min(mem_val,lvalue)
		elif lvalue!=None:
			mem_val = lvalue

		if cur_op!=None:
			last_op = cur_op
		i+=1
	if mem_val!=None:
		rvalue += mem_val
	return rvalue


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
		self.arguments = []
		self.updateMaxDepth(1)

	def __eq__(self, b):
		if type(b)==types.StringType:
			return self.val==b
		else:
			return NotImplemented

	"""setArguments of node"""
	def setArguments(self, args):
		if type(args)==type(str()):
			self.arguments = args[1:-1].split(',')
		elif type(args)==type(dict()):
			for i in range(0,self.getArgumentCount()):
				arg_expr = self.getArgument(i)
				for key, value in args.items():
					arg_expr = arg_expr.replace(key,'('+value+')')
				self.arguments[i]= str(calculate(arg_expr))

	"""Evaluate if node has any arguments"""
	def hasArguments(self):
		return len(self.arguments)>0

	"""getArgument at position index"""
	def getArgument(self, index):
		return self.arguments[index]

	"""Returns number of available arguments"""
	def getArgumentCount(self):
		return len(self.arguments)

	"""Returns all arguments of node"""
	def getArguments(self):
		return arguments

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

#	"""Compare two different LNode-system to see if they match"""
#	def match(self, b):
#		if type(self)==type(b):
#			#print self.val,'==',b.val
#			if self.val==b.val:
#				if self.hasChilds() and b.hasChilds():
#					cmp_child = True
#					i = 0
#					j = 0
#					while i < len(self.childs) and j < len(b.childs) :
#						cmp_child = self.childs[i].match(b.childs[j])
#						
#						if not cmp_child:
#							if self.childs[i].val=='[':
#								j-=1
#							else:
#								return False
#						i+=1
#						j+=1
#
#					if i==len(b.childs):
#						return True
#					else:
#						return False
#				elif self.hasChilds() and not b.hasChilds():
#					return True
#				elif not self.hasChilds() and b.hasChilds():
#					return False
#				else:
#					return True
#			elif b.val==']':
#				return True
#			elif self.val=='[':
#				is_ok = False
#				try:
#					node = self.up().down(self)
#					is_ok = node.match(b)
#				except StopIteration:
#					return False
#
#				return is_ok
#			else:
#				return False
#		elif type(b)==type(str()):
##			print 'TXT:',self.val,'==',b
#			if self.val==b and not self.hasChilds():
#				return True
#			else:
#				return False
#		else:
#			return False

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

	"""Returns the string, building up the node-scheme"""
	def to_string(self,traverse=False):
		tstr = self.val
		if self.hasArguments():
			tstr += '('
			for i in range(0,self.getArgumentCount()):
				tstr += self.getArgument(i)
				if i < self.getArgumentCount()-1:
					tstr+=','
				else:
					tstr+=')'
		if traverse:
			for node in self.childs:
				tstr += str(node.to_string(traverse))
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
	def __init__(self,initstr=None):
		self.states = []
		self.root = LNode()
		self.node = self.root

		if type(initstr)==type(str()):
			self.push(initstr)

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

	def first(self):
		tree = None
		if len(self.root.childs)==1:
			tree = self.root.childs[0]
			tree.predecessor=None
		else:
			tree = self.root
		return tree

	"""Push back literals to construct the tree"""
	def push(self, instr):
		slen = len(instr)
		i = 0
		bracket_start_pos = None
		bracket_count = 0
		while i <slen:
			if instr[i]=='(':
				bracket_start_pos=i
				bracket_count += 1
				i +=1
				while i < slen:
					if instr[i]=='(':
						bracket_count+=1
					elif instr[i]==')':
						bracket_count-=1
					if bracket_count==0:
						break
					i+=1
				self.node.setArguments(instr[bracket_start_pos:i+1])
			elif instr[i]=='[':
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
			return self.root.childs[0].to_string(True)
		else:
			return self.root.to_string(True)

class Rule(object):
	def __init__(self,initstr, consequences,ignore=''):
		self.flag = 0
		self.key = None
		self.less = None
		self.greater = None
		self.consequences = None
		self.prob_rules = []
		self.cs = None # Cummulative Sum
		self.cmp_type = None
		self.fn_str = None
		self.cmp_str = None
		self.ignore = ignore

		self.setup_case(initstr)
		self.setup_consequences(consequences)

	def setup_case(self, initstr):
		i = 0
		less_pos=None
		great_pos=None
		bracket_count = 0
		commas = []
		while i < len(initstr):
			if initstr[i]=='<':
				self.flag |= LOOK_BEFORE
				less_pos = i+1
			elif initstr[i]=='>':
				self.flag |= LOOK_AFTER
				great_pos = i
			elif initstr[i]=='(':
				self.flag |= BRACKETS
				self.flag |= BRACKET_ERROR
				bracket_count+=1
			elif initstr[i]==')':
				self.flag &=~BRACKET_ERROR
				bracket_count-=1
			elif initstr[i]==':':
				self.flag |= FUNC_DEF
				break;
			elif initstr[i]==',':
				commas.append(i)
			i+=1

		key_string = None

		if self.flag&FUNC_DEF:
			key_string = initstr[0:i]
		else:
			key_string = initstr

		self.key = (LTree() << key_string[less_pos:great_pos]).chop()
		
		if self.flag&LOOK_BEFORE:
			self.less    = (LTree() << key_string[0:less_pos-1]).chop()
	
		if self.flag&LOOK_AFTER:
			self.greater = (LTree() << key_string[great_pos+1:]).chop()
	
		if self.flag&FUNC_DEF:
			self.setup_func(initstr[(i+1):])

	def setup_func(self, funcstr):
		self.cmp_type = ''
		if '<=' in funcstr:
			self.cmp_type='<='
		elif '>=' in funcstr:
			self.cmp_type ='>='
		elif '==' in funcstr:
			self.cmp_type = '=='
		elif '!=' in funcstr:
			self.cmp_type = '!='
		elif '<' in funcstr:
			self.cmp_type='<'
		elif '>' in funcstr:
			self.cmp_type='>'

		pos = funcstr.find(self.cmp_type)
		self.fn_str = funcstr[0:pos]
		self.cmp_str = funcstr[pos+len(self.cmp_type):]

	def setup_consequences(self, consequences):
		if type(consequences)==type(dict()):
			self.type = STOCHASTIC_RULE
			weight = 0.;
			itr = iter(consequences)
			
			self.cs = [0.]
			try:
				while True:
					rule = itr.next();
					prob = consequences[rule]
					self.cs.append(prob+self.cs[-1])
					self.prob_rules.append(rule)
			except StopIteration:
				pass
			
			self.cs = np.array(self.cs,dtype=float)
			self.cs /= self.cs.max()
		else:
			self.prob_rules.append(consequences)

	"""Test if the node follows the rule. Returns True if it does,
	   otherwise False."""
	def trial(self,node):
		bf_node = None
		af_node = None
		
		if not self.simple_rule_match(self.key,node ):
			return False, None
		#print 'Key', self.key.val
		if self.flag&LOOK_BEFORE:
			lnode = node
			try:
				for i in range(self.less.depth):
					lnode = lnode.up()
					while lnode.val in self.ignore:
						lnode = lnode.up()

				if not self.match(lnode, self.less):
					return False, None
				else:
					bf_node =lnode
			except StopIteration:
				return False, None

		if self.flag&LOOK_AFTER:
			try:
				if self.match(node.next(), self.greater):
					af_node = node.next()
				else:
					return False, None
			except StopIteration:
				return False, None

		# Create argument list
		arglist = dict()
		self.parse_arguments(self.key,node,arglist)
		
		if bf_node:
			self.match(bf_node, self.less, arglist)
		if af_node:
			self.match(af_node, self.greater, arglist)

		state = True

		# Evaluate function
		if self.flag&FUNC_DEF:
			# Might be useful in the future
			#if self.key.getArgumentCount()!=\
			#	node.getArgumentCount():
			#	return False

			fn_str = self.fn_str
			cmp_str = self.cmp_str

			for i in range(self.key.getArgumentCount()):
				fn_str = fn_str.replace(self.key.getArgument(i),\
										node.getArgument(i))
				cmp_str = cmp_str.replace(self.key.getArgument(i),\
										node.getArgument(i))

			if self.cmp_type=='<=':
				state = calculate(fn_str) <= calculate(cmp_str)
			elif self.cmp_type=='>=':
				state = calculate(fn_str) >= calculate(cmp_str)
			elif self.cmp_type=='==':
				state = calculate(fn_str) == calculate(cmp_str)
			elif self.cmp_type=='!=':
				state = calculate(fn_str) != calculate(cmp_str)
			elif self.cmp_type=='<':
				state = calculate(fn_str) < calculate(cmp_str)
			elif self.cmp_type=='>':
				state = calculate(fn_str) > calculate(cmp_str)

		return state, arglist

	def return_rule(self,arglist=None,rule_id=1):
		rule = LTree(self.prob_rules[rule_id-1])
		if type(arglist)==type(dict()):
			node = rule.first();
			while True:
				node.setArguments(arglist)
				try:
					node= node.next()
				except StopIteration:
					break
			return rule.to_string()
		else:
			return rule.to_string()
	"""Test if the string follows the given rule, if it does
	   then it returns the replacement string otherwise None."""

	def try_case(self, case_str ):
		success, arglist = self.trial(case_str)
		if success:
			if self.cs==None:
				return self.return_rule(arglist)
			else:
				r = rand()
				for k in range(0,len(self.cs)):
					if r < self.cs[k]:
						return self.return_rule(arglist, k)
		else:
			return None

	def simple_rule_match(self,a,b):
		if a.val==b.val:
			if a.getArgumentCount()==b.getArgumentCount():
				return True
		return False

	"""Internal method to parse arguments"""
	def parse_arguments(self, a, b, d):
		for i in range(0,a.getArgumentCount()):
			if not d.has_key(a.getArgument(i)):
				d[a.getArgument(i)] = b.getArgument(i)
			else:
				print 'Argument error'

	"""Compare two different LNode-system to see if they match.
	   a is the instruction b is the rule."""
	def match(self, a, b, arglist=None):
		if type(a)==type(b):
			#print a.val,'==',b.val
			if self.simple_rule_match(a,b):
				if type(arglist)==types.DictType:
					self.parse_arguments(a,b,arglist)
				if a.hasChilds() and b.hasChilds():
					cmp_child = True
					i = 0
					j = 0
					while i < len(a.childs) and j < len(b.childs) :
						cmp_child = self.match(a.childs[i],b.childs[j],arglist)
						
						if not cmp_child:
							if a.childs[i].val=='[':
								j-=1
							else:
								return False
						i+=1
						j+=1

					if i==len(b.childs):
						return True
					else:
						return False
				elif a.hasChilds() and not b.hasChilds():
					return True
				elif not a.hasChilds() and b.hasChilds():
					return False
				else:
					return True
			elif b.val == '*':
				return True
			elif a.val in self.ignore:
				try:
					return self.match(a.next(),b,arglist)
				except StopIteration:
					return False
			elif b.val==']':
				return True
			elif a.val=='[':
				is_ok = False
				try:
					node = a.up().down(a)
					is_ok = self.match(node,b,arglist)
				except StopIteration:
					return False
				return is_ok
			else:
				return False
		elif type(b)==type(str()):
#			print 'TXT:',self.val,'==',b
			if a.val==b and not a.hasChilds():
				return True
			else:
				return False
		else:
			return False



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

	if node.val!=key:
		return False

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

def resolve_instructions_by_tree(instr,rules,nmax,**extras):
	law_book = []
	figures = None
	ignore = ''

	if extras.has_key("figures"):
		if type(extras['figures'])==types.DictType:
			figures == extras['figures']
		else:
			raise ValueError

	if extras.has_key('ignore'):
		if type(extras['ignore'])==types.StringType:
			ignore = extras['ignore']
		else:
			raise ValueError

	for law in rules.keys():
		law_book.append(Rule(law, rules[law],ignore))
	itree = LTree();

	if type(instr)==type(LTree()):
		itree = instr
	else:
		itree << instr

	for n in range(1,nmax+1):
		node = itree.chop()
		while True:
			new_str = None

			for rule in law_book:
				new_str = rule.try_case(node)
				if new_str!=None:
					break;

			if new_str!=None:
				itree << new_str
			else:
				itree << node.to_string()

			try:
				node = node.next()
			except StopIteration:
				break
	#instr = itree.to_string()
	#print 'n=',n,', ', instr
	if figures:
		itree = resolve_instructions_by_tree(itree,figures,1);
	return itree




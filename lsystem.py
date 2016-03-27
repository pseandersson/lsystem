import numpy as np
from numpy.random import random as rand

SUBSCRIPT       = (1<<0)
LOOK_BEFORE     = (1<<1)
LOOK_AFTER      = (1<<2)
BRACKETS        = (1<<3)
BRACKET_ERROR   = (1<<4)
FUNC_DEF        = (1<<5)

class LNode(object):
	BRANCH = 1
	CHILD = 0
	
	def __init__(self,val,pos=-1,node_type=CHILD,predecessor=None):
		self.node_type = node_type
		self.childs = []
		self.pos = pos
		self.predecessor = predecessor
		self.descendants = 0
		self.depth = 0

		if pos==-1:
			self.create_tree(val)
			self.val=''
			if len(self.childs)==1:
				child = self.childs.pop()
				self.val = child.val
				self.node_type  =child.node_type
				self.childs = child.childs
				self.depth = child.depth
				self.descendants = child.descendants
				self.predecessor=None
				for node in self.childs:
					node.predecessor = self
		else:
			self.val = val
			self.predecessor
			self.updateMaxDepth(1)

	def updateMaxDepth(self,depth):
		self.depth = depth
		if not self.isRoot() and not self.isBranch():
			self.predecessor.updateMaxDepth(self.depth+1)

	def increaseDescendants(self):
		self.descendants +1
		if not self.isRoot():
			self.predecessor.increaseDescendants()

	def addBranch(self, val, pos):
		self.childs.append(LNode(val,pos,self.BRANCH,self))
		self.increaseDescendants()
		return self.childs[-1]

	def addChild(self, val, pos):
		self.childs.append(LNode(val,pos,self.CHILD,self))
		self.increaseDescendants()
		return self.childs[-1]

	def isBranch(self):
		return self.node_type==self.BRANCH

	def isChild(self):
		return self.node_type==self.CHILD

	def isRoot(self):
		return self.predecessor==None

	def create_tree(self,instr):
		slen = len(instr)
		states = []
		node = self
		new_branch = False
		i = 0
		while i <slen:
			if instr[i]=='[':
				states.append(node)
				node = node.addChild(instr[i],i)
				new_branch = True
			elif instr[i]==']':
				node = node.addChild(instr[i],i)
				node = states.pop()
			else:
				key = instr[i]
				oi = i
				if i+1 < slen:
					if instr[i+1]=='_':
						key += instr[i+1:i+3]
						i+=2

				node = node.addChild(key, oi)

			i+=1

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
			print 'TXT:',self.val,'==',b
			if self.val==b and not self.hasChilds():
				return True
			else:
				return False
		else:
			return False

	def up(self):
		if self.isRoot():
			raise StopIteration
		else:
			if (self.predecessor.val=='['):
				return self.predecessor.up()
			else:
				return self.predecessor

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
	
	def hasChilds(self):
		return len(self.childs)>0

	def last_child(self):
		if self.hasChilds():
			return self.childs[-1].last_child()
		else:
			return self

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

	def next_at_parent(self):
		if not self.isRoot():
			return self.predecessor.next(self)
		else:
			raise StopIteration

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


	def getNodeAt(self,pos):
		if self.pos == pos:
			return self
		elif pos < self.pos:
			return self.predecessor.getNodeAt(pos)
		else:
			if len(self.childs)>1:
				for i in range(0,len(self.childs)-1):
					j =i+1
					if pos < self.childs[j].pos:
						return self.childs[i].getNodeAt(pos)
				return self.childs[-1].getNodeAt(pos)

			elif len(self.childs)>0:
				return self.childs[0].getNodeAt(pos)

			return None


	def to_string(self):
		tstr = self.val

		for node in self.childs:
			#if node.isBranch():
			#	tstr += '['
			tstr += str(node.to_string())
			#if node.isBranch():
			#	tstr += ']'
		return tstr

	def print_tree(self, indent=0):		
		ostr = str().zfill(indent).replace('0',' ') + self.val
		ostr += " ("+ str(self.depth)+")"
		print ostr
		for node in self.childs:
			node.print_tree(indent+2)

class LTree(object):
	def __init__(self):
		self.states = []
		self.root = LNode()
		self.node = self.root

	def __lshift__(self,instr):
		if type(instr)==type(str()):
			self.push(instr)

	def push(self, instr):
		slen = len(instr)
		i = 0

		while i <slen:
			if instr[i]=='[':
				self.states.append(node)
				self.node = self.node.addChild(instr[i],i)
				new_branch = True
			elif instr[i]==']':
				self.node = self.node.addChild(instr[i],i)
				self.node = self.states.pop()
			else:
				key = instr[i]
				oi = i
				if i+1 < slen:
					if instr[i+1]=='_':
						key += instr[i+1:i+3]
						i+=2

				self.node = self.node.addChild(key, oi)

			i+=1

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
		bf_rule = LNode(bf_str)
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
		af_rule = LNode(af_str)
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

	for n in range(1,nmax+1):
		oldstr = instr
		itree = LNode(oldstr)
		instr = ''
		sLen = len(oldstr)
		i = 0
		oi = 0
		node = itree
		while True:
			rule_exists, rkey = tree_lookup(node, rules)

			if rule_exists:
				if type(rules[rkey])==type(str()):
					instr = instr + rules[rkey]
				elif type(rules[rkey])==type(dict()):
					instr = instr + resolve_prob_rule(rules[rkey])

			else:
				instr = instr + node.val

			try:
				node = node.next()
			except StopIteration:
				break

		#print 'n=',n,', ', instr
	if (len(figures.keys())>0):
		instr = resolve_instructions(instr,figures,1);
	return instr




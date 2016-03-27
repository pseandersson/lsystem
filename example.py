import lsystem as ls
import turtle as t
import numpy as np
#from lviewer import *

figures ={'L':'','R':''}

instr =	'A'
rules = {
'A':'B-F+CFC+F-D&F^D-F+&&CFC+F+B//',
'B':'A&F^CFB^F^D^^-F-D^|F^B|FC^F^A//',
'C':'|D^|F^B-F+C^F^A&&FA&F^C+F+B^F^D//',
'D':'|CFB-F+B|FA&F^A&&FB-F+B|FC//'}


 
X0 = np.array([0,0,0])
R0 = np.eye(3)

stepsize=0.1
delta = 22.5
dr = 0.001
r0 = 0.01

generations = 10
instr = 'A'
rules = {
'A':'[&FL!A]/////\'[&FL!A]//////\'[&FL!A]',
'F':'S ///// F',
'S':'F L',
'L':'[\'\'\'^^{-f+f+f-|-f+f+f}]'}
# Alternative rules
ignore = '+-F' 

#dummy string='ABC[DE][SG[HI[JK]L]MNO]'
#give matching algorithm acces to
#the whole string.
#rules = {
	# Probabilities
#	'A':{'AB':1,'BA':1}
	# Conditional
#	'B>A':'AB',
#	'A<B':'BB',
#	'A<B>A':'BB',
#	'BC<S>GHM':'',
#	'A(x,y):y<=3':'A(x*2,x+y)'
#	'B(x):x>=1':'B(x-1)'
#}
#
instr ='ABC[DE][SG[HI[JK]L]MNO]'
#instr ='baaaaaa'
rules = {
'A':'X',
}
i = 3
mask = int('0xFFFF',16)
i &=~2
print (1<<0), i,(mask&~2)&i

print ls.parse_rule(instr,2,'a>b')
print '---------------------'
#for g in range(0,generations):
ltree = ls.LNode(instr)
lrule = ls.LNode('BC')
lrule2 = ls.LNode('G[HIL]M')
ltree.print_tree()
lrule.print_tree()
#lrule2.print_tree()

print instr
print lrule
l0 = ltree.getNodeAt(9)
#r0 = lrule.getNodeAt(0)
#l1 = l0.next()
#print l1.print_tree()
#print lrule2.print_tree()
if l0.match(lrule2):
	print 'Equal'
#if l0!=None:
#	print lrule.depth
#	for i in range(0,lrule.depth):
#		l0 = l0.up()
#
#	if l0==lrule:
#		print 'Equal',i
#
#else:
#	print 'Error'



iostr = ls.resolve_instructions_by_tree(instr, rules,2)
print iostr
#turtle = t.turtle(instr,X0,R0,r0,stepsize,delta,dr)
#draw_turtle(turtle)


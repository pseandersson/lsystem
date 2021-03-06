"""
Apologies for lot of comments, will clean this
up in the future.
"""
from lsystem import lsystem as ls
from lsystem import turtle as t
import numpy as np
import string
import cProfile
from lsystem.lviewer import *

figures = {'L': '', 'R': ''}

instr = 'A'
rules = {
    'A': 'B-F+CFC+F-D&F^D-F+&&CFC+F+B//',
    'B': 'A&F^CFB^F^D^^-F-D^|F^B|FC^F^A//',
    'C': '|D^|F^B-F+C^F^A&&FA&F^C+F+B^F^D//',
    'D': '|CFB-F+B|FA&F^A&&FB-F+B|FC//'}


X0 = np.array([0, 0, 0])
R0 = np.eye(3)

stepsize = 0.1
delta = 86
dr = 0.001
r0 = 0.01

generations = 7
instr = 'A'
rules = {
    'A': '[&FL!A]/////\'[&FL!A]//////\'[&FL!A]',
    'F': 'S ///// F',
    'S': 'F L',
    'L': '[\'\'\'^^{-f+f+f-|-f+f+f}]'}
# Alternative rules
#ignore = '+-F'

# dummy string='ABC[DE][SG[HI[JK]L]MNO]'
# give matching algorithm acces to
# the whole string.
# rules = {
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
#instr ='A(5,4)BC[DE][SG[HI[JK]L]MNO]'
#instr ='bbbaaaaa'
# rules = {
#'A(x,y): x+y <10':{'A((x+y)v25,(x*y)v30)':1,'A(x,y)':1},
#'BC<S>G[HIL]M':'X'
#}
i = 3
mask = int('0xFFFF', 16)
i &= ~2
print(1 << 0, i, (mask & ~2) & i)

# print (ls.parse_rule(instr,2,'a>b'))
print('---------------------')
# for g in range(0,generations):
#ltree = ls.LTree()
#ltree << instr
#lrule = ls.LTree()
#lrule << 'BC'
#lrule = lrule.chop()
#lrule2 = ls.LTree() << 'G[HIL]M'
# ltree.print_tree()
# lrule.print_tree()
# lrule2.print_tree()
A = ls.LTree() << 'X(4,3)'
B = ls.LTree() << 'B(x)'
# print instr
# print lrule
#l0 = ltree.getNodeAt(9)
#r0 = lrule.getNodeAt(0)
#l1 = l0.next()
# print l1.print_tree()
# print lrule2.print_tree()
# if l0.match(lrule2):
# x	print 'Equal'
# if l0!=None:
#	print lrule.depth
#	for i in range(0,lrule.depth):
#		l0 = l0.up()
#
#	if l0==lrule:
#		print 'Equal',i
#
# else:
#	print 'Error'


# print ls.calculate('2((3*5e-1)/4-2)-3')
# print ls.calculate('(5)+3')
# print ls.calculate('(5)*3')
# print ls.calculate('(5)/3')
# print ls.calculate('(4-2)^2')
# print ls.calculate('-2^2')
# print ls.calculate('4-3')
# print ls.calculate('(-2)^2')
# print ls.calculate('(-3)^2*2-3')
# print ls.calculate('5*(-2)^2')
# print ls.calculate('5-(-2)^2')
# print ls.calculate('2-4^.5')
# print ls.calculate('-4.3+3*(2-5)/(2.3-0.3)+4')
# print ls.calculate('2*(2v(3/2))')

# for g in range(1,6):
#	iostr = ls.resolve_instructions_by_tree(instr, rules,g)
#<	print iostr.to_string()
#instr = 'F1F1F1'
# rules = {
#	'0<0>0':'0',
#	'0<0>1':'1[-F1F1]',
#	'0<1>0':'1',
#	'0<1>1':'1',
#	'1<0>0':'0',
#	'1<0>1':'1F1',
#	'1<1>0':'1',
#	'1<1>1':'0',
#	'*<+>*':'-',
#	'*<->*':'+'
#}
# ignore='+-F'
#
instr = 'F(1,0)'
#
define = {
    'c': '1',
    'p': '0.3',
    'q': 'c-p',
    'h': '(p*q)^0.5'
}
#
# rules= {
#	'F(x)':'F(x*p)+F(x*h)--F(x*h)+F(x*q)'
#}
rules = {
    'F(x,t):t==0': 'F(x*p,2)+F(x*h,1)--F(x*h,1)+F(x*q,0)',
    'F(x,t):t>0': 'F(x,t-1)'
}
# define = {
#	'R':'1.456'
#}
#instr ='+(-90.)A(1)'
# rules= {
#	'A(s)':'F(s)[+A(s/R)][-A(s/R)]'
#}
bench_sys = ls.LSystem()\
    .set_definitions(define)\
    .set_rules(rules)\
    .set_max_iterations(14)

# ls.resolve_instructions_by_tree(instr,rules,14,definitions=define)
# cProfile.run('itree = ls.resolve_instructions_by_tree(instr,rules,14,definitions=define)', 'restats')
cProfile.run('itree = bench_sys.solve(instr)', 'restats')
# itree = ls.resolve_instructions_by_tree(instr,rules,4,definitions=define)
# print(itree.to_string())
#itree = ls.resolve_instructions_by_tree(itree,rules,1,ignore=ignore)
# print itree.to_string()
#itree = ls.resolve_instructions_by_tree(itree,rules,1,ignore=ignore)
# print itree.to_string()
#itree = ls.resolve_instructions_by_tree(itree,rules,1,ignore=ignore)
# print itree.to_string()

# print itree.to_string()
# itree = ls.LSystem()\
#     .set_rules({
#         '0<0>0':'0',
#         '0<0>1':'1[-F1F1]',
#         '0<1>0':'1',
#         '0<1>1':'1',
#         '1<0>0':'0',
#         '1<0>1':'1F1',
#         '1<1>0':'1',
#         '1<1>1':'0',
#         '*<+>*':'-',
#         '*<->*':'+'
#     })\
#     .set_ignore('F+-')\
#     .set_max_iterations(12)\
#     .solve('F1F1F1')
# itree = bench_sys.solve(instr)
turtle = t.turtle_tree(itree, X0, R0, r0, stepsize, delta, dr)
# print(itree.to_string())
print('Done!')
import pstats
p = pstats.Stats('restats')
p.sort_stats('cumulative').print_stats()

draw_turtle(turtle)

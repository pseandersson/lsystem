import unittest
from lsystem.lsystem import LNode, LTree, LNodeIterator, LNodeInsertIterator
from lsystem.lmath import Expression

class TreeTests(unittest.TestCase):
    def test_with_branches(self):
        itree = LTree('A')
        itree << 'B[CD]E[F][G]H'
        nodes = itree.chop()
        exp_node_str = \
"""A
 B
  [
   C
    D
     ]
  E
   [
    F
     ]
   [
    G
     ]
   H"""
        act_node_string = nodes.to_string(True, True)
        self.assertEqual(act_node_string, exp_node_str)

    def test_insert_node_tree_and_string(self):
        itree = LTree('A')
        exp_node_str = \
"""A
 B
  [
   C
    D
     ]
  E
   [
    F
     ]
   [
    G
     ]
   H"""

        B = LNode('B')
        B.add_child('[').add_child('C').add_child('D').add_child(']')
        E = B.add_child('E')
        E.add_child('[').add_child('F').add_child(']')
        E.add_child('[').add_child('G').add_child(']')
        itree << B << 'H'

        nodes = itree.chop()

        act_node_string = nodes.to_string(True, True)
        self.assertEqual(act_node_string, exp_node_str)

    def test_insert_empty_string_or_nodes(self):
        itree = LTree('')
        A = LNode('')
        itree << A << A << '' << ''
        nodes = itree.chop()
        self.assertEqual(nodes.val,'')
        self.assertEqual(len(nodes.get_childs()),0)
        # self.assertIsNone(nodes)

    def test_insert_limited_nodes(self):
        itree = LTree('')
        A = LNode('A')
        A.add_child('B').add_child('C').add_child('D')
        itree << 1 << A << A
        nodes = itree.chop()

        self.assertEqual(nodes.to_string(True),'AABCD')

    def test_insert_insert_iterator(self):
        itree = LTree('')
        A = LNode('A')
        A.add_child('B').add_child('C').add_child('D')
        itree << LNodeInsertIterator(A)
        nodes = itree.chop()

        self.assertEqual(nodes.to_string(True),'ABCD')

    def test_not_parse_arguments(self):
        itree = LTree('', False)
        itree = LTree('', False)
        itree << 'A(a,b)'
        nodes = itree.chop()
        self.assertEqual(nodes.get_arguments(), ['a', 'b'])
        itree = LTree()
        itree << 'A(a,b)'
        nodes = itree.chop()
        self.assertTrue(all([isinstance(x, Expression) for x in nodes.get_arguments()]))

if __name__ == "__main__":
    unittest.main()

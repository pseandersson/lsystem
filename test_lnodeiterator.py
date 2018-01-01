import unittest
from lsystem import LNode, LNodeIterator, LNodeInsertIterator

class LNodeInsertIteratorTests(unittest.TestCase):
    def test_simple_copying(self):
        A = LNode('A')
        B = LNode('B')

        for node in LNodeInsertIterator(A, B):
            pass

        exp_nodes = ['A', 'B']
        act_nodes = []

        for i in LNodeIterator(A):
            act_nodes.append(i.val)
        self.assertEqual(act_nodes, exp_nodes)

    def test_simple_copying_deep(self):
        A = LNode('A')
        B = LNode('B')
        B.add_child('C').add_child('D')

        for node in LNodeInsertIterator(A, B):
            pass

        exp_nodes = ['A', 'B', 'C', 'D']
        act_nodes = []

        for i in LNodeIterator(A):
            act_nodes.append(i.val)
        self.assertEqual(act_nodes, exp_nodes)

    def test_copying_branches(self):
        A = LNode('A')
        B = LNode('B')
        B.add_child('C').add_child('D')
        E = B.add_child('E')
        E.add_child('F')
        E.add_child('G')
        for node in LNodeInsertIterator(A, B):
            pass
        exp_node_str = \
"""A
 B
  C
   D
  E
   F
   G"""

        act_node_string = A.to_string(True, True)
        self.assertEqual(act_node_string, exp_node_str)

    def test_get_last_copied_node(self):
        A = LNode('A')
        B = LNode('B')
        B.add_child('C').add_child('D')
        E = B.add_child('E')
        E.add_child('F')
        E.add_child('G')
        itr = LNodeInsertIterator(A, B)
        for node in itr:
            pass
        exp_node_str = \
"""A
 B
  C
   D
  E
   F
   G"""
        act_node_string = A.to_string(True, True)
        self.assertEqual(act_node_string, exp_node_str)
        self.assertEqual(itr.get_end_node().val, 'G')

class LNodeIteratorTests(unittest.TestCase):
    def test_iterate_one_item(self):
        """Test if the iterator works properly"""
        node = LNode('A')
        itr = LNodeIterator(node)
        count = 0
        for n in itr:
            count += 1
        self.assertEqual(count, 1)

    def test_iterate_two_item(self):
        """Test if the iterator works for two items"""
        node = LNode('A')
        node.add_child('B')
        itr = LNodeIterator(node)
        count = 0
        for n in itr:
            count += 1
        self.assertEqual(count, 2)

    def test_iterate_higharchy_item(self):
        """Test if the iterator works in higharchies items"""
        node = LNode('A')
        bnode = node.add_child('B')
        node.add_child('C')
        itr = LNodeIterator(bnode)
        count = 0
        for n in itr:
            count += 1
        self.assertEqual(count, 2)

    def test_iterate_higharchy_item_last(self):
        """Test if the iterator works in higharchies items"""
        node = LNode('A')
        node.add_child('B')
        C = node.add_child('C')
        itr = LNodeIterator(C)
        count = 0
        for n in itr:
            count += 1
        self.assertEqual(count, 1)

if __name__ == "__main__":
    unittest.main()
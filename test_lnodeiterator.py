import unittest
from lsystem import LNode, LNodeIterator, LNodeInsertIterator
from lmath import Expression

class LNodeInsertIteratorTests(unittest.TestCase):
    def test_simple_copying(self):
        A = LNode('A')
        B = LNode('B')

        for node, ref in LNodeInsertIterator(B, A):
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

        for node in LNodeInsertIterator(B, A):
            pass

        exp_nodes = ['A', 'B', 'C', 'D']
        act_nodes = []

        for i in LNodeIterator(A):
            act_nodes.append(i.val)
        self.assertEqual(act_nodes, exp_nodes)
    def test_simple_copying_deep_limit(self):
        A = LNode('A')
        B = LNode('B')
        B.add_child('C').add_child('D')

        for node in LNodeInsertIterator(B, A, 1):
            pass

        exp_nodes = ['A', 'B']
        act_nodes = []

        for i in LNodeIterator(A):
            act_nodes.append(i.val)
        self.assertEqual(act_nodes, exp_nodes)
    def test_simple_copying_deep_set_limit(self):
        A = LNode('A')
        B = LNode('B')
        B.add_child('C').add_child('D')
        lii = LNodeInsertIterator(B, A)
        lii.set_limit(1)
        for node in lii:
            pass

        exp_nodes = ['A', 'B']
        act_nodes = []

        for i in LNodeIterator(A):
            act_nodes.append(i.val)
        self.assertEqual(act_nodes, exp_nodes)
    def test_transfer_arguments_on_copy(self):
        expr = Expression('a^2')
        A =  LNode('A')
        A.set_arguments([expr])
        itr = LNodeInsertIterator(A, None, 1)
        for i in itr:
            pass

        self.assertEqual(itr.get_begin_node().get_argument(0), expr)

    def test_evaluate_arguments_on_copy(self):
        expr = Expression('a^2')
        A =  LNode('A')
        A.set_arguments([expr])
        itr = LNodeInsertIterator(A, a=3)
        for i in itr:
            pass

        self.assertEqual(itr.get_begin_node().get_argument(0), 9)

    def test_copying_branches(self):
        A = LNode('A')
        B = LNode('B')
        B.add_child('[').add_child('C').add_child('D').add_child(']')
        E = B.add_child('E')
        E.add_child('[').add_child('F').add_child(']')
        E.add_child('[').add_child('G').add_child(']')
        lii = LNodeInsertIterator(B, A)
        for node in lii:
            pass
        self.assertEqual(lii.get_end_node().val, 'E')
        lii.get_end_node().add_child('H')
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
        act_node_string = A.to_string(True, True)
        self.assertEqual(act_node_string, exp_node_str)

    def test_get_last_copied_node(self):
        A = LNode('A')
        B = LNode('B')
        B.add_child('C').add_child('D')
        E = B.add_child('E')
        E.add_child('F')
        E.add_child('G')
        itr = LNodeInsertIterator(B, A)
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

    def test_copy_into_new(self):
        """Test of copy to new operation"""
        A = LNode('A')
        A.add_child('B').add_child('C')
        itr = LNodeInsertIterator(A)
        for a in itr:
            pass
        self.assertEqual(itr.get_begin_node().val, 'A')
        self.assertEqual(itr.get_end_node().val, 'C')
    def test_copy_into_existing_empty_first(self):
        """Test of copy to new operation"""
        A = LNode('A')
        B = LNode('')
        B.add_child('').add_child('B').add_child('C')
        itr = LNodeInsertIterator(B, A)
        for a in itr:
            pass
        self.assertEqual(itr.get_begin_node().val, 'A')
        self.assertEqual(itr.get_end_node().val, 'C')

    def test_copy_into_new_access_template(self):
        """Test of copy to new operation"""
        A = LNode('A')
        A.set_arguments('123')
        A.add_child('B').add_child('C')
        itr = LNodeInsertIterator(A)
        count = 0
        for a, b in itr:
            count += 1
        self.assertEqual(itr.get_begin_node().val, 'A')
        self.assertEqual(itr.get_end_node().val, 'C')
        self.assertEqual(count, 3)

    def test_copy_empty_nodes_to_new(self):
        """Test of copy to new operation"""
        A = LNode('A')
        A.add_child('').add_child('')
        itr = LNodeInsertIterator(A)
        for a, b in itr:
            self.assertNotEqual(a, b)
            self.assertEqual(a, a)
            pass
        self.assertEqual(itr.get_begin_node().val, 'A')
        self.assertEqual(itr.get_end_node().val, 'A')

    def test_insert_empty_nodes(self):
        """Test of empty values to an existing node tree"""
        A = LNode('A')
        B = LNode('')
        B.add_child('').add_child('')
        itr = LNodeInsertIterator(B, A)
        for a, b in itr:
            self.assertNotEqual(a, b)
            self.assertEqual(a, a)
            pass
        self.assertEqual(itr.get_begin_node().val, 'A')
        self.assertEqual(itr.get_end_node().val, 'A')

    def test_only_empty_nodes(self):
        """Test of copy empty nodes to new node-tree"""
        A = LNode('')
        A.add_child('').add_child('')
        itr = LNodeInsertIterator(A)
        for a, b in itr:
            self.assertNotEqual(a, b)
            self.assertEqual(a, a)

        self.assertEqual(itr.get_begin_node().val, '')
        self.assertEqual(itr.get_end_node().val, '')
        self.assertFalse(itr.get_begin_node().get_childs())

    def test_set_target(self):
        """Test of copy to existing target, by
        using the set_target method"""
        A = LNode('A')
        A.set_arguments('123')
        A.add_child('B').add_child('C')
        itr = LNodeInsertIterator(A)
        N = LNode('N')
        itr.set_target(N)
        count = 0
        for a, b in itr:
            pass

        for n in LNodeIterator(N):
            count += 1

        self.assertEqual(itr.get_begin_node().val, 'A')
        self.assertEqual(itr.get_end_node().val, 'C')
        self.assertEqual(count, 4)

    def test_set_kwargs(self):
        """Test of copy to existing target, by
        using the set_target method"""
        A = LNode('A')
        A.set_arguments('(a*4)')
        A.add_child('B').add_child('C')
        itr = LNodeInsertIterator(A, a=3.)
        N = LNode('N')
        itr.set_target(N)
        itr.set_kwargs(a=7.)
        count = 0
        for a, b in itr:
            pass

        for n in LNodeIterator(N):
            count += 1

        self.assertEqual(itr.get_begin_node().val, 'A')
        self.assertEqual(itr.get_begin_node().get_argument(0), 28)
        self.assertEqual(itr.get_end_node().val, 'C')
        self.assertEqual(count, 4)


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
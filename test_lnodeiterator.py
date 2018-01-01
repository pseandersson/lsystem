import unittest
from lsystem import LNode, LNodeIterator

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
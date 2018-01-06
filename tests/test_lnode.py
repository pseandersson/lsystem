"""
Tests for the LNode Item
"""
import unittest
from lsystem.lsystem import LNode
from lsystem.lmath import Expression

class LNodeTests(unittest.TestCase):

    def create_node(self):
        A = LNode('A')
        self.assertEqual(A.val, 'A')
        self.assertEqual(A.predecessor, None)
        B = LNode('B', A)
        self.assertEqual(B.val, 'B')
        self.assertEqual(B.predecessor, A)

    def test_set_arguments(self):
        """Test of setting arguments"""
        A = LNode('A')
        A.set_arguments([1.0, 2.0])
        self.assertEqual(A.get_arguments(), [1.0, 2.0])
        A.set_arguments((3.0, 4.0))
        self.assertEqual(A.get_arguments(), (3.0, 4.0,))
        A.set_arguments('(a,b)', False)
        self.assertEqual(A.get_arguments(), ['a', 'b'])
        A.set_arguments('(a,b)')
        self.assertTrue(all(isinstance(x, Expression) for x in A.get_arguments()))




if __name__ == "__main__":
    unittest.main()
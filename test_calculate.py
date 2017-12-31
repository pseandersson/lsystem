import unittest
from lsystem import calculate, Calculator

# class TestCalculator(unittest.TestCase):
#     """Class to test a faster calculator"""
#     def test_single(self):
#         c = Calculator()
#         self.assertEqual(c.calc('1'), 1.0)

#     def test_addition(self):
#         c = Calculator()
#         self.assertEqual(c.calc('1+2'), 3.0)

class TestCalculateMethod(unittest.TestCase):
    """Class which tests the calculate part of lsystem"""
    def test_e_behaivour(self):
        """Test expressions like 4e-1"""
        self.assertAlmostEqual(calculate('4e-1'), 0.4)
    def test_mul_par_e_div_min_min(self):
        """Test a complex expression"""
        self.assertAlmostEqual(calculate('2((3*5e-1)/4-2)-3'), -6.25)
    def test_par_add(self):
        """Test add with parentheries"""
        self.assertEqual(calculate('(5)+3'), 8)
    def test_par_mul(self):
        """Test multiplication with parentheries"""
        self.assertEqual(calculate('(5)*3'), 15)
    def test_div(self):
        """Test divsion with parentheries"""
        self.assertEqual(calculate('(5)/3'), 5/3)
    def test_scope_exp(self):
        """Test power of"""
        self.assertEqual(calculate('(4-2)^2'), 4)
    def test_min_to_pow_of_two(self):
        self.assertEqual(calculate('-2^2'), -4)
    def test_subtract(self):
        """Test of subtraction"""
        self.assertEqual(calculate('4-3'), 1)
    def test_subtract_neg_val(self):
        """Test subtraction if negation twice"""
        self.assertEqual(calculate('4--3'), 7)
    def test_neg_val_to_pow_of_two(self):
        self.assertEqual(calculate('(-2)^2'),4)
    def test_neg_val_to_pow_mul_min(self):
        self.assertEqual(calculate('(-3)^2*2-3'),15)
    def test_mul_neg_val_to_pow(self):
        self.assertEqual(calculate('5*(-2)^2'), 20)
    def test_val_min_neg_val_to_pow(self):
        self.assertEqual(calculate('5-(-2)^2'), 1)
    def test_val_min_val_to_decimal_pos(self):
        self.assertEqual(calculate('2-4^.5'), 0)
    def test_dec_add_val_mul_scope_div_scope_add(self):
        self.assertAlmostEqual(calculate('-4.3+3*(2-5)/(2.3-0.3)+4'), -4.8)
    def test_val_mininum_scope(self):
        """v denotes the min operator"""
        self.assertEqual(calculate('2*(2v(3/2))'), 4)

if __name__ == "__main__":
    unittest.main()

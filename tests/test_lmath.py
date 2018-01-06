"""
Tests for expressions and calculate
"""
import unittest

from random import choice, uniform
from lsystem.lmath import calculate, Expression, Operator

class TestExpression(unittest.TestCase):
    def test_add(self):
        """Test a simple expression"""
        expr = Expression('a+1')
        self.assertEqual(expr(a=1.), 2)

    def test_subtract(self):
        """Test a simple expression"""
        expr = Expression('t-1')
        self.assertEqual(expr(t=3.), 2)

    def test_mul(self):
        """Test a simple linear expression"""
        expr = Expression('5*a+2')
        self.assertEqual(expr(a=2.), 12)


    def test_pow(self):
        """Test a simple linear expression"""
        expr = Expression('a^2')
        self.assertEqual(expr(a=3.), 9)

    def test_passing_vars(self):
        expr = Expression('a^2')
        def fn(in_expr, **kwargs):
            return in_expr(**kwargs)
        self.assertEqual(fn(expr, a=3), 9)

    def test_constant_expression(self):
        """Test a constant expression e.g 5*3 + 1"""
        expr = Expression('5*3+1')
        self.assertTrue(expr.is_constant())
        self.assertEqual(expr(), 16)

class TestOperations(unittest.TestCase):
    """Class to test a faster calculator"""

    def test_operators_only_numbers(self):
        """Iterate over each operatore and do the math"""
        N = 10
        for i in range(N):
            # ops = [OpAdd, OpDivide, OpMin, OpMultiply, OpPower, OpSubtract]
            ref_ops = [float.__add__, float.__truediv__,
                       min, float.__mul__, pow, float.__sub__]

            a = [uniform(-10, 10) for x in ref_ops]
            b = [choice((-1, 1)) * uniform(0.00001, 10) for x in ref_ops]

            ops = [Operator(x, y, op) for x, y, op in zip(a, b, ref_ops)]

            ops[:] = [ops[i]() for i, x in enumerate(b)]
            ref_ops[:] = [ref_ops[i](x, y)
                          for i, (x, y) in enumerate(zip(a, b))]
            self.assertListEqual(ops, ref_ops)

    def test_operators_with_numbers_and_args(self):
        """Iterate over each operatore and do the math with custom arguments"""
        N = 10
        for i in range(N):
            # ops = [OpAdd, OpDivide, OpMin, OpMultiply, OpPower, OpSubtract]
            ref_ops = [float.__add__, float.__truediv__,
                       min, float.__mul__, pow, float.__sub__]

            a = [uniform(-10, 10) for x in ref_ops]
            b = [choice((-1, 1)) * uniform(0.00001, 10) for x in ref_ops]

            ops = [Operator(x, 'x', op) for x, op in zip(a, ref_ops)]

            ops[:] = [ops[i](**{'x': x}) for i, x in enumerate(b)]
            ref_ops[:] = [ref_ops[i](x, y)
                          for i, (x, y) in enumerate(zip(a, b))]
            self.assertListEqual(ops, ref_ops)

    def test_operators_with_only_args(self):
        """Iterate over each operatore and do the math with custom arguments"""
        N = 10
        for i in range(N):
            # ops = [OpAdd, OpDivide, OpMin, OpMultiply, OpPower, OpSubtract]
            ref_ops = [float.__add__, float.__truediv__,
                       min, float.__mul__, pow, float.__sub__]

            a = [uniform(-10, 10) for x in ref_ops]
            b = [choice((-1, 1)) * uniform(0.00001, 10) for x in ref_ops]

            ops = [Operator('a','b', op) for x, op in zip(a, ref_ops)]

            ops[:] = [ops[i](**{'a': x, 'b': y})
                      for i, (x, y) in enumerate(zip(a, b))]
            ref_ops[:] = [ref_ops[i](x, y)
                          for i, (x, y) in enumerate(zip(a, b))]
            self.assertListEqual(ops, ref_ops)

    def test_operator_multiply(self):
        """test expressions like 1+2*3"""
        opr2 = Operator(2., 3., float.__mul__)
        opr1 = Operator(1., opr2, float.__add__)

        self.assertEqual(opr1(), 7)

    def test_operator_multiply_dual(self):
        """test expressions like 1+2*3+4"""
        opr2 = Operator(2., 3., float.__mul__)
        opr1 = Operator(1., opr2, float.__add__)
        opr3 = Operator(opr1, 4., float.__add__)

        self.assertEqual(opr3(), 11)

    def test_operator_multiply_args(self):
        """test expressions like x+2*3"""
        opr2 = Operator(2., 3., float.__mul__)
        opr1 = Operator('x', opr2, float.__add__)
        args = {'x': 1.}
        self.assertEqual(opr1(**args), 7)

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
        self.assertEqual(calculate('(5)/3'), 5 / 3)

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
        self.assertEqual(calculate('(-2)^2'), 4)

    def test_neg_val_to_pow_mul_min(self):
        self.assertEqual(calculate('(-3)^2*2-3'), 15)

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
        self.assertEqual(calculate('2*(2v(3/2))'), 3)
        self.assertEqual(calculate('2*((3/2)v2)'), 3)


if __name__ == "__main__":
    unittest.main()

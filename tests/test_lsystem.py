import unittest
from lsystem.lsystem import LSystem
import re

class LSystemTests(unittest.TestCase):
    def test_zero_iterations(self):
        res = LSystem()\
            .set_rules({
                "A": "AB",
                "B": "A"
            })\
            .set_max_iterations(0)\
            .solve('A')\
            .to_string()
        self.assertEqual(res, 'A')

    def test_four_iterations(self):
        """Test a simple system with four iterations"""
        res = LSystem()\
            .set_rules({
                "A": "AB",
                "B": "A"
            })\
            .set_max_iterations(4)\
            .solve('A')\
            .to_string()
        self.assertEqual(res, 'ABAABABA')

    def test_arguments(self):
        """Test some rule with arguments"""
        res = LSystem()\
            .set_definitions({
                'c': '1',
                'p': '0.3',
                'q': 'c-p',
                'h': '(p*q)^0.5'
            })\
            .set_rules({
                'F(x,t):t==0': 'F(x*p,2)+F(x*h,1)--F(x*h,1)+F(x*q,0)',
                'F(x,t):t>0': 'F(x,t-1)'
            })\
            .set_max_iterations(2)\
            .solve('F(1,0)').chop().to_string(True, False, 1, True)

        def F(**kwargs):
            a = str(kwargs.get('x', '[\+\-\d.]+')).replace('.', '\.')
            b = str(kwargs.get('t', '[\+\-\d.]+')).replace('.', '\.')
            return "F\(" + a + "," + b + "\)"

        rule_a_1 = F(t=2.0) + "\+" + F(t=1.0) + "\-\-" + F(t=1.0) + "\+" + F(t=0.0)
        rule_a_2 = F(t=1.0) + "\+" + F(t=0.0) + "\-\-" + F(t=0.0) + "\+" + rule_a_1
        exp_pattern = re.compile(rule_a_2)

        print(res)

        # self.assertEqual(res, exp_2)
        self.assertTrue(exp_pattern.match(res))

    def test_logics(self):
        """Test heavily logic rules"""
        expected = ("F1F1F1F1[+F0F1]F1[-F0F1[-F1F1]F1]"
                    "F0F1[-F1F1][+F1F0F0F1][-F1[-F1F1]"
                    "F1[+F0F1]F0[-F1F1F1]F1]F1")
        res = LSystem()\
            .set_rules({
                '0<0>0': '0',
                '0<0>1': '1[-F1F1]',
                '0<1>0': '1',
                '0<1>1': '1',
                '1<0>0': '0',
                '1<0>1': '1F1',
                '1<1>0': '1',
                '1<1>1': '0',
                '*<+>*': '-',
                '*<->*': '+'
            })\
            .set_ignore('F+-')\
            .set_max_iterations(12)\
            .solve('F1F1F1').to_string()
        self.assertEqual(res, expected)


if __name__ == "__main__":
    unittest.main()

import unittest
from lsystem import LSystem

class LSystemTests(unittest.TestCase):
    def test_zero_iterations(self):
        res = LSystem()\
            .set_rules({
                "A":"AB",
                "B":"A"
            })\
            .set_max_iterations(0)\
            .solve('A')\
            .to_string()
        self.assertEqual(res, 'A')
    def test_four_iterations(self):
        """Test a simple system with four iterations"""
        res = LSystem()\
            .set_rules({
                "A":"AB",
                "B":"A"
            })\
            .set_max_iterations(4)\
            .solve('A')\
            .to_string()
        self.assertEqual(res, 'ABAABABA')

    def test_logics(self):
        """Test heavily logic rules"""
        expected = ("F1F1F1F1[+F0F1]F1[-F0F1[-F1F1]F1]"
                    "F0F1[-F1F1][+F1F0F0F1][-F1[-F1F1]"
                    "F1[+F0F1]F0[-F1F1F1]F1]F1")
        res = LSystem()\
                .set_rules({
                    '0<0>0':'0',
                	   '0<0>1':'1[-F1F1]',
                	   '0<1>0':'1',
                	   '0<1>1':'1',
                	   '1<0>0':'0',
                	   '1<0>1':'1F1',
                	   '1<1>0':'1',
                	   '1<1>1':'0',
                	   '*<+>*':'-',
                	   '*<->*':'+'
                })\
                .set_ignore('F+-')\
                .set_max_iterations(12)\
                .solve('F1F1F1').to_string()
        self.assertEqual(res, expected)

if __name__ == "__main__":
    unittest.main()
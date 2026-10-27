import unittest
from src.calculator import sum, substract, divide

class CalculatorTests(unittest.TestCase):

    def test_sum(self):
        assert sum(2,3) == 5

    def test_substract(self):
        assert substract(2,3) == -1

    def test_divide(self):
        with self.assertRaises(ValueError):
            result = divide(1,0)
        result = divide(10,5)
        expected = 2
        assert result == expected
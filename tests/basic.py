import unittest
from main import math_single_core_test


class TestBasicTools(unittest.TestCase):

    def test_single_core_exceptions(self):
        with self.assertRaises(ValueError):
            vals = (1, 2, 3)
            math_single_core_test(vals)

        with self.assertRaises(ValueError):
            vals = (0, 25)
            math_single_core_test(vals)

        with self.assertRaises(AttributeError):
            vals = ('a', 25)
            math_single_core_test(vals)

        with self.assertRaises(AttributeError):
            vals = (25, 'a')
            math_single_core_test(vals)

        with self.assertRaises(AttributeError):
            vals = (['a'], 25)
            math_single_core_test(vals)


if __name__ == '__main__':
    unittest.main()
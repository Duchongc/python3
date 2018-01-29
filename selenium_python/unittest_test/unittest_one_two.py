import unittest
from unittest_test import unittest_two,unittest_one
suit = unittest.TestSuite()
suit.addTest(unittest_one.test('test_01'))
suit.addTest(unittest_two.YoudaoTest('test_youdao'))
if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suit)
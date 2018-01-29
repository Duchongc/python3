import unittest
import sys

def add(a,b):
    return a + b
class demoTest(unittest.TestCase):
    def test_add_4_5(self):
        self.assertEqual(add(4,5),9)

if __name__ == '__main__':
    unittest.main()
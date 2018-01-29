import unittest
import random

class MyClass(object):
    @classmethod
    def sum(cls,a,b):
        return a + b
    @classmethod
    def div(cls,a,b):
        return a / b
    @classmethod
    def return_None(cls):
        return None

class MyTest(unittest.TestCase):
    def test_assertEqual(self):
        try:
            a,b = 1,2
            sum = 13
            self.assertEqual(a + b,sum,'duanyanshibai,%s + %s!= %s' %(a,b,sum))
        except AssertionError:
            print()
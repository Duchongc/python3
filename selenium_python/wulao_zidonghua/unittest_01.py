import unittest

class myclass(object):
    @classmethod
    def sum(cls,a,b):
        return a + b
    @classmethod
    def sub(cls,a,b):
        return a - b
class mytest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('-----setUpClass')
    @classmethod
    def tearDownClass(cls):
        print('-----tearDownClass')
    def setUp(self):
        self.a = 3
        self.b = 1
        print('--setUp')
    def tearDown(self):
        print('---teatDown')
    def testsum(self):
        self.assertEqual(myclass.sum(self.a,self.b),4,'test sum fail')
    def testsub(self):
        self.assertEqual(myclass.sub(self.a,self.b),2,'test sub fail')

if __name__ == '__main__':
    unittest.main()
import unittest
import random

class TestSequenceFunctions(unittest.TestCase):
     def setUp(self):
         self.seq = range(10)
     def tearDown(self):
         pass
     def test_choice(self):
         element = random.choice(self.seq)
         self.assertTrue(element in self.seq)
     def test_sample(self):
         with self.assertRaises(ValueError):
             random.sample(self.seq, 20)
         for element in random.sample(self.seq, 5):
             self.assertTrue(element in self.seq)
class TestDictValueFormatFunctions(unittest.TestCase):
    def setUp(self):
        self.seq = range(10)
    def tearDown(self):
        pass
    def test_shuffle(self):
        element = random.choice(self.seq)
        self.assertTrue(element in self.seq)

    def test_sample(self):
        with self.assertRaises(ValueError):
            random.sample(self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assertTrue(element in self.seq)

if __name__ == '__main__':
    testCase1 = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
    testCase2 = unittest.TestLoader().loadTestsFromTestCase(TestDictValueFormatFunctions)
    suite = unittest.TestSuite()
    suite.addTests(testCase1,testCase2)
    unittest.TextTestRunner(verbosity= 2).run(suite)



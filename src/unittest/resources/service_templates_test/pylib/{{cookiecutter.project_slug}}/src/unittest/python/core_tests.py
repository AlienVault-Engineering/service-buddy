import os
import unittest

ROOT_PATH = os.path.dirname(__file__)

class TestCase(unittest.TestCase):


    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_unit_test(self):
        self.assertEqual(True,True,"Woah!")

import unittest



class TestCase(unittest.TestCase):
    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        super(TestCase, cls).setUpClass()

    def test_create_cli(self):
        pass
import os
import tempfile
import unittest

from service_buddy.util import log_handler

DIRNAME = os.path.dirname(os.path.abspath(__file__))


class ParentTestCase(unittest.TestCase):
    def tearDown(self):
        try:
            for _file in os.listdir(self.temp_dir):
                os.remove(_file)
            os.removedirs(self.temp_dir)
        except Exception as e:
            print 'Error cleaning up ' + e.message

    @classmethod
    def setUpClass(cls):
        super(ParentTestCase, cls).setUpClass()
        cls.service_directory = os.path.join(DIRNAME, '../resources/service_definition_test')
        cls.service_templates_test = os.path.join(DIRNAME, '../resources/service_templates_test/')
        cls.temp_dir = tempfile.mkdtemp()
        log_handler.configure_logging(True)

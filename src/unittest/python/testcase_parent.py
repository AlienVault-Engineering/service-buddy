import os
import unittest

from service_manager.util import log_handler

DIRNAME = os.path.dirname(os.path.abspath(__file__))


class ParentTestCase(unittest.TestCase):
    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        super(ParentTestCase, cls).setUpClass()
        cls.service_directory = os.path.join(DIRNAME, '../resources/service_definition_test')
        cls.service_templates_test = os.path.join(DIRNAME, '../resources/service_templates_test/')
        log_handler.configure_logging(True)

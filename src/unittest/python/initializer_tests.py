import os
import random
import string
import unittest

from service_manager.service_initializer.initializer import Initializer
from service_manager.util import services, log_handler

from service_manager.util.services import load_service_definitions
from service_manager.vcs.vcs import VCS
from testcase_parent import ParentTestCase



class InitTestCase(ParentTestCase):
    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        super(InitTestCase, cls).setUpClass()
        cls.vcs = VCS(cls.service_directory,True)
        cls.out_dir = "/tmp/testout-{}".format(''.join(random.choice(string.lowercase) for i in range(5)))


    def validate_generation(self,definition):
        base_path = os.path.join(self.out_dir, definition.get_app(), definition.get_fully_qualified_service_name())
        self.assertTrue(os.path.exists(base_path),"Did not find generated code base")
        self.assertTrue(os.path.exists(os.path.join(base_path,"src")),"Did not find generated code directory")
        self.assertTrue(os.path.exists(os.path.join(base_path,"build.py")),"Did not find generated build file")



    def test_project_init(self):
        application_map = services.load_service_definitions(self.service_directory)
        init = Initializer(self.vcs, self.out_dir, True, self.service_templates_test)
        init.project_creator.dry_run = False
        init.initialize_services(application_map)
        services.walk_service_map(application_map,application_callback=None,service_callback=self.validate_generation)

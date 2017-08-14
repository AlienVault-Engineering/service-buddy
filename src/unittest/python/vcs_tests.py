import os
import unittest

from service_manager.util import services

from service_manager.util.services import load_service_definitions
from service_manager.vcs.vcs import VCS
from testcase_parent import ParentTestCase

DIRNAME = os.path.dirname(os.path.abspath(__file__))


class VCSTestCase(ParentTestCase):
    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        super(VCSTestCase, cls).setUpClass()
        cls.bad_vcs = os.path.join(DIRNAME, 'resources/bad_vcs')


    def test_vcs_init(self):
        try:
            vcs = VCS(self.bad_vcs,True)
            self.fail("Did not except")
        except Exception as E:
            self.assertTrue("vcs_config.json" in E.message)
        vcs = VCS(self.service_directory,True)
        application_map = services.load_service_definitions(self.service_directory)
        vcs.validate_repositories(application_map=application_map)
        vcs.pull_services(application_map=application_map,destination_directory="/tmp/out")
        for key, app in application_map.iteritems():
            for key, service in app.iteritems():
                vcs.init_repo(service,"/tmp/out/{}".format(key))
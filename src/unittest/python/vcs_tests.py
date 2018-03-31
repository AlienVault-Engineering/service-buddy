import os

from service_buddy.service import loader
from service_buddy.vcs.Bitbucket import BitbucketVCSProvider
from service_buddy.vcs.vcs import VCS, vcs_provider_map
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
            self.assertTrue("vcs-config.json" in E.message)
        vcs = VCS(self.service_directory,True)
        self.assertTrue(vcs.default_provider == "bitbucket","Failed to load default provider")
        self.assertTrue(type(vcs_provider_map[vcs.default_provider]) == BitbucketVCSProvider,"Failed to load default provider")
        application_map = loader.load_service_definitions(self.service_directory)
        vcs.validate_repositories(application_map=application_map)
        vcs.clone_service(application_map=application_map, destination_directory="/tmp/out")
        for key, app in application_map.iteritems():
            for key, service in app.iteritems():
                vcs.init_repo(service,"/tmp/out/{}".format(key))
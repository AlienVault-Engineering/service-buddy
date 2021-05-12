from service_buddy_too.service import loader
from testcase_parent import ParentTestCase
from service_buddy_too.vcs.bitbucket import BitbucketVCSProvider


class TestBitbucketClient(object):

    def find_repository_by_full_name(self, full_name, client):
        return RepoReturn(repository_name=full_name)

    def create(self,payload,repository_name,owner,client):
        return RepoReturn(repository_name=repository_name)

class RepoReturn(object):
    def __init__(self, repository_name):
        super(RepoReturn, self).__init__()
        self.clone ={"ssh": "ssh://git@bitbucket.org/{}".format(repository_name)}


class BitbucketVCSInitTest(ParentTestCase):


    @classmethod
    def setUpClass(cls):
        super(BitbucketVCSInitTest, cls).setUpClass()
        cls.vcs = BitbucketVCSProvider()
        cls.vcs.init(None, None, "test", False)
        cls.vcs.bitbucket_repo = TestBitbucketClient()
        cls.vcs.client = "TestClient"

    def validate_exists(self,service_definition):
        repo = self.vcs.find_repo(service_definition)
        self.assertIsNotNone(repo,"Failed to find repo")

    def validate_create(self,service_definition):
        repo = self.vcs.create_repo(service_definition)
        self.assertIsNotNone(repo,"Failed to create repo")

    def test_repo_exists(self):
        application_map = loader.load_service_definitions(self.service_directory)
        loader.walk_service_map(application_map, application_callback=None, service_callback=self.validate_exists)
        self.vcs.client = None
        self.vcs.dry_run = True
        loader.walk_service_map(application_map, application_callback=None, service_callback=self.validate_exists)
        self.vcs.client = "TestClient"

    def test_repo_create(self):
        application_map = loader.load_service_definitions(self.service_directory)
        loader.walk_service_map(application_map, application_callback=None, service_callback=self.validate_create)


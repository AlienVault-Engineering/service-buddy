from service_buddy.service import loader
from service_buddy.vcs.Bitbucket import BitbucketVCSProvider
from service_buddy.vcs.github_vcs import GitHubVCSProvider
from testcase_parent import ParentTestCase


class TestGitHubClient(object):

    def __init__(self, application_map):
        super(TestGitHubClient, self).__init__()
        self.known_repos = []
        for app in application_map.values():
            self.known_repos.extend([RepoReturn(definition.get_repository_name())for definition in app.values()])

    def get_repos(self):
        return self.known_repos

    def create_repo(self,name,private,has_issues,description,has_projects,has_wiki):
        return RepoReturn(repository_name=name)

class RepoReturn(object):
    def __init__(self, repository_name):
        super(RepoReturn, self).__init__()
        self.name = "test/{}".format(repository_name)
        self.ssh_url = "ssh://git@bitbucket.org/{}".format(repository_name)


class GitHubVCSInitTest(ParentTestCase):
    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        super(GitHubVCSInitTest, cls).setUpClass()
        cls.vcs = GitHubVCSProvider()
        cls.vcs.init(None, None, "test", False)

    def validate_exists(self,service_definition):
        repo = self.vcs.find_repo(service_definition)
        self.assertIsNotNone(repo,"Failed to find repo")

    def validate_create(self,service_definition):
        repo = self.vcs.create_repo(service_definition)
        self.assertIsNotNone(repo,"Failed to create repo")

    def test_repo_exists(self):
        application_map = loader.load_service_definitions(self.service_directory)
        self.vcs.client = TestGitHubClient(application_map)
        loader.walk_service_map(application_map, application_callback=None, service_callback=self.validate_exists)
        self.vcs.client = None
        self.vcs.dry_run = True
        loader.walk_service_map(application_map, application_callback=None, service_callback=self.validate_exists)

    def test_repo_create(self):
        application_map = loader.load_service_definitions(self.service_directory)
        self.vcs.client = TestGitHubClient(application_map)
        loader.walk_service_map(application_map, application_callback=None, service_callback=self.validate_create)


import logging

from atlassian.bitbucket import Cloud
from atlassian.bitbucket.cloud.repositories import WorkspaceRepositories
from atlassian.bitbucket.cloud.workspaces import Workspace

from service_buddy_too.service.service import Service
from service_buddy_too.util import command_util
from service_buddy_too.util.command_util import invoke_process


class BitbucketVCSProvider(object):

    @classmethod
    def get_type(cls):
        return 'bitbucket'

    def __init__(self):
        super(BitbucketVCSProvider, self).__init__()
        self.repo_root = ""
        self.workspace_name: str = None
        self.root_workspace: Workspace = None
        self.user = None
        self.password = None

    def init(self, user, password, repo_root):
        if user and password:
            client = Cloud(url="https://api.bitbucket.org/", username=user, password=password)
            self.root_workspace = client.workspaces.get(repo_root)
            self.user = user
            self.password = password
        else:
            logging.info("VCS username and password not configured - assuming git executable has appropriate "
                            "authorization for repo checks")

        self.workspace_name = repo_root

    def find_repo(self, service_definition: Service):
        bitbucket_url = self._get_git_url(service_definition)
        if self.root_workspace:
            exists = self.root_workspace.repositories.exists(service_definition.get_repository_name())
        else:
            exists = service_definition.does_service_directory_exists()
            if not exists:
                result = invoke_process(
                    args=['git', 'ls-remote', bitbucket_url, '>', '/dev/null'], exec_dir=None
                )
                exists = result == 0
        if exists:
            logging.info(f"Found repo for {service_definition.get_fully_qualified_service_name()}: {bitbucket_url}" )
            logging.warning(".")
        else:
            logging.info(f"Could not find repository - {service_definition.get_repository_name()}")
            bitbucket_url = None
        return bitbucket_url

    def _get_git_url(self, service_definition):
        if self.user: #assume has auth if user set
            # git remote set-url origin https://<your username>:${APP_SECRET}@bitbucket.org/${BITBUCKET_REPO_OWNER}/${BITBUCKET_REPO_SLUG}
            bit_prefix = f"https://{self.user}:{self.password}"
        else:
            bit_prefix = f"ssh://git"
        bitbucket_url = f'{bit_prefix}@bitbucket.org/{self.workspace_name}/{service_definition.get_repository_name()}'
        return bitbucket_url

    def create_repo(self, service_definition: Service):
        if command_util.dry_run_global:
            logging.error("Creating repo %r", str(service_definition.get_repository_name()))
        else:
            if self.root_workspace is None:
                raise Exception("VCS pass required for create repo operation")
            project_key = service_definition.get_app().replace('-', '_')
            project = self.root_workspace.projects.exists(project_key)
            if not project:
                logging.info(f"Creating project for {service_definition.get_app()}")
                project = self.root_workspace.projects.create(name=service_definition.get_app(),
                                                              key=project_key,
                                                              description=service_definition.get_app(),
                                                              is_private=True)
            repo = self.root_workspace.repositories.create(project_key=project_key,
                                                           repo_slug=service_definition.get_repository_name().replace('-','_'),
                                                           is_private=True, fork_policy=WorkspaceRepositories.NO_FORKS)
            repo.description = service_definition.get_description()
            repo.name = service_definition.get_fully_qualified_service_name()

        return self._get_git_url(service_definition)

    def update_repo_metadata(self,service_definition:Service):
        if not self.root_workspace:
            logging.warning("Skipping repo metadata update due to lack of username and password")
            return
        if not self.root_workspace.repositories.exists(service_definition.get_repository_name()):
            logging.warning("Tried to update non-existent repo!")
            return
        repository = self.root_workspace.repositories.get(repository=service_definition.get_repository_name())
        repository.description = service_definition.get_description()

import json
import os

from Bitbucket import BitbucketVCSProvider
from service_manager.util.services import walk_service_map, safe_mkdir, ensure_service_directory_exists, invoke_process


class VCS(object):
    def __init__(self, service_directory, dry_run):
        super(VCS, self).__init__()
        default_path = os.path.join(service_directory, "vcs-config.json")
        if os.path.exists(default_path):
            with open(default_path) as fp:
                defaults = json.load(fp)
                self.default_provider = defaults.get('provider',None)
                self.repo_root = defaults.get('root-user',None)
                self.user = defaults.get('user',os.environ.get('VCS_USER'))
                self.password = defaults.get('password',os.environ.get('VCS_PASSWORD'))
        else:
            raise Exception("Could not local 'vcs_config.json' in service directory")
        self.dry_run = dry_run
        self.vcs_providers = {
            BitbucketVCSProvider.get_type(): BitbucketVCSProvider(self.user, self.password, self.repo_root, dry_run)}
        if self.default_provider not in self.vcs_providers:
            raise Exception("Requested provider is not configured {}".format(self.default_provider))

    def _get_default_vcs_provider(self):
        return self.vcs_providers[self.default_provider]

    def validate_repositories(self, application_map):
        def populate_repo_metadata(service_definition):
            self._get_default_vcs_provider().find_repo(service_definition)

        walk_service_map(application_map=application_map, application_callback=None,
                         service_callback=populate_repo_metadata)

    def create_project(self, service_definition, app_dir):
        return self.init_repo(service_definition=service_definition,service_dir=service_definition.get_service_directory(app_dir))

    def init_repo(self, service_definition, service_dir):
        repo_url = self._get_default_vcs_provider().create_repo(service_definition)
        args = ['git', 'init']
        invoke_process(args, exec_dir=service_dir, dry_run=self.dry_run)
        args = ['git', 'add', '*', '**/*']
        invoke_process(args, exec_dir=service_dir, dry_run=self.dry_run)
        args = ['git', 'commit', '-m', 'Initial commit']
        invoke_process(args, exec_dir=service_dir, dry_run=self.dry_run)
        args = ['git', 'remote', 'add', 'origin', repo_url]
        invoke_process(args, exec_dir=service_dir, dry_run=self.dry_run)
        args = ['git', 'push', '-u', 'origin', 'master']
        invoke_process(args, exec_dir=service_dir, dry_run=self.dry_run)
        service_definition.set_git_url(repo_url)

    def pull_services(self, application_map, destination_directory):
        safe_mkdir(destination_directory)

        def clone_repository(service_defintion):
            destination_dir = ensure_service_directory_exists(destination_directory, service_defintion)
            if service_defintion.repo_exists():
                clone_url = service_defintion.get_git_url()
                args = ['git', 'clone', clone_url]
                invoke_process(args, destination_dir, self.dry_run)

        walk_service_map(application_map=application_map, application_callback=None,
                         service_callback=clone_repository)

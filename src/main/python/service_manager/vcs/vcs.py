from Bitbucket import BitbucketVCSProvider
from service_manager.util.services import walk_service_map, _safe_mkdir, ensure_service_directory_exists, invoke_process


class VCS(object):
    def __init__(self, user, password, repo_root, dry_run, default_provider='bitbucket'):
        super(VCS, self).__init__()
        self.dry_run = dry_run
        self.default_provider = default_provider
        self.vcs_providers = {}
        self.vcs_providers[default_provider] = BitbucketVCSProvider(user, password, repo_root, dry_run)

    def _get_default_vcs_provider(self):
        return self.vcs_providers[self.default_provider]

    def validate_repositories(self, application_map):
        def populate_repo_metadata(service_definition):
            self._get_default_vcs_provider().find_repo(service_definition)

        walk_service_map(application_map=application_map, application_callback=None,
                         service_callback=populate_repo_metadata)

    def init_repo(self, service_definition, service_dir):
        repo_url = self._get_default_vcs_provider().create_repo(service_definition)
        args = ['git', 'init']
        invoke_process(args, service_dir=service_dir, dry_run=self.dry_run)
        args = ['git', 'add', '*', '**/*']
        invoke_process(args, service_dir=service_dir, dry_run=self.dry_run)
        args = ['git', 'commit', '-m', 'Initial commit']
        invoke_process(args, service_dir=service_dir, dry_run=self.dry_run)
        args = ['git', 'remote', 'add', 'origin', repo_url]
        invoke_process(args, service_dir=service_dir, dry_run=self.dry_run)
        args = ['git', 'push', '-u', 'origin', 'master']
        invoke_process(args, service_dir=service_dir, dry_run=self.dry_run)

    def pull_services(self, application_map, destination_directory):
        _safe_mkdir(destination_directory)

        def clone_repository(service_defintion):
            destination_dir = ensure_service_directory_exists(destination_directory, service_defintion)
            if service_defintion.repo_exists():
                clone_url = service_defintion.get_git_url()
                args = ['git', 'clone', clone_url]
                invoke_process(args, destination_dir, self.dry_run)

        walk_service_map(application_map=application_map, application_callback=None,
                         service_callback=clone_repository)

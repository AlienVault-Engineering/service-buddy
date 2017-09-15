import json
import os

import logging

from Bitbucket import BitbucketVCSProvider
from service_buddy.service.loader import walk_service_map, safe_mkdir, ensure_app_directory_exists, \
    ensure_service_directory_exists
from service_buddy.service.service import Service
from service_buddy.util.command_util import invoke_process
from service_buddy.vcs.github_vcs import GitHubVCSProvider


class VCS(object):
    def __init__(self, service_directory, dry_run):
        super(VCS, self).__init__()
        default_path = os.path.join(service_directory, "vcs-config.json")
        if os.path.exists(default_path):
            with open(default_path) as fp:
                defaults = json.load(fp)
                self.default_provider = defaults.get('provider', None)
                self.repo_root = defaults.get('root-user', os.environ.get('VCS_ROOT_USER'))
                self.user = defaults.get('user', os.environ.get('VCS_USER'))
                self.password = defaults.get('password', os.environ.get('VCS_PASSWORD'))
        else:
            raise Exception("Could not local 'vcs-config.json' in service directory")
        self.dry_run = dry_run

        self.vcs_providers = {
            BitbucketVCSProvider.get_type(): BitbucketVCSProvider(),
            GitHubVCSProvider.get_type(): GitHubVCSProvider()}

        if self.default_provider not in self.vcs_providers:
            raise Exception("Requested provider is not configured {}".format(self.default_provider))
        else:
            self._get_default_vcs_provider().init(self.user, self.password, self.repo_root, dry_run)

    def _get_default_vcs_provider(self):
        return self.vcs_providers[self.default_provider]

    def validate_repositories(self, application_map):
        def populate_repo_metadata(service_definition):
            repo_url = self._get_default_vcs_provider().find_repo(service_definition)
            service_definition.set_git_url(repo_url)

        walk_service_map(application_map=application_map, application_callback=None,
                         service_callback=populate_repo_metadata)

    def create_project(self, service_definition, app_dir):
        return self.init_repo(service_definition=service_definition,
                              service_dir=service_definition.get_service_directory(app_dir))

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

    def clone_service(self, application_map, destination_directory):
        # type: (dict, str) -> None
        safe_mkdir(destination_directory)

        def clone_repository(service_defintion):
            # type: (Service) -> None
            app_dir = ensure_app_directory_exists(destination_directory, service_defintion)
            if service_defintion.repo_exists():
                clone_url = service_defintion.get_git_url()
                args = ['git', 'clone', clone_url,service_defintion.get_fully_qualified_service_name()]
                service_directory = service_defintion.get_service_directory(app_dir=app_dir)
                if os.path.exists(service_directory):
                    logging.warn("Skipping clone step directory exists - {}".format(service_directory))
                else:
                    invoke_process(args, app_dir, self.dry_run)

        walk_service_map(application_map=application_map, application_callback=None,
                         service_callback=clone_repository)

    def git_exec(self, application_map, destination_directory, args):
        # type: (dict,str, list) -> None

        def git_exec(service_defintion):
            # type: (Service) -> None
            destination_dir = ensure_service_directory_exists(destination_directory=destination_directory,
                                                              service_defintion=service_defintion,
                                                              create=False)
            if not destination_directory:
                logging.warn("Service '{}' did not exist in destination directory - {}".format(service_defintion.get_fully_qualified_service_name(),destination_directory))
                logging.warn("Skipping running git command - git {}".format(str(args)))
                return
            git_args = ['git']
            git_args.extend(args)
            invoke_process(git_args, destination_dir, self.dry_run)

        walk_service_map(application_map=application_map, application_callback=None,
                         service_callback=git_exec)

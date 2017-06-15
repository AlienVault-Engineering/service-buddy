import os
import subprocess

from pybitbucket import repository
from pybitbucket.auth import BasicAuthenticator
from pybitbucket.bitbucket import Client
from requests import HTTPError

from lib.services import walk_service_map, _safe_mkdir, ensure_service_directory_exists, invoke_process


class VCS(object):
    def __init__(self, user, password, repo_root,dry_run):
        super(VCS, self).__init__()
        self.dry_run = dry_run
        self.repo_root = repo_root
        self.bitbucket = Client(
            BasicAuthenticator(
                user,
                password,
                'pybitbucket@mailinator.com'))

    def validate_repositories(self, application_map):

        def populate_repo_metadata(app, service, definition):
            if 'repository' in definition:
                repository_name = definition['repository']
            else:
                repository_name = "{}-{}".format(app, service)
            fq_repository_name = "{}/{}".format(self.repo_root, repository_name)
            try:
                repo = repository.Repository.find_repository_by_full_name(full_name=fq_repository_name,
                                                                          client=self.bitbucket)
                if repo:
                    definition['repository'] = fq_repository_name
                    definition['repository_url'] = repo.clone['ssh']
                else:
                    definition['repository'] = "Not Found"
            except HTTPError:
                definition['repository'] = "Not Found"

        walk_service_map(application_map=application_map, application_callback=None,
                         service_callback=populate_repo_metadata)

    def pull_services(self, application_map, destination_directory):
        _safe_mkdir(destination_directory)

        def clone_repository(app, service, definition):
            service_dir = ensure_service_directory_exists(destination_directory, app, service)
            if 'repository_url' in definition:
                clone_url = definition['repository_url']
                args = ['git', 'clone', clone_url]
                invoke_process(args, service_dir,self.dry_run)


        walk_service_map(application_map=application_map, application_callback=None,
                     service_callback=clone_repository)
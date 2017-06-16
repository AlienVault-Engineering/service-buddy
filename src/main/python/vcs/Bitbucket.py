import logging
from pybitbucket import repository
from pybitbucket.auth import BasicAuthenticator
from pybitbucket.bitbucket import Client
from pybitbucket.repository import RepositoryPayload, RepositoryForkPolicy
from requests import HTTPError


class BitbucketVCSProvider(object):
    def __init__(self, user, password, repo_root,dry_run):
        super(BitbucketVCSProvider, self).__init__()
        self.dry_run = dry_run
        self.client = Client(
            BasicAuthenticator(
                user,
                password,
                'pybitbucket@mailinator.com'))
        self.team_root_user = repo_root

    def find_repo(self, service_definition):
        fq_repository_name = "{}/{}".format(self.team_root_user, service_definition.get_repository_name())
        try:
            repo = repository.Repository.find_repository_by_full_name(full_name=fq_repository_name,
                                                                      client=self.client)
            if repo:
                service_definition.set_git_url(repo.clone['ssh'])
        except HTTPError:
            logging.info("Could not find repository {}".format(service_definition.get_repository_name()))

    def create_repo(self, service_defintion):
        payload = RepositoryPayload()\
                    .add_description(str(service_defintion.get_description()))\
                    .add_is_private(True)\
                    .add_name(service_defintion.get_fully_qualified_service_name())\
                    .add_owner(self.team_root_user)\
                    .add_fork_policy(RepositoryForkPolicy.NO_PUBLIC_FORKS)
        if self.dry_run:
            logging.error("Creating repo {}".format(str(payload)))
        else:
            repo = repository.Repository.create(
                payload=payload,
                repository_name=service_defintion.get_fully_qualified_service_name(),
                owner=self.team_root_user,
                client=self.client )
            return repo.clone['ssh']

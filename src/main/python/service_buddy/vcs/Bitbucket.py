import logging

from pybitbucket import repository
from pybitbucket.auth import BasicAuthenticator
from pybitbucket.bitbucket import Client
from pybitbucket.repository import RepositoryPayload, RepositoryForkPolicy
from requests import HTTPError
import time

from service_buddy.util.command_util import invoke_process


class BitbucketVCSProvider(object):
    @classmethod
    def get_type(cls):
        return 'bitbucket'
    
    def __init__(self):
        super(BitbucketVCSProvider, self).__init__()
        self.repo_root = ""
        self.dry_run = ""
        self.client = None
        self.team_root_user = None
        self.bitbucket_repo = None

    def init(self, user, password, repo_root, dry_run):
        self.dry_run = dry_run
        if user and password:
            self.client = Client(
                BasicAuthenticator(
                    user,
                    password,
                    'pybitbucket@mailinator.com'))
        else:
            logging.warn("VCS username and password not configured - assuming git executable has appropriate "
                         "authorization for repo checks")
            self.client = None
        self.team_root_user = repo_root
        self.bitbucket_repo = repository.Repository

    def _find_repo_api(self, fq_repository_name):
        this_try = 0
        base_sleep = 1
        while this_try < 4:
            try:
                repo = self.bitbucket_repo.find_repository_by_full_name(
                    full_name=fq_repository_name,
                    client=self.client
                )
                return repo.clone['ssh']
            except HTTPError as e:
                logging.error("err = %r", e)
                #if e.errno == 401:
                sleep_time = base_sleep * (2 ** this_try)
                logging.info("Got rate-limited by bitbucket (?), sleeping for %0.1f, try #%d", sleep_time, this_try+1)
                time.sleep(sleep_time)
                this_try += 1

        logging.info("Could not find repository through Bitbucket API - %r", fq_repository_name)

    def find_repo(self, service_definition):
        fq_repository_name = "{}/{}".format(self.team_root_user, service_definition.get_repository_name())
        # logging.info("bitbucket find_repo: %r", fq_repository_name)
        if self.client:
            bitbucket_url = self._find_repo_api(fq_repository_name)
        else:
            bitbucket_url = 'ssh://git@bitbucket.org/{}'.format(fq_repository_name)
            result = invoke_process(
                args=['git', 'ls-remote', bitbucket_url, '>', '/dev/null'], exec_dir=None, dry_run=self.dry_run
            )
            if result != 0:
                logging.info(
                    "Could not find repository with git executable - %r",
                    service_definition.get_repository_name()
                )
                bitbucket_url = None
        return bitbucket_url

    def create_repo(self, service_defintion):
        payload = RepositoryPayload()\
                    .add_description(str(service_defintion.get_description()))\
                    .add_is_private(True)\
                    .add_name(service_defintion.get_fully_qualified_service_name())\
                    .add_owner(self.team_root_user)\
                    .add_fork_policy(RepositoryForkPolicy.NO_PUBLIC_FORKS)
        if self.dry_run:
            logging.error("Creating repo %r", str(payload._payload))
        else:
            if self.client is None:
                raise Exception("VCS pass required for create repo operation")
            repo = self.bitbucket_repo.create(
                payload=payload,
                repository_name=service_defintion.get_fully_qualified_service_name(),
                owner=self.team_root_user,
                client=self.client,
            )
            return repo.clone['ssh']

import os

REPO_URL = 'repository_url'

REPOSITORY_NAME = 'repository'
REPOSITORY_URL = 'repository_url'
DESCRIPTION = 'description'
ROLE = 'role'
APPLICATION = 'application'
FQN = 'project_name'
FORCE_RECREATE_BUILD = 'recreate-build'
SERVICE_TYPE = 'service-type'


class Service(dict):
    def __init__(self, app, role, definition, app_reference=None):
        super(Service, self).__init__()
        self.update(definition)
        self.app_ref = app_reference
        self[APPLICATION] = app
        self[ROLE] = role
        self[FQN] = self.get_fully_qualified_service_name()

    def get_fully_qualified_service_name(self):
        return "{application}-{role}".format(**self).replace(' ','_')

    def force_recreate_build(self):
        return self.get(FORCE_RECREATE_BUILD,os.environ.get('RECREATE_BUILDS',False))

    def get_description(self):
        return self[DESCRIPTION]

    def get_service_type(self):
        return self[SERVICE_TYPE]

    def repo_exists(self):
        return self.get(REPOSITORY_URL,None) is not None

    def get_role(self):
        return self[ROLE]

    def get_app(self):
        return self[APPLICATION]

    def get_repository_name(self):
        return self[REPOSITORY_NAME] if REPOSITORY_NAME in self else self.get_fully_qualified_service_name()

    def set_git_url(self, url):
        self[REPO_URL] = url

    def get_git_url(self):
        return self.get(REPO_URL,None)

    def get_contract_test_git_url(self):
        return self.app_ref.get_contract_test_git_url()

    def get_service_directory(self,app_dir):
        return os.path.join(app_dir,self.get_fully_qualified_service_name())

    def set_service_type(self, param):
        self[SERVICE_TYPE] = param
class Application(dict):
    def __init__(self, application):
        super(Application, self).__init__()
        self.application = application

    def add_service(self, role, service):
        self[role] = service

    def get_contract_test_git_url(self):
        for name,definition in self.iteritems():
            if definition.get_service_type() == 'contract-tests':
                return definition.get_git_url()
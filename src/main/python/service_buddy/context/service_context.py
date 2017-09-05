from service_buddy.service import loader
from service_buddy.vcs.vcs import VCS


class ServiceContext(object):

    def __init__(self, filter_string, directory, dry_run):
        super(ServiceContext, self).__init__()
        self.dry_run = dry_run
        self.application_map = loader.load_service_definitions(service_directory=directory,app_filter=filter_string)
        self.vcs = VCS(service_directory=directory, dry_run=dry_run)

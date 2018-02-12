import os

import logging

from service_buddy.service import loader
from service_buddy.vcs.vcs import VCS


class ServiceContext(object):

    def __init__(self, filter_string, service_filter_string, service_directory, destination_directory, dry_run):
        super(ServiceContext, self).__init__()
        self.destination_directory = destination_directory
        self.dry_run = dry_run
        if not os.path.exists(service_directory):
            logging.warn("Service directory does not exist, not loading services or vcs - {}".format(service_directory))
        else:
            self.application_map = loader.load_service_definitions(service_directory=service_directory, app_filter=filter_string, service_filter=service_filter_string)
            self.vcs = VCS(service_directory=service_directory, dry_run=dry_run)

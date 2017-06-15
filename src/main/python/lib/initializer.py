import subprocess

import logging

from lib import services
from lib.log_handler import print_red_bold
from lib.services import walk_service_map, ensure_service_directory_exists, invoke_process


class Initializer(object):
    def __init__(self, vcs, destination_directory, dry_run):
        super(Initializer, self).__init__()
        self.dry_run = dry_run
        self.destination_directory = destination_directory
        self.vcs = vcs

    def init_service(self, app, service, definition):
        if 'repository_url' in definition:
            logging.info("Service exists - {}-{}".format(app, service))
            return
        service_dir = ensure_service_directory_exists(self.destination_directory, app, service)
        logging.info("Creating Service - {}-{}".format(app, service))
        services.pretty_print_service(app, service, definition)
        args = ['rerun', 'otx:', 'create-otx-project', '--add-repo', 'True', '--project-description',
                definition['description'], '--project-type', definition['service-type'], '--application', app,
                '--role', service]
        invoke_process(args, service_dir, self.dry_run)

    def initialize_services(self, application_map):
        walk_service_map(application_map=application_map, application_callback=None,
                         service_callback=self.init_service)

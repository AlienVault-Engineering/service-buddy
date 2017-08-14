import logging

from service_manager.service_initializer.creators.cookie_cutter_creator import CookeCutterProjectCreator
from service_manager.util import services
from service_manager.util.services import walk_service_map, ensure_service_directory_exists


class Initializer(object):
    def __init__(self, vcs, destination_directory, dry_run,service_template_definitions):
        super(Initializer, self).__init__()
        self.project_creator = CookeCutterProjectCreator(service_template_definitions, dry_run)
        self.dry_run = dry_run
        services.safe_mkdir(destination_directory=destination_directory)
        self.destination_directory = destination_directory
        self.vcs = vcs

    def init_service(self, definition):
        if definition.repo_exists():
            logging.info("Service exists - {}".format(definition.get_fully_qualified_service_name()))
            return
        logging.info("Creating Service -{}".format(definition.get_fully_qualified_service_name()))
        destination_dir = ensure_service_directory_exists(self.destination_directory, service_defintion=definition)
        services.pretty_print_service(definition)
        project_directory= self.project_creator.create_project(definition,destination_dir)
        self.vcs.init_repo(definition,project_directory)

    def initialize_services(self, application_map):
        walk_service_map(application_map=application_map, application_callback=None,
                         service_callback=self.init_service)
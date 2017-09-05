import logging

from service_buddy.ci.bamboo_build_creator import BambooBuildCreator
from service_buddy.code.cookie_cutter_creator import CookeCutterProjectCreator
from service_buddy.service.loader import safe_mkdir, ensure_service_directory_exists, walk_service_map, \
    ensure_app_directory_exists
from service_buddy.service.service import Service
from service_buddy.util.pretty_printer import pretty_print_service


class Initializer(object):
    def __init__(self, vcs, destination_directory, dry_run,service_template_definitions):
        super(Initializer, self).__init__()
        self.code_generator = CookeCutterProjectCreator(service_template_definitions, dry_run)
        self.build_creator = BambooBuildCreator(service_template_definitions, dry_run)
        self.dry_run = dry_run
        safe_mkdir(directory=destination_directory)
        self.destination_directory = destination_directory
        self.vcs = vcs

    def init_app(self,app):
        pass
    
    def init_service(self, definition):
        # type: (Service ) -> None
        if definition.repo_exists():
            logging.info("Service exists - {}".format(definition.get_fully_qualified_service_name()))
            if definition.force_recreate_build():
                self.build_creator.create_project(definition)
            return
        logging.info("Creating Service -{}".format(definition.get_fully_qualified_service_name()))
        app_dir = ensure_app_directory_exists(self.destination_directory, service_defintion=definition)
        pretty_print_service(definition)
        self.code_generator.create_project(definition, app_dir)
        self.vcs.create_project(definition,app_dir)
        self.build_creator.create_project(definition)

    def initialize_services(self, application_map):
        walk_service_map(application_map=application_map, application_callback=self.init_app,
                         service_callback=self.init_service)

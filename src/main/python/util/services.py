import json
from collections import defaultdict

import logging
import os
import subprocess

from util.log_handler import print_red_bold

REPO_URL = 'repository_url'

REPOSITORY_NAME = 'repository'
REPOSITORY_URL = 'repository_url'
DESCRIPTION = 'description'
ROLE = 'role'
APPLICATION = 'application'
FQN = 'project_name'


class Application(dict):

    def __init__(self,application):
        super(Application, self).__init__()
        self.application = application

    def add_service(self,role,service):
        self[role] = service

class Service(dict):
    def __init__(self, app, role, definition):
        super(Service, self).__init__()
        self[APPLICATION] = app
        self[ROLE] = role
        self.update(definition)
        self[FQN]= self.get_fully_qualified_service_name()

    def get_fully_qualified_service_name(self):
        return "{application}-{role}".format(**self)

    def get_description(self):
        return self[DESCRIPTION]

    def repo_exists(self):
        return REPOSITORY_URL in self

    def get_role(self):
        return self[ROLE]

    def get_app(self):
        return self[APPLICATION]

    def get_repository_name(self):
        return self[REPOSITORY_NAME] if REPOSITORY_NAME in self else self.get_fully_qualified_service_name()

    def set_git_url(self,url):
        self[REPO_URL] = url
        
    def get_git_url(self):
        return self[REPO_URL]

def load_service_definitions(app_root, service_directory):
    service_dir = os.path.abspath(service_directory)
    listdir = os.listdir(service_dir)
    service_map = defaultdict(dict)
    for dir in listdir:
        if _is_valid_app(dir, service_dir) and application_filter(app_root,dir):
            service_map[dir] = Application(dir)
            with open(os.path.join(service_dir, dir, 'service.json')) as service_def:
                service_definitions = json.load(service_def)
                for role, definition in service_definitions.iteritems():
                    service_map[dir].add_service(role,Service(app=dir, role=role, definition=definition))
    return service_map


def _is_valid_app(dir, service_dir):
    return os.path.isdir(os.path.join(service_dir, dir)) and not dir.startswith('.')


def application_filter(app_root, application):
    return app_root is None or application.startswith(app_root)


def walk_service_map(application_map, application_callback, service_callback):
    for application, service_map in application_map.iteritems():
        if application_callback: application_callback(application)
        for service, service_definition in service_map.iteritems():
            if service_callback: service_callback(service_definition)


def pretty_print_application(app): logging.error("{}".format(app))


def pretty_print_service(service_definition):
    logging.warn("\t {}".format(service_definition.get_role()))
    for dat in service_definition:
        secondary_indent = '\t\t' if len(dat) <= 10 else '\t'
        logging.info("\t\t {}{}- {}".format(dat, secondary_indent, service_definition[dat]))


def pretty_print_services(application_map):
    walk_service_map(application_map, pretty_print_application, pretty_print_service)


def _safe_mkdir(destination_directory):
    if not os.path.exists(destination_directory):
        os.mkdir(destination_directory)


def ensure_service_directory_exists(destination_directory, service_defintion ):
    app_dir = os.path.join(destination_directory, service_defintion.get_app())
    _safe_mkdir(app_dir)
    return app_dir


def invoke_process(args, service_dir, dry_run):
    if dry_run:
        print_red_bold("\t {}".format(str(args)))
    else:
        subprocess.call(args=args, cwd=service_dir)

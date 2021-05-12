import json
import logging
import os
import re
from collections import defaultdict

from service_buddy_too.service.application import Application
from service_buddy_too.service.service import Service


def load_service_definitions(service_directory, app_filter=None, service_filter=None):
    service_dir = os.path.abspath(service_directory)
    listdir = os.listdir(service_dir)
    service_map = defaultdict(dict)
    for dir in listdir:
        if _is_valid_app(dir, service_dir) and application_filter(app_filter, dir):
            service_definition_file = os.path.join(service_dir, dir, 'service.json')
            if not os.path.exists(service_definition_file):
                logging.warning("Skipping invalid application directory - no service.json exists - {}".format(service_dir))
            else:
                service_map[dir] = Application(dir)
                with open(service_definition_file) as service_def:
                    service_definitions = json.load(service_def)
                    for role, definition in service_definitions.items():
                        if re.match(service_filter or ".*", role):
                            service_map[dir].add_service(
                                role, Service(app=dir, role=role, definition=definition,
                                app_reference=service_map[dir])
                            )
    return service_map


def _is_valid_app(dir, service_dir):
    return os.path.isdir(os.path.join(service_dir, dir)) and not dir.startswith('.')


def application_filter(app_filter, application):
    return app_filter is None or application.startswith(app_filter)


def walk_service_map(application_map, application_callback, service_callback):
    for application, service_map in application_map.items():
        if application_callback: application_callback(application)
        for service, service_definition in service_map.items():
            if service_callback: service_callback(service_definition)


def safe_mkdir(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)


def ensure_app_directory_exists(destination_directory, service_defintion):
    app_dir = os.path.join(destination_directory, service_defintion.get_app())
    safe_mkdir(app_dir)
    return app_dir


def ensure_service_directory_exists(destination_directory, service_defintion, create=True):
    app_dir = ensure_app_directory_exists(destination_directory=destination_directory,
                                          service_defintion=service_defintion)
    service_directory = service_defintion.get_service_directory(app_dir=app_dir)
    if create:
        safe_mkdir(service_directory)
        return service_directory
    else:
        if os.path.exists(service_directory):
            return service_directory
        return None

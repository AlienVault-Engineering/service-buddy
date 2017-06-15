import json
from collections import defaultdict

import logging
import os
import subprocess

from lib.log_handler import print_red_bold


def load_service_definitions(app_root, service_directory):
    service_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), service_directory)
    listdir = os.listdir(service_dir)
    service_map = defaultdict(dict)
    for dir in listdir:
        if os.path.isdir(os.path.join(service_dir,dir)) and not dir.startswith('.') and application_filter(app_root, dir):
            with open(os.path.join(service_dir, dir, 'service.json')) as service_def:
                service_map[dir] = json.load(service_def)
    return service_map


def application_filter(app_root, application):
    return app_root is None or application.startswith(app_root)


def walk_service_map(application_map, application_callback, service_callback):
    for application, service_map in application_map.iteritems():
        if application_callback: application_callback(application)
        for service, definition in service_map.iteritems():
            if service_callback: service_callback(application, service, definition)


def pretty_print_application(app): logging.error("{}".format(app))


def pretty_print_service(application, service, definition):
    logging.warn("\t {}".format(service))
    for dat in definition:
        secondary_indent = '\t\t' if len(dat) <=10 else '\t'
        logging.info("\t\t {}{}- {}".format(dat,secondary_indent, definition[dat]))


def pretty_print_services(application_map):
    walk_service_map(application_map, pretty_print_application, pretty_print_service)


def _safe_mkdir(destination_directory):
    if not os.path.exists(destination_directory):
        os.mkdir(destination_directory)


def ensure_service_directory_exists(destination_directory, app, service, ):
    app_dir = os.path.join(destination_directory, app)
    _safe_mkdir(app_dir)
    service_dir = os.path.join(app_dir, service)
    _safe_mkdir(service_dir)
    return service_dir


def invoke_process( args, service_dir,dry_run):
    if dry_run:
        print_red_bold("\t {}".format(str(args)))
    else:
        subprocess.call(args=args, cwd=service_dir)
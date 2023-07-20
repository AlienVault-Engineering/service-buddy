import logging

from service_buddy_too.service.loader import walk_service_map

from service_buddy_too.service.service import Service


def pretty_print_application(app): logging.error(u"{}".format(app))


def pretty_print_service(service_definition):
    logging.warning(u"\t {}".format(service_definition.get_role()))
    for dat in service_definition:
        secondary_indent = '\t\t' if len(dat) <= 10 else '\t'
        logging.info(u"\t\t {}{}- {}".format(dat, secondary_indent, service_definition[dat]))

def print_fqsn_service(service_definition:Service):
    logging.warning(service_definition.get_fully_qualified_service_name())

def pretty_print_services(application_map):
    walk_service_map(application_map, pretty_print_application, pretty_print_service)

def print_fqsn_services(application_map):
    walk_service_map(application_map, None, print_fqsn_service)

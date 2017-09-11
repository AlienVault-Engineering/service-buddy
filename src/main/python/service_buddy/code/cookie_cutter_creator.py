import json
import os

import logging
from cookiecutter.main import cookiecutter


def _make_cookie_safe(service_definition):
    ret = {}
    for key, valey in service_definition.iteritems():
        ret[key.replace('-', "_")] = valey
    return ret


class CookeCutterProjectCreator(object):
    def __init__(self, template_dir, dry_run, templates):
        super(CookeCutterProjectCreator, self).__init__()
        self.template_dir = template_dir
        self.templates =templates
        self.dry_run = dry_run

    def create_project(self, service_definition, app_dir):
        template = self._lookup_service_template(service_definition.get_service_type())
        if template['type'] == 'file':
            location = os.path.abspath(os.path.join(self.template_dir, template['location']))
        else:
            location = template['location']

        extra_context = _make_cookie_safe(service_definition)
        if self.dry_run:
            logging.error("Creating project from template {} ".format(location))
        else:
            return cookiecutter(location, no_input=True, extra_context=extra_context, output_dir=app_dir)

    def _lookup_service_template(self, service_type):
        if service_type not in self.templates:
            raise Exception("Unknown code template - {}".format(service_type))
        return self.templates[service_type]

    @classmethod
    def get_type(cls):
        return "cookiecutter"


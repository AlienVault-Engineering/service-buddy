import json
import os

from service_buddy.util.command_util import invoke_process


class BambooBuildCreator(object):

    def __init__(self, template_dir,dry_run):
        self.dry_run = dry_run
        self.template_dir = template_dir
        bamboo_config = os.path.join(os.path.abspath(template_dir),"build-config.json")
        with open(bamboo_config) as builtin:
            settings = json.load(builtin)
            self.url = settings['bamboo-url']
            self.build_templates = settings['build-templates']

    def create_project(self, definition):
        if definition.get_service_type() not in self.build_templates:
            raise Exception("Build template not found for service type {}".format(definition.get_service_type()))
        else:
            build_template = self.build_templates.get(definition.get_service_type())['type']


        args = [
            'java',
            '-jar',
            'bamboo-plan-1.0-SNAPSHOT.jar',
            '--build-template', build_template,
            '--bamboo-url', self.url,
            '--application', definition.get_app(),
            '--role', definition.get_role()
        ]
        invoke_process(args, exec_dir=self.template_dir, dry_run=self.dry_run)

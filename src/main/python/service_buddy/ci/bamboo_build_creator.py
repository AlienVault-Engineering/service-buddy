import json
import os
from service_buddy.util.command_util import invoke_process


class BambooBuildCreator(object):

    def __init__(self, template_dir, dry_run, default_config, build_templates):
        self.dry_run = dry_run
        self.template_dir = template_dir
        self.url = default_config['bamboo-url']
        self.build_templates = build_templates

    def create_project(self, service_definition,service_dir):
        if service_definition.get_service_type() not in self.build_templates:
            raise Exception("Build template not found for service type {}".format(service_definition.get_service_type()))
        else:
            build_template = self.build_templates.get(service_definition.get_service_type())['type']


        args = [
            'java',
            '-jar',
            'bamboo-plan-1.0-SNAPSHOT.jar',
            '--build-template', build_template,
            '--bamboo-url', self.url,
            '--application', service_definition.get_app(),
            '--role', service_definition.get_role()
        ]
        invoke_process(args, exec_dir=self.template_dir, dry_run=self.dry_run)

    @classmethod
    def get_type(cls):
        return "bamboo"

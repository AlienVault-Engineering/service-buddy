import json
import os
from service_buddy.util.command_util import invoke_process


class BambooBuildCreator(object):

    def init(self, dry_run, default_config, build_templates):
        self.dry_run = dry_run
        self.url = default_config['bamboo-url']
        self.build_templates = build_templates

    def create_project(self, service_definition,app_dir):
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
            '--role', service_definition.get_role(),
            '-Dbamboo.specs.log.level=DEBUG'
        ]

        res = invoke_process(args, dry_run=self.dry_run)
        if res>0:
            raise Exception("Error creating bamboo build")

    @classmethod
    def get_type(cls):
        return "bamboo"

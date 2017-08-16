import json
import os

from service_manager.util.services import invoke_process


class BambooBuildCreator(object):

    def __init__(self, template_dir,dry_run):
        self.dry_run = dry_run
        self.template_dir = template_dir
        bamboo_config = os.path.join(os.path.abspath(template_dir),"build-config.json")
        with open(bamboo_config) as builtin:
            settings = json.load(builtin)
            self.url = settings['bamboo-url']

    def create_project(self, definition):
        args = [
            'java',
            '-jar',
            'bamboo-plan-1.0-SNAPSHOT.jar',
            '--bamboo-url', self.url,
            '--application', definition.get_app(),
            '--role', definition.get_role()
        ]
        invoke_process(args, exec_dir=self.template_dir, dry_run=self.dry_run)

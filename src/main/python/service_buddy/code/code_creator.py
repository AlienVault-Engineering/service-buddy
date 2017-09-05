import json
import os

import logging

from service_buddy.code.cookie_cutter_creator import CookeCutterProjectCreator


class CodeCreator(object):
    def __init__(self, code_template_directory, dry_run):
        super(CodeCreator, self).__init__()
        default_path = os.path.join(code_template_directory, "code-template-config.json")
        if os.path.exists(default_path):
            with open(default_path) as fp:
                defaults = json.load(fp)
                self.default_provider = defaults.get('provider', None)
                self.extended_templates = defaults.get('code-template-definitions', {})
        else:
            logging.warn("Could not local 'code-template-config.json' in code template directory")
            self.default_provider = "cookiecutter"
            self.extended_templates ={}
        built_in = self._load_service_templates(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'builtin_service_templates.json'))
        built_in.update(self.extended_templates)
        self.code_creators = {
            CookeCutterProjectCreator.get_type(): CookeCutterProjectCreator(template_dir=code_template_directory,
                                                                            dry_run=dry_run,
                                                                            templates=built_in)}
        if self.default_provider not in self.code_creators:
            raise Exception("Requested provider is not configured {}".format(self.default_provider))

    def _load_service_templates(self, builtIn):
        # type: (str) -> dict
        with open(builtIn) as builtin:
            return json.load(builtin)

    def get_default_code_creator(self):
        # type: () -> CodeCreator
        return self.code_creators[self.default_provider]

    def create_project(self, service_definition, service_dir):
        return self.get_default_code_creator().create_project(service_definition=service_definition,
                                                              service_dir=service_dir)

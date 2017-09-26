import json
import os

import logging

from copy import deepcopy

from service_buddy.service.service import Service
from service_buddy.code.cookie_cutter_creator import CookeCutterProjectCreator
from service_buddy.service.service_template_generator import ServiceTemplateGenerator


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
            logging.info("Could not locate 'code-template-config.json' in code template directory")
            self.default_provider = "cookiecutter"
            self.extended_templates = {}
        built_in = self._load_service_templates(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'builtin-code-templates.json'))
        built_in.update(self.extended_templates)
        self.templates = self._resolve_alias(built_in)
        self.service_template_generator = ServiceTemplateGenerator()
        self.code_creators = {
            CookeCutterProjectCreator.get_type(): CookeCutterProjectCreator(template_dir=code_template_directory,
                                                                            dry_run=dry_run,
                                                                            templates=self.templates)}
        if self.default_provider not in self.code_creators:
            raise Exception("Requested provider is not configured {}".format(self.default_provider))

    def _resolve_alias(self, templates):
        ret = {}
        for key, value in templates.iteritems():
            if value['type'] == 'alias':
                ret[key] = deepcopy(templates[value['lookup']])
                value.pop('type')
                value.pop('lookup')
                ret[key].update(value)
            else:
                ret[key] = value
        return ret

    def _load_service_templates(self, builtIn):
        # type: (str) -> dict
        with open(builtIn) as builtin:
            return json.load(builtin)

    def get_default_code_creator(self):
        # type: () -> CodeCreator
        return self.code_creators[self.default_provider]

    def create_project(self, service_definition, app_dir):
        # type: (Service, str) -> None
        project = self.get_default_code_creator().create_project(service_definition=service_definition,
                                                                 app_dir=app_dir)
        service_type_ = self.templates[service_definition.get_service_type()]
        create_service_def = service_type_.get('generate-service-definition', True)
        if create_service_def:
           self.service_template_generator.create_project(service_definition,app_dir,service_type=service_type_.get('service-definition',None))
        return project

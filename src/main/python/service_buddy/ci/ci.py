import json
import os
import logging
from service_buddy.ci.bamboo_build_creator import BambooBuildCreator


class BuildCreator(object):
    def __init__(self, template_directory, dry_run):
        super(BuildCreator, self).__init__()
        default_path = os.path.join(template_directory, "build-config.json")
        if os.path.exists(default_path):
            with open(default_path) as fp:
                defaults = json.load(fp)
                self.default_provider = defaults.get('provider', None)
                self.build_templates = defaults.get('build-templates', {})
                self.default_config = defaults
        else:
            logging.warn("Could not local 'build-config.json' in code template directory")
            self.default_provider = "bamboo"
        self.code_creators = {
            BambooBuildCreator.get_type(): BambooBuildCreator(template_dir=template_directory,
                                                              dry_run=dry_run,
                                                              default_config=self.default_config,
                                                              build_templates=self.build_templates)}
        if self.default_provider not in self.code_creators:
            raise Exception("Requested provider is not configured {}".format(self.default_provider))

    def _get_default_build_creator(self):
        # type: () -> BuildCreator
        return self.code_creators[self.default_provider]

    def create_project(self, service_definition, service_dir=None):
        return self._get_default_build_creator().create_project(service_definition=service_definition,
                                                                service_dir=service_dir)

import os

from service.service import Service


class BitBucketPipelineBuildCreator(object):

    def options(self):
        return {}

    def init(self, dry_run, default_config, build_templates, user=None, password=None):
        self.dry_run = dry_run
        self.build_templates = build_templates
        self.build_configuration = default_config.get('build-configuration', {})

    def create_project(self, service_definition, app_dir):
        # type: (Service, str) -> None
        pass
        # if service_definition.get_service_type() not in self.build_templates:
        #     raise Exception(
        #         "Build template not found for service type {}".format(service_definition.get_service_type()))
        # else:
        #     build_type = self.build_templates.get(service_definition.get_service_type())['type']
        # service_dir = service_definition.get_service_directory(app_dir=app_dir)
        # if os.path.exists(self._get_pipeline_file(service_dir)):
        #     logging.warn("travis build file exists - enabling repo")
        #     self._invoke_travis(['enable'], exec_dir=service_dir)
        # else:
        #     build_template = self.build_configuration.get(build_type, None)
        #     if build_template:
        #         self.create_build(service_dir, build_template, service_definition)
        #     else:
        #         logging.warn("Could not locate build template"
        #                      " for build type - {}:{}".format(service_definition.get_service_type(),
        #                                                       build_type))

    def _get_pipeline_file(self, service_dir):
        return os.path.join(service_dir, "bitbucket-pipelines.yml")

    @classmethod
    def get_type(cls):
        return "bitbucket_pipeline"

    def create_build(self, service_dir, build_template, service_definition):
        language_ = build_template.get('language', 'python')

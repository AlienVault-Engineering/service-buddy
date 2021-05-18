import os

# noinspection PyUnresolvedReferences
from infra_buddy.commandline import cli
from infra_buddy.commands.generate_service_definition import command as gen_service
from infra_buddy.context.deploy_ctx import DeployContext

from service_buddy_too.service.loader import safe_mkdir


class ServiceTemplateGenerator(object):

    def create_project(self, service_definition, service_type=None, defaults=None):
        if not service_type:
            service_type = service_definition.get_service_type()
        service_def_folder = os.path.join(service_definition.get_service_directory(), "service")
        safe_mkdir(service_def_folder)
        gen_service.do_command(DeployContext.create_deploy_context(
            application=service_definition.get_app(),
            role=service_definition.get_role(),
            environment='dev',
            defaults=defaults
        ), service_type=service_type,
            destination=service_def_folder)

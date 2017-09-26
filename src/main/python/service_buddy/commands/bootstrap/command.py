import os

import click
from infra_buddy.context.deploy_ctx import DeployContext

from service_buddy.code.code_creator import CodeCreator
from service_buddy.commandline import cli
from service_buddy.context.service_context import ServiceContext
from service_buddy.service.service import Service
from infra_buddy.commands.bootstrap import command as bootstrap


@cli.command(name='bootstrap', short_help="Create a repository containing the initial definition for a micro-service "
                                          "stack managed by service-buddy.")
@click.option("--application", envvar='APPLICATION', required=True,
              help='Application name for new micro-service stack.  Brevity suggested.')
@click.option("--deploy-region", envvar='REGION',
              help='Region to initialize the application.')
@click.option("--skip-infrastructure-bootstrap", is_flag=True, envvar="SKIP_ENV",
              help="Skip the bootstrap of the infrastructure for "
                   "this application.")
@click.pass_obj
def bootstrap(service_ctx, application, skip_infrastructure_bootstrap, deploy_region=None):
    # type: (ServiceContext, str,bool,str) -> None
    cc = CodeCreator("", service_ctx.dry_run)
    service_def = Service(app=application, role="master", definition={})
    service_def.set_service_type("service-buddy-master")
    directory = service_ctx.destination_directory
    if directory == "./code": #override default for this usecase
        directory = "./"
    cc.create_project(service_definition=service_def, app_dir=directory)
    if deploy_region:
        os.environ.setdefault('REGION', deploy_region)
    if not skip_infrastructure_bootstrap:
        bootstrap.do_command(
            DeployContext.create_deploy_context(
                application=application,
                role="none",
                environment='dev'
            ),
            ['ci', 'prod']
        )

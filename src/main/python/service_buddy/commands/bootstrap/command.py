import click

from service_buddy.code.code_creator import CodeCreator
from service_buddy.commandline import cli
from service_buddy.context.service_context import ServiceContext
from service_buddy.service.service import Service


@cli.command(name='bootstrap',short_help="Create a repository containing the initial definition for a micro-service stack managed by service-buddy.")
@click.option("--application", envvar='APPLICATION', required=True,
              help='Application name for new micro-service stack.  Suggest brevity.')
@click.pass_obj
def bootstrap(service_ctx,application):
    # type: (ServiceContext, str) -> None
    cc = CodeCreator("", service_ctx.dry_run)
    service_def = Service(app=application,role="master",definition={})
    service_def.set_service_type("service-buddy-master")
    cc.create_project(service_definition=service_def,service_dir=service_ctx.destination_directory)